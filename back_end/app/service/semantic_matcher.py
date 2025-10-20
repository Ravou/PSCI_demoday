import json
import torch
from sentence_transformers import util

class SemanticMatcher:
    """
    Semantic matcher compatible avec le NLPPreprocessor
    et prêt à alimenter le PromptBuilder.
    """

    def __init__(self, rgpd_embeddings_path="rgpd_embeddings.json", nlp_output_path="nlp_output.json"):
        # Charger RGPD statique
        with open(rgpd_embeddings_path, "r", encoding="utf-8") as f:
            self.rgpd_data = json.load(f)
        # Charger NLP dynamique
        with open(nlp_output_path, "r", encoding="utf-8") as f:
            self.site_data = json.load(f)

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
        if top_k:
            matches = matches[:top_k]
        return matches

    def build_prompt_data(self, threshold=0.75, top_k=3):
        """
        Prépare le JSON prêt pour le PromptBuilder.
        """
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
        print(f"✅ Données prêtes pour PromptBuilder dans {output_path}")
    
    # à la fin de semantic_matcher.py ou semantic_matcher_for_promptbuilder.py
if __name__ == "__main__":
    matcher = SemanticMatcher(
        rgpd_embeddings_path="rgpd_embeddings.json",
        nlp_output_path="nlp_output.json"
    )
    matcher.save_prompt_data(
        output_path="prompt_data.json",
        threshold=0.75,
        top_k=3
    )

