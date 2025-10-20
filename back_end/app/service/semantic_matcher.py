import json
import torch
from sentence_transformers import util
from app.models.base_model import BaseModel  # Assure-toi que BaseModel existe

class SemanticMatcher(BaseModel):
    """
    Effectue le matching sémantique entre les sections du site et la checklist RGPD.
    Produit un JSON prêt pour le générateur de prompt.
    """

    def __init__(self, rgpd_embeddings_path="rgpd_embeddings.json", nlp_output_path="nlp_output.json"):
        super().__init__()  # Initialisation de BaseModel

        # Chargement RGPD embeddings
        with open(rgpd_embeddings_path, "r", encoding="utf-8") as f:
            self.rgpd_data = json.load(f)

        # Chargement NLP output
        with open(nlp_output_path, "r", encoding="utf-8") as f:
            self.site_data = json.load(f)

        # ✅ S'assurer qu'on a une liste de pages
        if isinstance(self.site_data, dict):
            # on prend la première valeur de dict si c’est un seul champ comme "site_analysis"
            possible_key = next(iter(self.site_data))
            if isinstance(self.site_data[possible_key], list):
                self.site_data = self.site_data[possible_key]
            else:
                raise ValueError("Format inattendu de nlp_output.json : aucune liste de pages trouvée.")

    @staticmethod
    def cosine_similarity(vec1, vec2):
        t1 = torch.tensor(vec1)
        t2 = torch.tensor(vec2)
        return util.cos_sim(t1, t2).item()

    def match_section(self, dynamic_vector, threshold=0.75, top_k=3):
        matches = []
        for section in self.rgpd_data:
            score = self.cosine_similarity(dynamic_vector, section["embedding"])
            if score >= threshold:
                matches.append({
                    "numero": section["numero"],
                    "titre_chapitre": section["titre_chapitre"],
                    "score": round(score, 4),
                    "contenu": section["contenu"]
                })
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:top_k] if top_k else matches

    def build_prompt_data(self, threshold=0.75, top_k=3):
        prompt_data = []
        for page in self.site_data:
            page_entry = {"url": page.get("url"), "sections": []}
            for section in page.get("sections", []):
                vector = section["nlp"]["vector"]
                matches = self.match_section(vector, threshold=threshold, top_k=top_k)
                page_entry["sections"].append({
                    "type": section.get("type"),
                    "url_source": section.get("url_source"),
                    "contenu": section.get("contenu"),
                    "matches": matches
                })
            prompt_data.append(page_entry)
        return prompt_data

    def save_prompt_data(self, output_path="prompt_data.json", threshold=0.75, top_k=3):
        data = self.build_prompt_data(threshold=threshold, top_k=top_k)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Données sémantiques sauvegardées dans {output_path}")


if __name__ == "__main__":
    matcher = SemanticMatcher()
    matcher.save_prompt_data()




