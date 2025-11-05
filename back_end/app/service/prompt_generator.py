import json
from typing import Dict, Any, List


class PromptGenerator:
    """Generates a GDPR prompt compatible with the Perplexity API."""


    MAX_CONTENT_LENGTH = 8000  # max length of the full prompt
    MAX_SECTION_LENGTH = 600   # max length per text section


    def __init__(self):
        self.output_prompt = None
        self.gdpr_points = [
            "Cookies and trackers",
            "Privacy policy",
            "Legal notices",
            "Forms and consents",
            "Security and transfers",
            "Minors",
            "Documentation",
            "Final report",
        ]


    @staticmethod
    def clean_text(text: Any) -> str:
        """Cleans text by removing non-printable characters."""
        if not isinstance(text, str):
            text = str(text)
        return ''.join(c if 32 <= ord(c) <= 126 else ' ' for c in text)


    def dict_to_list(self, site_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Converts a dict {url: {...}} into a list [{url, sections}] compatible with API,
           cleaning and truncating each section."""
        result = []
        for url, content in site_dict.items():
            sections = content.get("sections", [])
            truncated_sections = []
            for s in sections:
                s_clean = self.clean_text(s)
                if len(s_clean) > self.MAX_SECTION_LENGTH:
                    cutoff = s_clean.rfind(' ', 0, self.MAX_SECTION_LENGTH)
                    cutoff = cutoff if cutoff > 0 else self.MAX_SECTION_LENGTH
                    s_clean = s_clean[:cutoff] + "..."
                truncated_sections.append(s_clean)
            result.append({
                "url": self.clean_text(url),
                "sections": truncated_sections
            })
        return result


    def generate_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a structured prompt in the format expected by Perplexity API."""
        if not isinstance(prompt_data, dict):
            raise TypeError("❌ prompt_data must be a dict.")


        prompt_data_list = self.dict_to_list(prompt_data)
        site_json = json.dumps(prompt_data_list, ensure_ascii=False)


        # Construct prompt text with escaped quotes in JSON example
        format_json_example = (
            '[{{"point": "Name of GDPR point", '
            '"status": "compliant | partially compliant | non compliant | not detected", '
            '"evidence": "Short excerpt justifying the assessment", '
            '"recommendation": "Simple and concrete recommendation", '
            '"articles": "Legal articles referenced"}}]'
        )


        prompt_text = (
            "⚠️ Respond only with valid JSON.\n"
            "You are a GDPR auditor tasked to assess a website.\n"
            "Analyze the following excerpts and assign an assessment for each GDPR point.\n"
            "Expected response format: JSON list.\n\n"
            f"Site excerpts: {site_json}\n\n"
            f"GDPR points to evaluate: {', '.join(self.gdpr_points)}\n\n"
            f"Expected JSON format: {format_json_example}"
        )


        if len(prompt_text) > self.MAX_CONTENT_LENGTH:
            prompt_text = prompt_text[:self.MAX_CONTENT_LENGTH] + "\n…[truncated]"


        self.output_prompt = {
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "You are an AI assistant specialized in GDPR compliance."},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.2,
            "max_tokens": 1500
        }


        print("✅ Prompt generated successfully, ready for Perplexity.")
        return self.output_prompt



if __name__ == "__main__":
    pg = PromptGenerator()
    example_data = {
        "https://example.com": {
            "sections": [
                "Here is a GDPR content example with cookies.",
                "Another section explaining the privacy policy."
            ]
        }
    }
    prompt = pg.generate_prompt(example_data)
    print(json.dumps(prompt, indent=2, ensure_ascii=False))


    def __repr__(self):
        return f"PromptGenerator(url='{self.url}', hostname='{self.hostname}')"

