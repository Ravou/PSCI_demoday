# app/service/perplexity_auditor_mem.py
import json
import os
import re
import requests
from dotenv import load_dotenv
from app.models.base_model import BaseModel

# Charger clé API
load_dotenv()

class PerplexityAuditor(BaseModel):
    """Audit RGPD via Perplexity, full mémoire (dict en entrée/sortie)."""

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ Variable d’environnement PERPLEXITY_API_KEY non trouvée !")

    def call_api(self, prompt_payload: dict) -> str:
        """Appelle directement l’API Perplexity avec le dict en mémoire."""
        url = "https://api.perplexity.ai/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": prompt_payload.get("model", "sonar-medium-chat"),
            "messages": prompt_payload.get("messages", []),
            "temperature": 0.5,
            "max_tokens": 2048,
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
            return data["choices"][0]["message"]["content"].strip()

        print("=== Réponse brute API ===")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        raise RuntimeError("❌ Aucune réponse valide reçue de l'API.")

    def extract_json(text: str) -> dict:
        """Extrait le JSON de la réponse de façon plus robuste."""
        # Recherche la première accolade ouvrante ou crochet
        start = text.find('{')
        end = text.rfind('}') + 1

        if start == -1 or end == -1:
            start = text.find('[')
            end = text.rfind(']') + 1

        if start == -1 or end == -1:
            print("=== Réponse brute du modèle ===")
            print(text)
            raise ValueError("❌ Aucun JSON valide trouvé dans la réponse.")

        json_str = text[start:end]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("=== JSON extrait mais invalide ===")
            print(json_str)
            raise ValueError(f"❌ JSON invalide : {e}")

    def run(self, prompt_payload: dict) -> dict:
        """Pipeline complet, tout en mémoire."""
        print("🚀 Lancement du PerplexityAuditor (full mémoire)...")
        response_text = self.call_api(prompt_payload)
        audit_json = self.extract_json(response_text)
        print("✅ Audit RGPD généré en mémoire.")
        return audit_json















