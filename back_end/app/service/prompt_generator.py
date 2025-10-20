import json
import os
from app.models.base_model import BaseModel

class PromptGenerator(BaseModel):
    """
    Génère un prompt JSON prêt pour l'API (OpenAI, Perplexity…)
    à partir des données sémantiques extraites du site.
    """

    def __init__(self, 
                 prompt_file="prompt_data.json", 
                 output_file="rgpd_prompt_to_model.json"):
        super().__init__()
        self.prompt_file = prompt_file
        self.output_file = output_file
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
        self.prompt_data = self.load_prompt_data()

    def load_prompt_data(self):
        if not os.path.exists(self.prompt_file):
            raise FileNotFoundError(f"❌ Fichier introuvable : {self.prompt_file}")
        with open(self.prompt_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_prompt_text(self):
        return (
            "⚠️ Réponds uniquement en JSON valide, sans explications.\n"
            "Tu es un assistant IA spécialisé en conformité RGPD.\n"
            "Analyse les extraits de site suivants et évalue leur conformité pour chaque point RGPD.\n\n"
            f"Extraits de site :\n{json.dumps(self.prompt_data, ensure_ascii=False, indent=2)}\n\n"
            f"Points RGPD à évaluer : {', '.join(self.rgpd_points)}\n\n"
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

    def save_prompt(self):
        prompt_text = self.build_prompt_text()
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump({"prompt": prompt_text}, f, ensure_ascii=False, indent=2)
        print(f"✅ Prompt généré et sauvegardé dans : {self.output_file}")

# ==========================
# 🔹 Main
# ==========================
if __name__ == "__main__":
    generator = PromptGenerator()
    generator.save_prompt()

























