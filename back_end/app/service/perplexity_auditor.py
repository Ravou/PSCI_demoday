import os
import re
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Any
from app.models.base_model import BaseModel

load_dotenv()

class PerplexityAuditor(BaseModel):
    """Audit RGPD via Perplexity, full mémoire (dict en entrée/sortie)."""

    MAX_MESSAGE_LENGTH = 3500  # Limite par message pour éviter 400

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ Variable d’environnement PERPLEXITY_API_KEY non trouvée !")

    def call_api(self, prompt_payload: Dict[str, Any]) -> str:
        """Appelle l’API Perplexity et retourne le texte brut."""
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Nettoyage & troncature pour éviter les erreurs 400
        for msg in prompt_payload.get("messages", []):
            msg["content"] = msg["content"].replace("\x0c", " ")
            if len(msg["content"]) > self.MAX_MESSAGE_LENGTH:
                msg["content"] = msg["content"][:self.MAX_MESSAGE_LENGTH] + "\n…[truncated]"

        try:
            response = requests.post(url, headers=headers, json=prompt_payload, timeout=90)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Erreur lors de l'appel API Perplexity : {e}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Erreur JSON inattendue depuis Perplexity : {response.text}")

        # Extraction sécurisée du contenu
        if "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
            return data["choices"][0]["message"]["content"].strip()

        raise RuntimeError("❌ Aucune réponse valide reçue de l'API.")

    def extract_json(self, text: str) -> Dict[str, Any]:
        """Extrait un JSON valide même si Perplexity renvoie un texte partiel ou bruité."""
        if not text:
            raise ValueError("❌ Réponse vide du modèle.")

        # Supprime les balises parasites
        clean_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

        # 1️⃣ Recherche de blocs ```json ... ```
        matches = re.findall(r"```(?:json)?\s*(.*?)\s*```", clean_text, re.DOTALL)
        candidate = None

        if matches:
            for block in matches:
                block = block.strip()
                if block.startswith("{") or block.startswith("["):
                    candidate = block
                    break

        # 2️⃣ Sinon, extraction du premier bloc JSON trouvé
        if not candidate:
            match = re.search(r"(\[.*?\]|\{.*?\})", clean_text, re.DOTALL)
            candidate = match.group(1) if match else None

        if not candidate:
            print("=== Réponse brute du modèle (aucun JSON trouvé) ===")
            print(clean_text[:500])
            raise ValueError("❌ Aucun JSON valide trouvé dans la réponse.")

        # 3️⃣ Nettoyage des caractères typographiques et spéciaux
        candidate = candidate.replace("“", '"').replace("”", '"').replace("’", "'")

        # 4️⃣ Si le JSON est tronqué → on coupe après le dernier '}' ou ']'
        last_bracket = max(candidate.rfind('}'), candidate.rfind(']'))
        if last_bracket != -1:
            candidate = candidate[:last_bracket + 1]

        # 5️⃣ Tentatives de parsing avec récupération
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as e:
            print("⚠️ JSON invalide, tentative de correction automatique...")
            # Supprime caractères non imprimables
            cleaned = ''.join(c for c in candidate if c.isprintable() or c in "\n\t ")
            # Retente le parsing jusqu’à la dernière fermeture de bloc
            partial = re.sub(r'[^}\]]+$', '', cleaned)
            try:
                return json.loads(partial)
            except Exception as e2:
                print("=== Réponse brute non parseable ===")
                print(text[:500])
                raise ValueError(f"❌ JSON invalide extrait : {e2}")

    def run(self, prompt_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute l'audit RGPD via Perplexity et retourne un dict prêt à stocker."""
        print("🚀 Lancement du PerplexityAuditor (full mémoire)...")
        response_text = self.call_api(prompt_payload)
        audit_json = self.extract_json(response_text)
        print("✅ Audit RGPD généré en mémoire.")
        return audit_json














