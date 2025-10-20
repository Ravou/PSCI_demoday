import json
import re
import time
from jsonschema import validate, ValidationError
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# =======================
# Schéma de validation JSON
# =======================
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "checklist_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "checklist_item": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["✅ Conforme", "⚠️ Partiellement", "❌ Non conforme", "Non détecté"]
                    },
                    "evidence": {"type": "string"},
                    "recommendation": {"type": "string"}
                },
                "required": ["checklist_item", "status", "evidence", "recommendation"]
            }
        },
        "score": {"type": "integer"}
    },
    "required": ["checklist_items", "score"]
}


# =======================
# Classe principale
# =======================
class AIReport:
    MAX_CHUNK_LENGTH = 1200

    def __init__(self,
                 audit_json_path="rgpd_prompt_to_model.json",
                 model_name="microsoft/phi-3-mini-4k-instruct"):
        self.audit_json_path = audit_json_path
        self.model_name = model_name
        self.audit_data = self.load_prompt_data()

        print(f"⏳ Chargement du modèle Hugging Face : {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            offload_folder="offload"
        )

    # -----------------------
    # Chargement du prompt
    # -----------------------
    def load_prompt_data(self):
        try:
            with open(self.audit_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("prompt", "")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du prompt : {e}")
            return ""

    # -----------------------
    # Validation JSON
    # -----------------------
    def validate_json(self, data):
        try:
            validate(instance=data, schema=JSON_SCHEMA)
            return True
        except ValidationError as e:
            print(f"⚠️ Erreur de validation JSON : {e.message}")
            return False

    # -----------------------
    # Extraction JSON
    # -----------------------
    def extract_json_from_text(self, text):
        try:
            match = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.DOTALL)
        except re.error:
            match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            cleaned = match.group().replace("'", '"').replace("\n", " ").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None

    # -----------------------
    # Découpage du prompt
    # -----------------------
    def chunk_prompt(self):
        prompt = self.audit_data.strip()
        chunks = []
        for i in range(0, len(prompt), self.MAX_CHUNK_LENGTH):
            chunks.append(prompt[i:i + self.MAX_CHUNK_LENGTH])
        return chunks

    # -----------------------
    # Appel du modèle
    # -----------------------
    def query_model(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=800, temperature=0.3)
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text

    # -----------------------
    # Génération IA avec relance
    # -----------------------
    def generate_audit_with_ai(self, max_retries=3, delay_sec=2):
        if not self.audit_data.strip():
            print("⚠️ Aucun prompt trouvé, génération impossible.")
            return {"checklist_items": [], "score": 0}

        chunks = self.chunk_prompt()
        final_items = []

        for chunk_idx, chunk in enumerate(chunks):
            print(f"\n🧩 Génération chunk {chunk_idx + 1}/{len(chunks)}...")

            for attempt in range(max_retries):
                generated = self.query_model(chunk)

                print("\n🧠 --- TEXTE GÉNÉRÉ PAR LE MODÈLE ---")
                print(generated)
                print("--------------------------------------")

                chunk_json = self.extract_json_from_text(generated)
                if chunk_json and "checklist_items" in chunk_json:
                    final_items.extend(chunk_json["checklist_items"])
                    break
                else:
                    print(f"⚠️ JSON invalide pour ce chunk, tentative {attempt + 1}/{max_retries}...")
                    time.sleep(delay_sec)
            else:
                print(f"❌ Échec sur chunk {chunk_idx + 1}, ajout vide.")

        total = len(final_items)
        conformes = sum(1 for i in final_items if i.get("status") == "✅ Conforme")
        score = int(conformes / max(total, 1) * 100)

        print(f"\n📝 Score calculé : {score}%")
        return {"checklist_items": final_items, "score": score}

    # -----------------------
    # Affichage terminal
    # -----------------------
    def generate_json(self):
        audit_result = self.generate_audit_with_ai()
        print("\n📄 === RAPPORT JSON FINAL ===")
        print(json.dumps(audit_result, ensure_ascii=False, indent=4))
        print("=============================\n")
        return audit_result


# -----------------------
# Exécution directe
# -----------------------
if __name__ == "__main__":
    report = AIReport()
    report.generate_json()











