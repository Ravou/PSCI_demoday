import json
import os

# Fichier de sortie pour le prompt
OUTPUT_FILE = "rgpd_prompt_to_model.json"

# Checklist RGPD complète
CHECKLIST_TEXT = """Checklist RGPD pour audit d’un site web

1️⃣ Cookies et traceurs
- Identifier tous les cookies et traceurs présents sur le site.
- Consentement avant cookies non essentiels.
- Bouton “Refuser tout”.
- Retrait facile du consentement.
- Politique de cookies détaillée et à jour.

2️⃣ Politique de confidentialité
- Types de données collectées.
- Finalité du traitement.
- Base légale pour chaque traitement.
- Durée de conservation.
- Droits des utilisateurs (accès, rectification, suppression…)
- Moyen d’exercer les droits.
- Lisibilité et accessibilité.

3️⃣ Mentions légales
- Responsable du traitement
- Coordonnées de contact
- Hébergeur

4️⃣ Formulaires et consentements
- Cases décochées par défaut
- Finalité claire
- Preuve du consentement

5️⃣ Sécurité et transferts
- HTTPS actif
- Sécurité serveur
- Transferts hors UE encadrés

6️⃣ Mineurs et publics spécifiques
- Consentement parental si mineurs
- Langage adapté

7️⃣ Documentation et registre (hors site)
- Registre des traitements
- Procédures internes RGPD

8️⃣ Rapport final
- Synthèse des points conformes/non conformes
- Actions correctives prioritaires
- Références RGPD/CNIL
- Score global (0–100%)
"""

# Exemple d'extraits de site (snippets)
site_snippets = [
    {"url": "https://example.com", "type": "static", "excerpt": "Exemple de texte extrait du site."},
    {"url": "https://example.com/contact", "type": "static", "excerpt": "Formulaire de contact et consentement."}
]

# Génération du prompt
prompt = (
    "Tu es un assistant IA spécialisé en conformité RGPD. "
    "Analyse les extraits du site web et évalue leur conformité à chaque point de la checklist. "
    "Réponds uniquement sous forme d'un JSON valide, strictement selon le format ci-dessous.\n\n"
    f"Extraits de site (max {len(site_snippets)} snippets) :\n"
    f"{json.dumps(site_snippets, ensure_ascii=False, indent=2)}\n\n"
    "Checklist RGPD :\n"
    f"{CHECKLIST_TEXT}\n\n"
    "Format JSON attendu :\n"
    "[\n"
    "  {\n"
    "    \"point\": \"Nom du point RGPD (ex: Cookies et traceurs)\",\n"
    "    \"status\": \"conforme | partiellement conforme | non conforme | non détecté\",\n"
    "    \"evidence\": \"Court extrait du site justifiant l'évaluation\",\n"
    "    \"recommendation\": \"Recommandation simple et concrète\"\n"
    "  }\n"
    "]\n\n"
    "⚠️ Ne mets rien en dehors du JSON."
)

# Sauvegarde dans un fichier
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"prompt": prompt}, f, ensure_ascii=False, indent=2)

print(f"✅ Prompt généré et sauvegardé dans : {OUTPUT_FILE}")
