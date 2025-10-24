import os
import re
import json
import math
import torch
import requests
from unidecode import unidecode
from langdetect import detect, DetectorFactory
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoTokenizer, AutoModel
from app.models.base_model import BaseModel
import nltk
import spacy
from dotenv import load_dotenv 

# ==========================
# 📥 Charger le fichier .env
# ==========================
load_dotenv() 

# ==========================
# 📥 Préparations NLTK / spaCy
# ==========================
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")
nlp_fallback = spacy.load("xx_ent_wiki_sm")
DetectorFactory.seed = 0

# ==========================
# 🌐 Classe principale
# ==========================
class NLPPreprocessor(BaseModel):
    CHUNK_SIZE = 2000

    def __init__(self):
        super().__init__()
        # Récupère la clé depuis .env
        self.pplx_key = os.getenv("PERPLEXITY_API_KEY")
        self.has_pplx = bool(self.pplx_key)

        if not self.has_pplx:
            print("⚙️ Mode local Hugging Face (aucune clé Perplexity détectée).")
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )

    # ------------------
    # 🔹 API Perplexity
    # ------------------
    def call_perplexity(self, prompt: str):
        if not self.pplx_key:
            raise ValueError("⚠️ PERPLEXITY_API_KEY non trouvée.")
        headers = {
            "Authorization": f"Bearer {self.pplx_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "",
            "messages": [
                {"role": "system", "content": "Tu es un assistant NLP spécialisé en conformité RGPD."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        resp = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    # ------------------
    # 🔹 Nettoyage & métadonnées
    # ------------------
    def detect_lang(self, text: str):
        if not text or not text.strip():
            return "unknown"
        try:
            return detect(text)
        except:
            doc = nlp_fallback(text)
            return getattr(doc, "lang_", "unknown")

    def clean_text_with_metadata(self, text: str):
        if not text:
            return "", {}
        text = unidecode(text)
        metadata = {
            "emails": re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text),
            "phones": re.findall(r"\b\d{10,}\b", text),
            "urls": re.findall(r"https?://[^\s]+|www\.[^\s]+", text)
        }
        text = re.sub(r"<.*?>", " ", text)
        text = re.sub(r"\d+", "<NUM>", text)
        text = re.sub(r"[^\w\s'-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower(), metadata

    # ------------------
    # 🔹 Version locale HF (fallback)
    # ------------------
    def local_nlp_pipeline(self, text: str):
        lang = self.detect_lang(text)
        cleaned, metadata = self.clean_text_with_metadata(text)
        nlp = nlp_fr if lang == "fr" else nlp_en
        doc = nlp(cleaned)

        tokens = [t.text for t in doc if not t.is_stop and not t.is_punct]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        sentiment = self.sentiment_analyzer(cleaned[:512])[0]
        vector = self.vectorize_text(cleaned)

        snippets = []
        if len(cleaned) > self.CHUNK_SIZE:
            for i in range(math.ceil(len(cleaned) / self.CHUNK_SIZE)):
                snippets.append(cleaned[i*self.CHUNK_SIZE:(i+1)*self.CHUNK_SIZE])
        else:
            snippets.append(cleaned)

        return {
            "lang": lang,
            "cleaned_text": cleaned,
            "metadata": metadata,
            "tokens": tokens,
            "entities": entities,
            "sentiment": sentiment,
            "vector_shape": vector.shape,
            "vector": vector.tolist(),
            "snippets": snippets
        }

    def vectorize_text(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()
        return embeddings.numpy()

    # ------------------
    # 🔹 Version API Perplexity
    # ------------------
    def perplexity_pipeline(self, text: str):
        prompt = f"""
        Analyse ce texte RGPD et renvoie un JSON structuré avec les champs :
        - "lang"
        - "summary"
        - "sentiment"
        - "entities"
        - "themes"
        - "recommendations"

        Texte :
        {text[:4000]}
        """

        try:
            result = self.call_perplexity(prompt)
            return {"model": "Perplexity", "analysis": result, "text_length": len(text)}
        except Exception as e:
            return {"model": "Perplexity", "error": str(e)}

    # ------------------
    # 🔹 Wrapper principal
    # ------------------
    def nlp_pipeline(self, text: str):
        if self.has_pplx:
            return self.perplexity_pipeline(text)
        else:
            return self.local_nlp_pipeline(text)

    # ====================================================
    # 🔹 Sauvegarde RGPD / Site
    # ====================================================
    def save_rgpd_embeddings(self, rgpd_path: str, cache_path="rgpd_embeddings.json"):
        if os.path.exists(cache_path):
            print(f"✅ Cache RGPD trouvé : {cache_path} — pas de recalcul.")
            return

        if self.has_pplx:
            print("⚠️ Mode Perplexity : embeddings locaux non générés (texte uniquement).")
            return

        print(f"📘 Génération du cache RGPD à partir de {rgpd_path}...")
        results = []
        with open(rgpd_path, "r", encoding="utf-8") as f:
            rgpd = json.load(f)

        chapitres = rgpd.get("reglement", {}).get("dispositif_normatif", {}).get("chapitres", [])
        for chapitre in chapitres:
            for article in chapitre.get("articles", []):
                texte = article.get("contenu", "")
                if texte.strip():
                    results.append({
                        "numero": article.get("numero"),
                        "titre_chapitre": chapitre.get("titre"),
                        "contenu": texte,
                        "embedding": self.vectorize_text(texte).tolist()
                    })

        with open(cache_path, "w", encoding="utf-8") as out:
            json.dump(results, out, ensure_ascii=False, indent=2)
        print(f"✅ Embeddings RGPD enregistrés dans {cache_path}")

    def save_audit_nlp_output(self, crawler_path: str, output_path="nlp_output.json"):
        site_results = []
        with open(crawler_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            page_data = {"url": item.get("url"), "sections": []}

            # Contenu dynamique
            main_text = item.get("dynamic", {}).get("resultats", {}).get("html_text_snippet", "")
            if main_text.strip():
                page_data["sections"].append({
                    "type": "dynamic",
                    "contenu": main_text,
                    "nlp": self.nlp_pipeline(main_text)
                })

            # Contenu statique RGPD
            textes_rgpd = item.get("static", {}).get("textes_rgpd", {})
            for rgpd_url, rgpd_text in textes_rgpd.items():
                if rgpd_text.strip():
                    page_data["sections"].append({
                        "type": "static",
                        "url_source": rgpd_url,
                        "contenu": rgpd_text,
                        "nlp": self.nlp_pipeline(rgpd_text)
                    })

            site_results.append(page_data)

        output_data = {"site_analysis": site_results}
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(output_data, out, ensure_ascii=False, indent=2)
        print(f"✅ NLP complet sauvegardé dans {output_path}")


# ==========================
# 🔹 Main
# ==========================
if __name__ == "__main__":
    nlp_proc = NLPPreprocessor()
    nlp_proc.save_rgpd_embeddings("rgpd_structure.json", cache_path="rgpd_embeddings.json")
    nlp_proc.save_audit_nlp_output("crawler_results.json", output_path="nlp_output.json")
