import json
import os
from app.models.base_model import BaseModel
from app.service.utils import cosine_similarity  # si tu as une fonction utilitaire
from typing import List, Dict, Any


class SemanticMatcher(BaseModel):
    """
    Classe pour faire correspondre les résultats NLP analysés avec la structure RGPD.
    Hérite de BaseModel pour cohérence avec les autres modules (FastAPI, ORM, etc.)
    """

    def __init__(self,
                 nlp_output_path="data/nlp_output.json",
                 rgpd_path="data/rgpd_structure.json",
                 output_path="data/prompt_data.json"):
        super().__init__()
        self.nlp_output_path = nlp_output_path
        self.rgpd_path = rgpd_path
        self.output_path = output_path

    def load_json(self, path: str) -> Any:
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Fichier introuvable : {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def extract_nlp_entries(self, data: Dict) -> List[Dict]:
        """
        Récupère proprement la liste des pages ou sections depuis nlp_output.json,
        quelle que soit la structure racine.
        """
        if isinstance(data, list):
            return data
        if "site_analysis" in data:
            return data["site_analysis"]
        if "results" in data:
            return data["results"]
        # fallback : une seule entrée
        return [data]

    def match_sections(self, nlp_data: List[Dict], rgpd_data: Dict) -> List[Dict]:
        """
        Fait correspondre les sections NLP à la structure RGPD
        via une mesure de similarité.
        """
        results = []

        for page in nlp_data:
            url = page.get("url", "")
            for section in page.get("sections", []):
                section_text = section.get("contenu", "")
                best_match, best_score = None, 0.0

                for rgpd_key, rgpd_info in rgpd_data.items():
                    rgpd_text = rgpd_info.get("description", "")
                    score = cosine_similarity(section_text, rgpd_text)
                    if score > best_score:
                        best_score, best_match = rgpd_key, score

                results.append({
                    "url": url,
                    "section_type": section.get("type", ""),
                    "content": section_text,
                    "best_rgpd_match": best_match,
                    "similarity_score": best_score
                })

        return results

    def save_prompt_data(self, matched_data: List[Dict]):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(matched_data, f, indent=2, ensure_ascii=False)
        print(f"✅ prompt_data.json généré : {self.output_path}")

    def run(self):
        """Exécute tout le pipeline de matching."""
        print("🚀 Lancement du SemanticMatcher...")

        nlp_data_raw = self.load_json(self.nlp_output_path)
        rgpd_data = self.load_json(self.rgpd_path)

        nlp_entries = self.extract_nlp_entries(nlp_data_raw)
        matched = self.match_sections(nlp_entries, rgpd_data)
        self.save_prompt_data(matched)

        print(f"✅ {len(matched)} correspondances générées avec succès.")
        return matched


if __name__ == "__main__":
    matcher = SemanticMatcher()
    matcher.run()



