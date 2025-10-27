from typing import Optional, List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime
from app.models.user import User
from app.models.audit import Audit
from app.service.content_scraper import ContentScraper
from app.service.nlp_preprocessor import NLPPreprocessor
from app.service.semantic_matcher import SemanticMatcher
from app.service.prompt_generator import PromptGenerator
from app.service.perplexity_auditor import PerplexityAuditor
from sentence_transformers import SentenceTransformer

load_dotenv()

class Facade:
    def __init__(self):
        self.users: Dict[str, User] = {}          # id -> User
        self.audits: Dict[str, List[Audit]] = {}  # user_id -> List[Audit]
        self.temp_outputs: Dict[str, dict] = {}   # file_id/site -> étapes intermédiaires
        self.scraper = ContentScraper()
        self.nlp = NLPPreprocessor()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # ---------- Utilisateurs ----------
    def create_user(self, name: str, email: str, password: str, consent_ip: str) -> User:
        user = User(name=name, email=email, password=password, consent_ip=consent_ip)
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self.users.values() if u.email == email), None)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None

    def list_users(self) -> List[User]:
        return list(self.users.values())

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user(user_id)
        if user:
            user.delete_account(archive_consent=True)
            del self.users[user_id]
            return True
        return False

    # ---------- Données RGPD ----------
    def get_rgpd_data(self) -> dict:
        return {
            "consent": True,
            "timestamp": datetime.now().isoformat(),
            "policy_version": "1.0"
        }

    # ---------- Audits (with outputs memory) ----------
    def get_site_sections(self, site: str) -> List[dict]:
        return [{"type": "section_example", "content": "Contenu exemple"}]

    def save_output(self, file_id: str, output: dict):
        self.temp_outputs[file_id] = output

    def get_output(self, file_id: str) -> Optional[dict]:
        return self.temp_outputs.get(file_id)

    def create_audit(self, user_id: str, site: str, run_perplexity: bool = False) -> Optional[Audit]:
        user = self.get_user(user_id)
        if not user:
            return None

        rgpd_data = self.get_rgpd_data()
        sections = self.get_site_sections(site)

        # --- Scraping ---
        static_data = self.scraper.scrape_static(site)
        dynamic_data = self.scraper.scrape_dynamic(site)
        html_text = dynamic_data.get("html_text_snippet", "")

        # --- NLP ---
        nlp_output_texts = self.nlp.nlp_pipeline(html_text)
        enriched_sections = []
        for text in nlp_output_texts:
            vector = self.embedder.encode(text).tolist()
            enriched_sections.append({
                "type": "text",
                "url_source": site,
                "contenu": text,
                "nlp": {"vector": vector}
            })

        # --- Semantic Matching & Prompt ---
        semantic_matcher = SemanticMatcher(site_data=[{"url": site, "sections": enriched_sections}], rgpd_data=rgpd_data)
        prompt_data_dict = semantic_matcher.build_prompt_data()
        prompt_generator = PromptGenerator()
        prompt_payload = prompt_generator.generate_prompt(prompt_data_dict)

        # --- Appel Perplexity (optionnel) ---
        perplexity_report = None
        if run_perplexity:
            api_key = os.getenv("PERPLEXITY_API_KEY")
            if not api_key:
                print("⚠️ Aucune clé API Perplexity trouvée dans .env")
            else:
                auditor = PerplexityAuditor(api_key=api_key)
                perplexity_report = auditor.run(prompt_payload=prompt_payload)

        # --- Enregistrement output temporaire ---
        temp_id = f"{user_id}_{site}_{datetime.now().isoformat()}"
        self.save_output(temp_id, {
            "static": static_data,
            "dynamic": dynamic_data,
            "nlp_output": nlp_output_texts,
            "prompt_data": prompt_payload,
            "perplexity_report": perplexity_report
        })

        # --- Création & stockage objet Audit ---
        audit = Audit(
            user_id=user_id,
            site=site,
            content=self.temp_outputs[temp_id],
            timestamp=datetime.now()
        )
        self.audits.setdefault(user_id, []).append(audit)
        user.audits.append(audit)
        return audit

    def list_audits(self, user_id: str) -> List[Audit]:
        return self.audits.get(user_id, [])

    def get_audit(self, user_id: str, site: str) -> Optional[Audit]:
        return next((a for a in self.list_audits(user_id) if a.site == site), None)

# Instance globale
facade = Facade()