import json
from typing import Dict, Any, List
from app.models.base_model import BaseModel


class PromptGenerator(BaseModel):
    """Génère un prompt RGPD compatible Perplexity API."""

    MAX_CONTENT_LENGTH = 8000  # assez grand pour sonar-pro
    MAX_SECTION_LENGTH = 600   # limite sûre par section

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
    def clean_text(text: Any) -> str:
        """Nettoie le texte (caractères non imprimables)."""
        if not isinstance(text, str):
            text = str(text)
        return ''.join(c if 32 <= ord(c) <= 126 else ' ' for c in text)

    def dict_to_list(self, site_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convertit un dict {url: {...}} en liste [{url, sections}] pour l’API."""
        result = []
        for url, content in site_dict.items():
            sections = content.get("sections", [])
            truncated_sections = []
            for s in sections:
                s_clean = self.clean_text(s)
                if len(s_clean) > self.MAX_SECTION_LENGTH:
                    s_clean = s_clean[:self.MAX_SECTION_LENGTH] + "..."
                truncated_sections.append(s_clean)
            result.append({
                "url": self.clean_text(url),
                "sections": truncated_sections
            })
        return result

    def generate_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Construit un prompt structuré et conforme au schéma attendu par Perplexity."""
        if not isinstance(prompt_data, dict):
            raise TypeError("❌ prompt_data doit être un dict.")

        prompt_data_list = self.dict_to_list(prompt_data)
        site_json = json.dumps(prompt_data_list, ensure_ascii=False)

        prompt_text = (
            "⚠️ Réponds uniquement par un JSON valide, sans texte explicatif.\n"
            "Tu es un auditeur RGPD chargé d’évaluer un site web.\n"
            "Analyse les extraits suivants et attribue une évaluation pour chaque point RGPD.\n"
            "Format de réponse attendu : liste JSON.\n\n"
            f"Extraits du site : {site_json}\n\n"
            f"Points RGPD à évaluer : {', '.join(self.rgpd_points)}\n\n"
            "Format JSON attendu : ["
            "{\"point\": \"Nom du point RGPD\", "
            "\"status\": \"conforme | partiellement conforme | non conforme | non détecté\", "
            "\"evidence\": \"Court extrait justifiant l’évaluation\", "
            "\"recommendation\": \"Recommandation simple et concrète\", "
            "\"articles\": \"Articles légaux utilisés\"}"
            "]"
        )

        # tronquer uniquement si le texte total dépasse la limite API
        if len(prompt_text) > self.MAX_CONTENT_LENGTH:
            prompt_text = prompt_text[:self.MAX_CONTENT_LENGTH] + "\n…[truncated]"

        # ✅ Structure finale acceptée par Perplexity API
        self.output_prompt = {
            "model": "sonar-pro",  # ← modèle valide
            "messages": [
                {"role": "system", "content": "Tu es un assistant IA spécialisé en conformité RGPD."},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.2,
            "max_tokens": 1500
        }

        print("✅ Prompt généré avec succès, prêt pour Perplexity.")
        return self.output_prompt


# === Exemple d’exécution directe ===
if __name__ == "__main__":
    pg = PromptGenerator()
    example_data = {
        "https://exemple.com": {
            "sections": [
                "Voici un exemple de contenu RGPD avec cookies.",
                "Une autre section de texte expliquant la politique de confidentialité."
            ]
        }
    }
    prompt = pg.generate_prompt(example_data)
    print(json.dumps(prompt, indent=2, ensure_ascii=False))
