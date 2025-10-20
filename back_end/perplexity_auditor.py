import json
import os
import re
import requests
from app.models.base_model import BaseModel

class PerplexityAuditor(BaseModel):
    """
    Interagit avec l'API Perplexity pour générer un audit RGPD
    à partir d'un prompt JSON.
    """

    def __init__(self,
                 prompt_file="rgpd_prompt_to_model.json",
                 output_file="rgpd_audit_report.json",
                 api_key=None):
        super().__init__()
        self.prompt_file = prompt_file
        self.output_file = output_file
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ Variable d’environnement PERPLEXITY_API_KEY non trouvée !")

    def load_prompt(self) -> str:
        if not os.path.exists(self.prompt_file):
            raise FileNotFoundError(f"❌ Fichier introuvable : {self.prompt_file}")
        with open(self.prompt_file, "r", encoding="utf-8") as f:
            prompt_data = json.load(f)
        return prompt_data.get("prompt", "")

    def call_api(self, prompt_text: str) -> str:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "sonar-reasoning",
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 0.7,
            "max_tokens": 2048
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        raise RuntimeError("❌ Aucune réponse reçue de l'API Perplexity")

    def extract_json(self, text: str) -> dict:
        """Extrait un JSON même si Perplexity ajoute du texte ou des <think>"""
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if not match:
            print("=== Réponse brute du modèle ===")
            print(text)
            raise ValueError("❌ Aucun JSON trouvé dans la réponse")
        return json.loads(match.group(0))

    def save_audit(self, audit_json: dict):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(audit_json, f, ensure_ascii=False, indent=2)
        print(f"✅ Audit RGPD généré et sauvegardé dans : {self.output_file}")

    def run(self):
        """Exécute tout le pipeline"""
        print("🚀 Lancement du PerplexityAuditor...")
        prompt_text = self.load_prompt()
        response_text = self.call_api(prompt_text)
        audit_json = self.extract_json(response_text)
        self.save_audit(audit_json)
        return audit_json


if __name__ == "__main__":
    auditor = PerplexityAuditor()
    auditor.run()

