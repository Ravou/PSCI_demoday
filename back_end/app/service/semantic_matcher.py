import json
import torch
from sentence_transformers import util
from app.models.base_model import BaseModel

class SemanticMatcher(BaseModel):
    """
    Fait le matching sémantique entre sections d’un site et les embeddings RGPD.
    Retourne un dict prêt pour PromptGenerator ou stockage en base.
    """

    def __init__(self, rgpd_data: list, site_data: list):
        super().__init__()

        if rgpd_data is None:
            raise ValueError("Il faut passer les embeddings RGPD déjà chargé en mémoire")
        self.rgpd_data = rgpd_data

        # --- Chargement des données du site ---
        if site_data is None:
            raise ValueError("Il faut passer soit site_data contenant les donées du site")
        self.site_data = site_data

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

    def build_prompt_data(self, threshold: float = 0.75, top_k: int = 3) -> dict:
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

    def save_prompt_data(self, threshold=0.75, top_k=3) -> dict:
        return self.build_prompt_data(threshold=threshold, top_k=top_k)


if __name__ == "__main__":
    import json

    try:
        # Chargement manuel des embeddings RGPD depuis fichier (debug)
        with open("rgpd_embeddings.json", "r", encoding="utf-8") as f:
            rgpd_embeddings = json.load(f)
        print(f"✅ Embeddings RGPD chargés, count={len(rgpd_embeddings)}")
    except Exception as e:
        print(f"Erreur lors du chargement des embeddings RGPD: {e}")
        rgpd_embeddings = None

    try:
        # Chargement manuel des données NLP du site depuis fichier (debug)
        with open("nlp_output.json", "r", encoding="utf-8") as f:
            site_data = json.load(f)
        print("✅ Données NLP site chargées")
    except Exception as e:
        print(f"Erreur lors du chargement des données NLP site: {e}")
        site_data = None

    # S’assurer que les données nécessaires sont bien chargées
    if rgpd_embeddings and site_data:
        matcher = SemanticMatcher(rgpd_data=rgpd_embeddings, site_data=site_data)
        prompt_data = matcher.build_prompt_data()
        
        # Pour debug, on peut afficher ou sauver ce dict dans un fichier
        print("=== Prompt data construit ===")
        print(json.dumps(prompt_data, ensure_ascii=False, indent=2))
        
        # Exemple sauvegarde optionnelle (debug uniquement)
        with open("prompt_data.json", "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=2)
        print("✅ Données de prompt sauvegardées dans prompt_data.json")
    else:
        print("Données manquantes, arrêt du traitement.")
