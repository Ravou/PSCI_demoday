import os
import re
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Any


load_dotenv()


class PerplexityAuditor:
    """GDPR audit via Perplexity, full memory (dict input/output)."""


    MAX_MESSAGE_LENGTH = 3500  # Limit per message to avoid 400 errors


    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ Environment variable PERPLEXITY_API_KEY not found!")


    def call_api(self, prompt_payload: Dict[str, Any]) -> str:
        """Calls the Perplexity API and returns raw text."""
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


        # Clean & truncate to avoid 400 errors
        for msg in prompt_payload.get("messages", []):
            msg["content"] = msg["content"].replace("\x0c", " ")
            if len(msg["content"]) > self.MAX_MESSAGE_LENGTH:
                msg["content"] = msg["content"][:self.MAX_MESSAGE_LENGTH] + "\n…[truncated]"


        try:
            response = requests.post(url, headers=headers, json=prompt_payload, timeout=90)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Error calling Perplexity API: {e}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Unexpected JSON error from Perplexity: {response.text}")


        # Safe extraction of content
        if "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
            return data["choices"][0]["message"]["content"].strip()


        raise RuntimeError("❌ No valid response received from API.")


    def extract_json(self, text: str) -> Dict[str, Any]:
        """Extracts valid JSON even if Perplexity returns partial or noisy text."""
        if not text:
            raise ValueError("❌ Empty model response.")


        # Remove parasitic tags
        clean_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


        # 1️⃣ Look for `````` blocks
        matches = re.findall(r"``````", clean_text, re.DOTALL)
        candidate = None


        if matches:
            for block in matches:
                block = block.strip()
                if block.startswith("{") or block.startswith("["):
                    candidate = block
                    break


        # 2️⃣ Otherwise, extract first JSON block found
        if not candidate:
            match = re.search(r"(\[.*?\]|\{.*?\})", clean_text, re.DOTALL)
            candidate = match.group(1) if match else None


        if not candidate:
            print("=== Raw model response (no JSON found) ===")
            print(clean_text[:500])
            raise ValueError("❌ No valid JSON found in response.")


        # 3️⃣ Clean typographic and special characters
        candidate = candidate.replace("“", '"').replace("”", '"').replace("’", "'")


        # 4️⃣ If JSON truncated → cut after last '}' or ']'
        last_bracket = max(candidate.rfind('}'), candidate.rfind(']'))
        if last_bracket != -1:
            candidate = candidate[:last_bracket + 1]


        # 5️⃣ Parsing attempts with recovery
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as e:
            print("⚠️ Invalid JSON, trying automatic correction...")
            # Remove non-printable characters
            cleaned = ''.join(c for c in candidate if c.isprintable() or c in "\n\t ")
            # Retry parsing up to last closing block
            partial = re.sub(r'[^}\]]+$', '', cleaned)
            try:
                return json.loads(partial)
            except Exception as e2:
                print("=== Unparsable raw response ===")
                print(text[:500])
                raise ValueError(f"❌ Extracted invalid JSON: {e2}")


    def run(self, prompt_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the GDPR audit via Perplexity and returns a dict ready for storage."""
        print("🚀 Starting PerplexityAuditor (full memory)...")
        response_text = self.call_api(prompt_payload)
        audit_json = self.extract_json(response_text)
        print("✅ GDPR audit generated in memory.")
        return audit_json
    
    def __repr__(self):
        return f"PerplexityAuditor(url='{self.url}', hostname='{self.hostname}')"















