import json
from app.models.base_model import BaseModel

class PromptGenerator(BaseModel):
    """Génère un prompt RGPD compatible Perplexity API (full mémoire)."""

    def __init__(self):
        super().__init__()
        self.output_prompt = None
        self.rgpd_points = [
            "Cookies et traceurs",
            "Politique de confidentialité",
            "Mentions légales",
            "Formulaires et consentements",
            "Sécurité et transferts",
            "Mineurs",
            "Documentation",
            "Rapport final",
        ]

    @staticmethod
    def dict_to_list(site_dict: dict) -> list:
        """Convertit un dict {url: {...}} en liste [{url, sections}] pour l’API."""
        result = []
        for url, content in site_dict.items():
            result.append({
                "url": url,
                "sections": content.get("sections", [])
            })
        return result

    def generate_prompt(self, prompt_data: dict) -> dict:
        if not isinstance(prompt_data, dict):
            raise TypeError("❌ prompt_data doit être un dict.")

        # Conversion dict → liste pour l’API
        prompt_data_list = self.dict_to_list(prompt_data)

        prompt_text = (
            "⚠️ Réponds uniquement par un JSON valide.\n"
            "Analyse les extraits de site suivants et évalue chaque point RGPD.\n"
            "Pour chaque point, indique les articles légaux utilisés.\n\n"
            f"Extraits de site : {json.dumps(prompt_data_list, ensure_ascii=False)}\n"
            f"Points RGPD à évaluer : {', '.join(self.rgpd_points)}\n\n"
            "Format JSON attendu : "
            "[" 
            "{\"point\": \"Nom du point RGPD\", "
            "\"status\": \"conforme | partiellement conforme | non conforme | non détecté\", "
            "\"evidence\": \"Court extrait du site justifiant l'évaluation\", "
            "\"recommendation\": \"Recommandation simple et concrète\", "
            "\"articles\": \"Articles légaux utilisés pour cette évaluation\"}"
            "]"
        )

        self.output_prompt = {
            "model": "sonar-medium-chat",
            "messages": [
                {"role": "system", "content": "Tu es un assistant IA spécialisé en conformité RGPD."},
                {"role": "user", "content": prompt_text}
            ]
        }

        # Vérification rapide
        if not isinstance(self.output_prompt, dict) or "model" not in self.output_prompt or "messages" not in self.output_prompt:
            raise ValueError("❌ Payload généré invalide.")

        print("✅ Prompt généré en mémoire et prêt pour Perplexity.")
        return self.output_prompt


