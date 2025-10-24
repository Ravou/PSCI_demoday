import json
import torch
from sentence_transformers import util
from app.models.base_model import BaseModel

class SemanticMatcher(BaseModel):
    """
    Fait le matching sémantique entre sections d’un site et les embeddings RGPD.
    Retourne un dict prêt pour PromptGenerator ou stockage en base.
    """

    def __init__(self, rgpd_embeddings_path="rgpd_embeddings.json", nlp_output_path=None, site_data=None):
        super().__init__()

        # --- Chargement des embeddings RGPD ---
        with open(rgpd_embeddings_path, "r", encoding="utf-8") as f:
            self.rgpd_data = json.load(f)

        # --- Chargement des données du site ---
        if site_data is not None:
            self.site_data = site_data
        elif nlp_output_path is not None:
            with open(nlp_output_path, "r", encoding="utf-8") as f:
                self.site_data = json.load(f)
        else:
            raise ValueError("Il faut passer soit site_data soit nlp_output_path.")

        # --- Normalisation : dict → list si nécessaire ---
        if isinstance(self.site_data, dict):
            # si dict, on prend la première clé qui contient la liste
            first_key = next(iter(self.site_data))
            if isinstance(self.site_data[first_key], list):
                self.site_data = self.site_data[first_key]
            else:
                raise ValueError("Format inattendu : aucune liste de pages trouvée.")

    @staticmethod
    def cosine_similarity(vec1, vec2):
        """Retourne la similarité cosinus entre deux vecteurs."""
        t1 = torch.tensor(vec1)
        t2 = torch.tensor(vec2)
        return util.cos_sim(t1, t2).item()

    def match_section(self, dynamic_vector, threshold=0.75, top_k=3):
        """Renvoie les matches RGPD au-dessus du seuil, triés par score."""
        matches = []
        for section in self.rgpd_data:
            if "embedding" not in section or not section["embedding"]:
                continue
            score = self.cosine_similarity(dynamic_vector, section["embedding"])
            if score >= threshold:
                matches.append({
                    "numero": section.get("numero"),
                    "titre_chapitre": section.get("titre_chapitre"),
                    "score": round(score, 4),
                    "contenu": section.get("contenu")
                })
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:top_k] if top_k else matches

    def build_prompt_data(self, threshold=0.75, top_k=3) -> dict:
        """
        Retourne un dict structuré :
        {
            "url_1": {"sections": [...matches...]},
            "url_2": {"sections": [...matches...]},
        }
        """
        prompt_data = {}
        for page in self.site_data:
            url = page.get("url", "unknown_url")
            prompt_data[url] = {"sections": []}

            for section in page.get("sections", []):
                vector = section.get("nlp", {}).get("vector")
                if vector is None:
                    continue
                matches = self.match_section(vector, threshold=threshold, top_k=top_k)
                prompt_data[url]["sections"].append({
                    "type": section.get("type"),
                    "url_source": section.get("url_source"),
                    "contenu": section.get("contenu"),
                    "matches": matches
                })
        return prompt_data

    def save_prompt_data(self, output_path="prompt_data.json", threshold=0.75, top_k=3):
        """Sauvegarde le prompt dict en JSON."""
        data = self.build_prompt_data(threshold=threshold, top_k=top_k)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Données sémantiques sauvegardées dans {output_path}")


if __name__ == "__main__":
    matcher = SemanticMatcher()
    matcher.save_prompt_data()




