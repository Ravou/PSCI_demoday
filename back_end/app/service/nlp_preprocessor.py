import re
import json
from langdetect import detect
from unidecode import unidecode
import nltk
import spacy
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# =====================================
# 📥 Téléchargement NLTK
# =====================================
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords", quiet=True)

# =====================================
# ⚙️ Modèles spaCy
# =====================================
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

# =====================================
# 🔍 Détection de langue
# =====================================
def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"

# =====================================
# 🧼 Nettoyage / regex + métadonnées
# =====================================
def clean_text_with_metadata(text):
    text = unidecode(text)
    metadata = {
        "emails": re.findall(r"\S+@\S+", text),
        "phones": re.findall(r"\b\d{10,}\b", text),
        "urls": re.findall(r"http\S+|www\S+", text)
    }
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower(), metadata

# =====================================
# ✂️ Tokenisation (NLTK)
# =====================================
def sentence_tokenize(text, lang="fr"):
    """
    Tokenise un texte en phrases selon la langue.
    Langue supportée : 'fr' pour français, 'en' pour anglais.
    """
    language_map = {"fr": "french", "en": "english"}
    language = language_map.get(lang, "french")  # fallback sur français
    
    try:
        return nltk.sent_tokenize(text, language=language)
    except LookupError:
        # Télécharger punkt si manquant
        nltk.download("punkt")
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
    nlp = nlp_fr if lang == "fr" else nlp_en
    doc = nlp(text)
    processed = []
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.like_num:
            processed.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_
            })
    return processed

# =====================================
# 🧠 NER (spaCy)
# =====================================
def extract_entities(text, lang="fr"):
    nlp = nlp_fr if lang == "fr" else nlp_en
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
        result = sentiment_analyzer(text[:512])
        return result[0]
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
# =====================================
# 🧪 Traitement des fichiers JSON (robuste)
# =====================================
# ...existing code...
def process_rgpd_json(file_path):
    """
    Traite rgpd_structure.json :
    - Analyse le texte de chaque article RGPD
    """
    with open(file_path, "r", encoding="utf-8") as f:
        rgpd = json.load(f)
    chapitres = rgpd.get("reglement", {}).get("dispositif_normatif", {}).get("chapitres", [])
    for chapitre in chapitres:
        for article in chapitre.get("articles", []):
            texte = article.get("contenu", "")
            if texte.strip():
                print(f"\n=== {article.get('numero')} - {chapitre.get('titre')} ===")
                print(texte[:300], "...\n")
                nlp_result = nlp_pipeline(texte)
                print("NLP RGPD :", nlp_result)

def process_crawler_json(file_path):
    """
    Traite crawler_results.json :
    - Analyse le texte principal de chaque page
    - Analyse tous les textes RGPD de chaque page
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        # 1️⃣ Texte principal (static > text)
        main_text = item.get("static", {}).get("text", "")
        print(f"\n=== Page #{idx+1} : {item.get('url')} ===")
        print("Texte principal :")
        print(main_text[:300], "...\n")
        nlp_result = nlp_pipeline(main_text)
        print("NLP principal :", nlp_result)

        # 2️⃣ Textes RGPD (static > textes_rgpd)
        textes_rgpd = item.get("static", {}).get("textes_rgpd", {})
        for rgpd_url, rgpd_text in textes_rgpd.items():
            if rgpd_text.strip():
                print(f"\n--- RGPD ({rgpd_url}) ---")
                print(rgpd_text[:300], "...\n")
                nlp_result_rgpd = nlp_pipeline(rgpd_text)
                print("NLP RGPD :", nlp_result_rgpd)

if __name__ == "__main__":
    # 1️⃣ Traiter RGPD JSON
    process_rgpd_json("rgpd_structure.json")

    # 2️⃣ Traiter Crawler JSON (texte principal + textes RGPD)
    process_crawler_json("crawler_results.json")

