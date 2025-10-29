import os
import re
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
import json

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
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "Tu es un assistant NLP spécialisé en conformité RGPD."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        resp = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def perplexity_pipeline(self, text: str):
        """
        Appelle l'API Perplexity et renvoie le JSON d'analyse.
        """
        prompt = f"""
        Analyse ce texte RGPD et renvoie un JSON structuré avec les champs :
        - lang
        - summary
        - sentiment
        - entities
        - themes
        - recommendations

        Texte :
        {text[:4000]}
        """
        result = self.call_perplexity(prompt)
        return {
            "model": "Perplexity",
            "analysis": result,
            "text_length": len(text)
        }

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
    # 🔹 Wrapper principal
    # ------------------
    def nlp_pipeline(self, text: str):
        if self.has_pplx:
            return self.perplexity_pipeline(text)
        else:
            return self.local_nlp_pipeline(text)

    # ------------------
    # 🔹 Parsing Perplexity pour SemanticMatcher
    # ------------------
    def parse_perplexity_output(self, nlp_output: dict):
        """
        Parse le champ 'analysis' et retourne un dict exploitable
        """
        analysis_text = nlp_output.get("analysis", "{}")
        try:
            parsed = json.loads(analysis_text)
        except json.JSONDecodeError:
            parsed = {}
        return parsed

    def nlp_sections_for_matching(self, nlp_output: dict, url: str):
        """
        Crée des sections utilisables par SemanticMatcher
        """
        parsed = self.parse_perplexity_output(nlp_output)
        sections = []

        # Résumé
        summary_text = parsed.get("summary", "")
        if summary_text.strip():
            vector = self.vectorize_text(summary_text).tolist()
            sections.append({
                "type": "text",
                "url_source": url,
                "contenu": summary_text,
                "nlp": {
                    "model": nlp_output.get("model"),
                    "vector": vector
                }
            })

        # Recommandations
        for rec in parsed.get("recommendations", []):
            if rec.strip():
                vector = self.vectorize_text(rec).tolist()
                sections.append({
                    "type": "text",
                    "url_source": url,
                    "contenu": rec,
                    "nlp": {
                        "model": nlp_output.get("model"),
                        "vector": vector
                    }
                })

        # Texte complet
        full_text = f"{summary_text} {' '.join(parsed.get('recommendations', []))}".strip()
        if full_text:
            vector = self.vectorize_text(full_text).tolist()
            sections.append({
                "type": "text",
                "url_source": url,
                "contenu": full_text,
                "nlp": {
                    "model": nlp_output.get("model"),
                    "vector": vector
                }
            })

        return sections

    def build_site_data(self, nlp_outputs: list):
        """
        Construit un dictionnaire site_data prêt pour SemanticMatcher
        """
        site_data = []
        for entry in nlp_outputs:
            url = entry.get("url", "unknown_url")
            sections = self.nlp_sections_for_matching(entry, url)
            site_data.append({
                "url": url,
                "sections": sections
            })
        return site_data


