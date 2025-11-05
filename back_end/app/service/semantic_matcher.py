import json
import torch
from sentence_transformers import SentenceTransformer, util


class SemanticMatcher:
    """
    Performs semantic matching between site sections and GDPR embeddings.
    Automatically generates vectors if missing in NLP data.
    Returns a dict ready for PromptGenerator or database storage.
    """


    def __init__(self, rgpd_data: list, site_data: list, embedding_model_name: str = "all-MiniLM-L6-v2"):


        if rgpd_data is None:
            raise ValueError("GDPR embeddings must be provided in memory")
        self.rgpd_data = rgpd_data


        if site_data is None:
            raise ValueError("Site data must be provided")
        self.site_data = site_data


        # --- Normalize dict → list if needed ---
        if isinstance(self.site_data, dict):
            first_key = next(iter(self.site_data))
            if isinstance(self.site_data[first_key], list):
                self.site_data = self.site_data[first_key]
            else:
                raise ValueError("Unexpected format: no list of pages found.")


        # --- Model to generate vectors ---
        self.embedding_model = SentenceTransformer(embedding_model_name)


    @staticmethod
    def cosine_similarity(vec1, vec2):
        """Returns the cosine similarity between two vectors."""
        t1 = torch.tensor(vec1)
        t2 = torch.tensor(vec2)
        return util.cos_sim(t1, t2).item()


    def match_section(self, dynamic_vector, threshold=0.75, top_k=3):
        """Returns GDPR matches above threshold, sorted by score."""
        matches = []
        for section in self.rgpd_data:
            if "embedding" not in section or not section["embedding"]:
                continue
            score = self.cosine_similarity(dynamic_vector, section["embedding"])
            if score >= threshold:
                matches.append({
                    "number": section.get("numero"),
                    "chapter_title": section.get("titre_chapitre"),
                    "score": round(score, 4),
                    "content": section.get("contenu")
                })
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:top_k] if top_k else matches


    def build_prompt_data(self, threshold: float = 0.75, top_k: int = 3) -> dict:
        """
        Returns a structured dict:
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
                nlp_data = section.get("nlp", {})
                vector = nlp_data.get("vector")


                # --- Generate vector if missing ---
                if vector is None:
                    text_to_embed = section.get("contenu", "")
                    if text_to_embed.strip():
                        vector = self.embedding_model.encode(text_to_embed).tolist()
                    else:
                        vector = None


                if vector is None:
                    continue


                # --- Match GDPR ---
                matches = self.match_section(vector, threshold=threshold, top_k=top_k)


                # --- Actual content for prompt ---
                if nlp_data.get("model") == "Perplexity" and "analysis" in nlp_data:
                    section_content = nlp_data["analysis"]
                else:
                    section_content = section.get("contenu", "")


                prompt_data[url]["sections"].append({
                    "type": section.get("type"),
                    "url_source": section.get("url_source"),
                    "content": section_content,
                    "matches": matches
                })


        return prompt_data


    def save_prompt_data(self, threshold=0.75, top_k=3) -> dict:
        return self.build_prompt_data(threshold=threshold, top_k=top_k)
    
    def __repr__(self):
        return f"SemanticMatcher(rgpd_data={self.rgpd_data}, site_data={self.site_data})"



if __name__ == "__main__":
    try:
        with open("rgpd_embeddings.json", "r", encoding="utf-8") as f:
            rgpd_embeddings = json.load(f)
        print(f"✅ GDPR embeddings loaded, count={len(rgpd_embeddings)}")
    except Exception as e:
        print(f"Error loading GDPR embeddings: {e}")
        rgpd_embeddings = None


    try:
        with open("nlp_output.json", "r", encoding="utf-8") as f:
            site_data = json.load(f)
        print("✅ NLP site data loaded")
    except Exception as e:
        print(f"Error loading NLP site data: {e}")
        site_data = None


    if rgpd_embeddings and site_data:
        matcher = SemanticMatcher(rgpd_data=rgpd_embeddings, site_data=site_data)
        prompt_data = matcher.build_prompt_data()


        print("=== Prompt data built ===")
        print(json.dumps(prompt_data, ensure_ascii=False, indent=2))


        with open("prompt_data.json", "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=2)
        print("✅ Prompt data saved in prompt_data.json")
    else:
        print("Missing data, stopping process.")