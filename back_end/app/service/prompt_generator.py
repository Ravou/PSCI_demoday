import json

PROMPT_FILE = "prompt_data.json"
OUTPUT_PROMPT_FILE = "rgpd_prompt_to_model.json"

# Points RGPD
RGPD_POINTS = [
    "Cookies et traceurs",
    "Politique de confidentialité",
    "Mentions légales",
    "Formulaires et consentements",
    "Sécurité et transferts",
    "Mineurs",
    "Documentation",
    "Rapport final"
]

# Charger les données sémantiques
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompt_data = json.load(f)

# Construire le prompt
prompt_text = (
    "⚠️ Réponds uniquement en JSON valide, sans explications.\n"
    "Tu es un assistant IA spécialisé en conformité RGPD.\n"
    "Analyse les extraits de site suivants et évalue leur conformité pour chaque point RGPD.\n\n"
    f"Extraits de site :\n{json.dumps(prompt_data, ensure_ascii=False, indent=2)}\n\n"
    f"Points RGPD à évaluer : {', '.join(RGPD_POINTS)}\n\n"
    "Format JSON attendu :\n"
    "[\n"
    "  {\n"
    "    \"point\": \"Nom du point RGPD\",\n"
    "    \"status\": \"conforme | partiellement conforme | non conforme | non détecté\",\n"
    "    \"evidence\": \"Court extrait du site justifiant l'évaluation\",\n"
    "    \"recommendation\": \"Recommandation simple et concrète\"\n"
    "  }\n"
    "]"
)

# Sauvegarde
with open(OUTPUT_PROMPT_FILE, "w", encoding="utf-8") as f:
    json.dump({"prompt": prompt_text}, f, ensure_ascii=False, indent=2)

print(f"✅ Prompt généré et sauvegardé dans : {OUTPUT_PROMPT_FILE}")
























