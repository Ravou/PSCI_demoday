import re
import json
from langdetect import detect, DetectorFactory
from unidecode import unidecode
import nltk
import spacy
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# =====================================
# 📥 Téléchargement NLTK
# =====================================
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# =====================================
# ⚙️ Modèles spaCy
# =====================================
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")
nlp_fallback = spacy.load("xx_ent_wiki_sm")  # Multilingue fallback

# =====================================
# 🔍 Détection de langue
# =====================================
DetectorFactory.seed = 0  # Pour rendre les résultats reproductibles

def detect_lang(text):
    if not text or not text.strip():
        return "unknown"
    text = text.strip()
    if len(text.split()) < 5:
        doc = nlp_fallback(text)
        return doc.lang_ if doc.lang_ else "unknown"
    try:
        return detect(text)
    except:
        doc = nlp_fallback(text)
        return doc.lang_ if doc.lang_ else "unknown"

# =====================================
# 🧼 Nettoyage / regex + métadonnées
# =====================================
def clean_text_with_metadata(text):
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

# =====================================
# ✂️ Tokenisation (NLTK)
# =====================================
def sentence_tokenize(text, lang="fr"):
    language_map = {"fr": "french", "en": "english"}
    language = language_map.get(lang, "french")
    try:
        return nltk.sent_tokenize(text, language=language)
    except LookupError:
        nltk.download("punkt", quiet=True)
        return nltk.sent_tokenize(text, language=language)

def tokenize_text(text, lang="fr"):
    tokens = []
    for sent in sentence_tokenize(text, lang):
        tokens.extend(word_tokenize(sent, language="french" if lang=="fr" else "english"))
    return tokens

# =====================================
# 🧹 Lemmatisation / POS (spaCy)
# =====================================
def spacy_processing(text, lang="fr"):
    nlp = nlp_fr if lang=="fr" else nlp_en
    doc = nlp(text)
    processed = []
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.like_num:
            processed.append({"text": token.text, "lemma": token.lemma_, "pos": token.pos_})
    return processed

# =====================================
# 🧠 NER (spaCy)
# =====================================
def extract_entities(text, lang="fr"):
    nlp = nlp_fr if lang=="fr" else nlp_en
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# =====================================
# ❤️ Sentiment (Hugging Face)
# =====================================
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def sentiment_analysis(text):
    try:
        return sentiment_analyzer(text[:512])[0]
    except:
        return {"label": "neutral", "score": 0.0}

# =====================================
# 🚀 Vectorisation Hugging Face
# =====================================
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def vectorize_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze()
    return embeddings.numpy()

# =====================================
# 🧩 Pipeline NLP global
# =====================================
def nlp_pipeline(text):
    lang = detect_lang(text)
    cleaned, metadata = clean_text_with_metadata(text)
    tokens = tokenize_text(cleaned, lang)
    lemmas_pos = spacy_processing(cleaned, lang)
    entities = extract_entities(cleaned, lang)
    sentiment = sentiment_analysis(cleaned)
    vector = vectorize_text(cleaned)
    return {
        "lang": lang,
        "cleaned_text": cleaned,
        "metadata": metadata,
        "tokens": tokens,
        "lemmas_pos": lemmas_pos,
        "entities": entities,
        "sentiment": sentiment,
        "vector_shape": vector.shape
    }

# =====================================
# 🧪 Traitement des fichiers JSON
# =====================================
def process_rgpd_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        rgpd = json.load(f)
    chapitres = rgpd.get("reglement", {}).get("dispositif_normatif", {}).get("chapitres", [])
    for chapitre in chapitres:
        for article in chapitre.get("articles", []):
            texte = article.get("contenu", "")
            if texte.strip():
                print(f"\n=== {article.get('numero')} - {chapitre.get('titre')} ===")
                print(texte[:300], "...\n")
                print("NLP RGPD :", nlp_pipeline(texte))

def process_crawler_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for idx, item in enumerate(data):
        print(f"\n=== Page #{idx+1} : {item.get('url')} ===")

        # 🔹 Texte principal dynamique
        main_text = item.get("dynamic", {}).get("resultats", {}).get("html_text_snippet", "")
        if main_text.strip():
            print("Texte principal dynamique :")
            print(main_text[:300], "...\n")
            print("NLP principal :", nlp_pipeline(main_text))
        else:
            print("Texte principal dynamique vide.\n")

        # 🔹 Textes RGPD statiques
        textes_rgpd = item.get("static", {}).get("textes_rgpd", {})
        if textes_rgpd:
            for rgpd_url, rgpd_text in textes_rgpd.items():
                if rgpd_text.strip():
                    print(f"\n--- RGPD ({rgpd_url}) ---")
                    print(rgpd_text[:300], "...\n")
                    print("NLP RGPD :", nlp_pipeline(rgpd_text))
                else:
                    print(f"\n--- RGPD ({rgpd_url}) vide ---\n")
        else:
            print("Pas de textes RGPD statiques.\n")

# =====================================
# 🔹 Main
# =====================================
if __name__ == "__main__":
    process_rgpd_json("rgpd_structure.json")
    process_crawler_json("crawler_results.json")

