import os
import threading
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional, List, Dict

from app.models.user import User
from app.models.audit import Audit
from app.persistence.repository import UserRepository, AuditRepository
from app.service.content_scraper import ContentScraper
from app.service.nlp_preprocessor import NLPPreprocessor
from app.service.semantic_matcher import SemanticMatcher
from app.service.prompt_generator import PromptGenerator
from app.service.perplexity_auditor import PerplexityAuditor
from app.service.extraction_docs import GDPRScraper
from app.service.rgpd_updater import RGPDUpdater
from sentence_transformers import SentenceTransformer
import schedule
import time

load_dotenv()


class Facade:
    def __init__(self):
        # Repositories SQLAlchemy
        self.user_repo = UserRepository()
        self.audit_repo = AuditRepository()

        # Services
        self.scraper = ContentScraper()
        self.nlp = NLPPreprocessor()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # RGPD
        self.gdpr_scraper = GDPRScraper()
        self.rgpd_updater = RGPDUpdater()

        # Stockage temporaire outputs
        self.temp_outputs: Dict[str, dict] = {}

        # Scheduler RGPD hebdomadaire
        self.start_rgpd_scheduler()

    # =======================================================
    # UTILISATEURS
    # =======================================================
    def create_user(self, name: str, email: str, password: str, consent_ip: str, is_admin: bool = False) -> dict:
        user = self.user_repo.create(name, email, password, consent_ip, is_admin)
        return user.to_dict()

    def get_user(self, user_id: str) -> Optional[dict]:
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.user_repo.get_by_email(email)
        return user.to_dict() if user else None

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Vérifie email + password et retourne dict si correct"""
        user = self.user_repo.get_by_email(email)
        if user and user.verify_password(password):
            return user.to_dict()
        return None

    def list_users(self) -> List[dict]:
        users = self.user_repo.get_all()
        return [u.to_dict() for u in users]

    def delete_user(self, user_id: str, archive_consent: bool = True) -> bool:
        return self.user_repo.delete_user(user_id, archive_consent=archive_consent)

    # =======================================================
    # RGPD
    # =======================================================
    def update_rgpd(self):
        """Vérifie et met à jour les données RGPD si nécessaire"""
        if self.gdpr_scraper.check_update():
            self.gdpr_scraper.scrape()
            self.rgpd_updater.update_rgpd()
        else:
            print("✅ RGPD déjà à jour")

    def get_rgpd_data(self) -> dict:
        """Retourne les données RGPD pour les audits ou analyses"""
        return {
            "consent": True,
            "timestamp": datetime.now().isoformat(),
            "policy_version": "1.0"
        }

    def start_rgpd_scheduler(self):
        """Lance un thread pour vérifier le RGPD chaque lundi à 09:00"""
        schedule.every().monday.at("09:00").do(self.update_rgpd)

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()

    # =======================================================
    # SECTIONS DU SITE
    # =======================================================
    def get_site_sections(self, site: str) -> List[dict]:
        return [{"type": "section_example", "content": "Contenu exemple"}]

    # =======================================================
    # GESTION DES OUTPUTS TEMPORAIRES
    # =======================================================
    def save_output(self, file_id: str, output: dict):
        self.temp_outputs[file_id] = output

    def get_output(self, file_id: str) -> Optional[dict]:
        return self.temp_outputs.get(file_id)

    # =======================================================
    # AUDITS
    # =======================================================
    def create_audit(self, user_id: str, site: str, run_perplexity: bool = False) -> Optional[dict]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Mise à jour RGPD avant l’audit
        self.update_rgpd()
        rgpd_data = self.get_rgpd_data()

        # --- Scraping ---
        static_data = self.scraper.scrape_static(site)
        dynamic_data = self.scraper.scrape_dynamic(site)
        html_text = dynamic_data.get("html_text_snippet", "")

        # --- NLP local / embeddings ---
        nlp_output = self.nlp.nlp_pipeline(html_text)
        enriched_sections = []

        if isinstance(nlp_output, dict) and "analysis" in nlp_output:
            enriched_sections.append({
                "type": "text",
                "url_source": site,
                "contenu": nlp_output["analysis"],
                "nlp": {"vector": []}
            })
        else:
            for text in nlp_output.get("snippets", [html_text]):
                vector = self.embedder.encode(text).tolist()
                enriched_sections.append({
                    "type": "text",
                    "url_source": site,
                    "contenu": text,
                    "nlp": {"vector": vector}
                })

        # --- Semantic Matching & Prompt ---
        semantic_matcher = SemanticMatcher(
            site_data=[{"url": site, "sections": enriched_sections}],
            rgpd_data=rgpd_data
        )
        prompt_data_dict = semantic_matcher.build_prompt_data()
        prompt_generator = PromptGenerator()
        prompt_payload = prompt_generator.generate_prompt(prompt_data_dict)

        # --- Appel Perplexity (optionnel) ---
        perplexity_report = None
        if run_perplexity:
            api_key = os.getenv("PERPLEXITY_API_KEY")
            if api_key:
                auditor = PerplexityAuditor(api_key=api_key)
                perplexity_report = auditor.run(prompt_payload=prompt_payload)
            else:
                print("⚠️ Aucune clé API Perplexity trouvée dans .env")

        # --- Enregistrement output temporaire ---
        temp_id = f"{user_id}_{site}_{datetime.now().isoformat()}"
        self.save_output(temp_id, {
            "static": static_data,
            "dynamic": dynamic_data,
            "nlp_output": nlp_output,
            "prompt_data": prompt_payload,
            "perplexity_report": perplexity_report
        })

        # --- Création & stockage Audit dans DB via repository ---
        audit = self.audit_repo.create(
            user_id=user_id,
            site=site,
            content=self.temp_outputs[temp_id],
            timestamp=datetime.now()
        )

        return audit.to_dict() if audit else None

    def list_audits(self, user_id: str) -> List[dict]:
        audits = self.audit_repo.list_by_user(user_id)
        return [a.to_dict() for a in audits]

    def get_audit(self, user_id: str, site: str) -> Optional[dict]:
        audit = self.audit_repo.get_by_user_and_site(user_id, site)
        return audit.to_dict() if audit else None


# =======================================================
# INSTANCE GLOBALE
# =======================================================
facade = Facade()