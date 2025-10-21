import json
from app.models.base_model import BaseModel

class PromptGenerator(BaseModel):
    """Génère un prompt RGPD à partir de données sémantiques."""

    def __init__(self):
        super().__init__()
        self.prompt_file = "prompt_data.json"
        self.output_prompt_file = "rgpd_prompt_to_model.json"

        # Points RGPD
        self.rgpd_points = [
            "Cookies et traceurs",
            "Politique de confidentialité",
            "Mentions légales",
            "Formulaires et consentements",
            "Sécurité et transferts",
            "Mineurs",
            "Documentation",
            "Rapport final"
        ]

    def generate_prompt(self):
        # Charger les données sémantiques
        with open(self.prompt_file, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)

        # Construire le prompt
        prompt_text = (
            "⚠️ Réponds uniquement par un JSON valide, sans aucun texte explicatif.\n"
            "Ne mets rien avant ni après le JSON.\n"
            "Tu es un assistant IA spécialisé en conformité RGPD.\n"
            "Analyse les extraits de site suivants et évalue leur conformité pour chaque point RGPD.\n\n"
            f"Extraits de site :\n{json.dumps(prompt_data, ensure_ascii=False, indent=2)}\n\n"
            f"Points RGPD à évaluer : {', '.join(self.rgpd_points)}\n\n"
            "Format JSON attendu :\n"
            "[\n"
            "  {\n"
            "    \"point\": \"Nom du point RGPD\",\n"
            "    \"status\": \"conforme | partiellement conforme | non conforme | non détecté\",\n"
            "    \"evidence\": \"Court extrait du site justifiant l'évaluation\",\n"
            "    \"recommendation\": \"Recommandation simple et concrète\"\n"
            "  }\n"
            "]\n"
    )


        # Sauvegarde
        with open(self.output_prompt_file, "w", encoding="utf-8") as f:
            json.dump({"prompt": prompt_text}, f, ensure_ascii=False, indent=2)

        print(f"✅ Prompt généré et sauvegardé dans : {self.output_prompt_file}")

if __name__ == "__main__":
    pg = PromptGenerator()
    pg.generate_prompt()
