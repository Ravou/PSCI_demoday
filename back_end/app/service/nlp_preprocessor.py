import re
import json
import os
from app.models.base_model import BaseModel
from langdetect import detect, DetectorFactory
from unidecode import unidecode
import nltk
import spacy
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import math

# ==========================
# 📥 Préparations NLTK / spaCy
# ==========================
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")
nlp_fallback = spacy.load("xx_ent_wiki_sm")  # fallback multilingue

DetectorFactory.seed = 0  # reproductibilité

# Hugging Face pipelines
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# ==========================
# 🌟 Classe NLPPreprocessor adaptée GPT-Neo
# ==========================
class NLPPreprocessor(BaseModel):
    CHUNK_SIZE = 2000  # nombre de caractères par chunk pour GPT-Neo

    def __init__(self):
        super().__init__()
        self.nlp_fr = nlp_fr
        self.nlp_en = nlp_en
        self.nlp_fallback = nlp_fallback
        self.sentiment_analyzer = sentiment_analyzer
        self.tokenizer = tokenizer
        self.model = model

    # ------------------
    # Détection de langue
    # ------------------
    def detect_lang(self, text: str) -> str:
        if not text or not text.strip():
            return "unknown"
        if len(text.split()) < 5:
            doc = self.nlp_fallback(text)
            return getattr(doc, "lang_", "unknown")
        try:
            return detect(text)
        except:
            doc = self.nlp_fallback(text)
            return getattr(doc, "lang_", "unknown")

    # ------------------
    # Nettoyage et métadonnées
    # ------------------
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
    # Tokenisation
    # ------------------
    def sentence_tokenize(self, text: str, lang="fr"):
        language_map = {"fr": "french", "en": "english"}
        language = language_map.get(lang, "french")
        try:
            return nltk.sent_tokenize(text, language=language)
        except LookupError:
            nltk.download("punkt", quiet=True)
            return nltk.sent_tokenize(text, language=language)

    def tokenize_text(self, text: str, lang="fr"):
        tokens = []
        for sent in self.sentence_tokenize(text, lang):
            tokens.extend(word_tokenize(sent, language="french" if lang == "fr" else "english"))
        return tokens

    # ------------------
    # Lemmatisation / POS
    # ------------------
    def spacy_processing(self, text: str, lang="fr"):
        nlp = self.nlp_fr if lang == "fr" else self.nlp_en
        doc = nlp(text)
        return [{"text": t.text, "lemma": t.lemma_, "pos": t.pos_}
                for t in doc if not t.is_stop and not t.is_punct and not t.like_num]

    # ------------------
    # NER
    # ------------------
    def extract_entities(self, text: str, lang="fr"):
        nlp = self.nlp_fr if lang == "fr" else self.nlp_en
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    # ------------------
    # Sentiment HF
    # ------------------
    def sentiment_analysis(self, text: str):
        try:
            return self.sentiment_analyzer(text[:512])[0]
        except:
            return {"label": "neutral", "score": 0.0}

    # ------------------
    # Vectorisation HF
    # ------------------
    def vectorize_text(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()
        return embeddings.numpy()

    # ------------------
    # NLP complet + snippets pour GPT-Neo
    # ------------------
    def nlp_pipeline(self, text: str):
        lang = self.detect_lang(text)
        cleaned, metadata = self.clean_text_with_metadata(text)
        tokens = self.tokenize_text(cleaned, lang)
        lemmas_pos = self.spacy_processing(cleaned, lang)
        entities = self.extract_entities(cleaned, lang)
        sentiment = self.sentiment_analysis(cleaned)
        vector = self.vectorize_text(cleaned)

        # Découpage en chunks pour GPT-Neo
        snippets = []
        if len(cleaned) > self.CHUNK_SIZE:
            for i in range(math.ceil(len(cleaned)/self.CHUNK_SIZE)):
                start = i * self.CHUNK_SIZE
                end = (i+1) * self.CHUNK_SIZE
                snippets.append(cleaned[start:end])
        else:
            snippets.append(cleaned)

        return {
            "lang": lang,
            "cleaned_text": cleaned,
            "metadata": metadata,
            "tokens": tokens,
            "lemmas_pos": lemmas_pos,
            "entities": entities,
            "sentiment": sentiment,
            "vector_shape": vector.shape,
            "vector": vector.tolist(),
            "snippets": snippets
        }

    # ====================================================
    # 🔹 Sauvegarde séparée : RGPD (statique) / Site (dynamique)
    # ====================================================
    def save_rgpd_embeddings(self, rgpd_path: str, cache_path="rgpd_embeddings.json"):
        if os.path.exists(cache_path):
            print(f"✅ Cache RGPD trouvé : {cache_path} — pas de recalcul.")
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

        rgpd_analysis = []
        if os.path.exists("rgpd_embeddings.json"):
            with open("rgpd_embeddings.json", "r", encoding="utf-8") as f:
                rgpd_analysis = json.load(f)

        nlp_output = {
            "site_analysis": site_results,
            "rgpd_analysis": rgpd_analysis
        }

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(nlp_output, out, ensure_ascii=False, indent=2)
        print(f"✅ NLP dynamique et RGPD enregistré dans {output_path}")


# ==========================
# 🔹 Main
# ==========================
if __name__ == "__main__":
    nlp_proc = NLPPreprocessor()
    nlp_proc.save_rgpd_embeddings("rgpd_structure.json", cache_path="rgpd_embeddings.json")
    nlp_proc.save_audit_nlp_output("crawler_results.json", output_path="nlp_output.json")


