from typing import Optional, List, Dict
from datetime import datetime
from app.models.user import User
from app.models.audit import Audit
from app.service.content_scraper import ContentScraper
from app.service.nlp_preprocessor import NLPPreprocessor
from app.service.semantic_matcher import SemanticMatcher
from app.service.prompt_generator import PromptGenerator  # full mémoire
from app.service.perplexity_auditor import PerplexityAuditor  # full mémoire
from sentence_transformers import SentenceTransformer

class Facade:
    def __init__(self):
        self.users: Dict[str, User] = {}          # id -> User
        self.audits: Dict[str, List[Audit]] = {}  # user_id -> List[Audit]
        self.scraper = ContentScraper()
        self.nlp = NLPPreprocessor()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # embeddings pour SemanticMatcher

    # -------------------------------
    # Gestion des utilisateurs
    # -------------------------------
    def create_user(self, name: str, email: str, password: str, consent_ip: str) -> User:
        user = User(name=name, email=email, password=password, consent_ip=consent_ip)
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def list_users(self) -> List[User]:
        return list(self.users.values())

    # -------------------------------
    # Gestion des audits
    # -------------------------------
    def create_audit(self, user_id: str, site: str, api_key: Optional[str] = None) -> Optional[Audit]:
        user = self.get_user(user_id)
        if not user:
            return None

        # --- Scraping ---
        static_data = self.scraper.scrape_static(site)
        dynamic_data = self.scraper.scrape_dynamic(site)
        html_text = dynamic_data.get("html_text_snippet", "")

        # --- NLP ---
        nlp_output_texts = self.nlp.nlp_pipeline(html_text)
        sections = []
        for text in nlp_output_texts:
            vector = self.embedder.encode(text).tolist()
            sections.append({
                "type": "text",
                "url_source": site,
                "contenu": text,
                "nlp": {"vector": vector}
            })

        # --- Semantic Matching ---
        semantic_matcher = SemanticMatcher(site_data=[{"url": site, "sections": sections}])
        prompt_data_dict = semantic_matcher.build_prompt_data()

        # --- Génération du prompt full mémoire ---
        prompt_generator = PromptGenerator()
        prompt_payload = prompt_generator.generate_prompt(prompt_data_dict)

        # --- Appel Perplexity full mémoire ---
        perplexity_report = None
        if api_key:
            auditor = PerplexityAuditor(api_key=api_key)
            perplexity_report = auditor.run(prompt_payload=prompt_payload)

        # --- Création de l'objet Audit ---
        audit = Audit(
            user_id=user_id,
            site=site,
            content={
                "static": static_data,
                "dynamic": dynamic_data,
                "nlp_output": nlp_output_texts,
                "prompt_data": prompt_payload,
                "perplexity_report": perplexity_report
            },
            timestamp=datetime.now()
        )

        # --- Stockage en mémoire ---
        self.audits.setdefault(user_id, []).append(audit)
        user.audits.append(audit)

        return audit

    def list_audits(self, user_id: str) -> List[Audit]:
        return self.audits.get(user_id, [])

    def get_audit(self, user_id: str, site: str) -> Optional[Audit]:
        for audit in self.list_audits(user_id):
            if audit.site == site:
                return audit
        return None

# Instance globale
facade = Facade()







