"""
Modèle Audit - Gestion des audits RGPD
"""

from datetime import datetime
import json

# Ne pas importer db ici, il sera injecté via models.__init__.py
def init_audit_model(db):
    """
    Créer le modèle Audit avec l'instance db
    Cette fonction est appelée après l'initialisation de db
    """
    
    class Audit(db.Model):
        """Modèle Audit pour stocker les audits RGPD"""
        __tablename__ = 'audits'

        id = db.Column(db.String(50), primary_key=True)
        target = db.Column(db.String(500), nullable=False)
        status = db.Column(db.String(50), default='pending')
        score = db.Column(db.Float, default=0.0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        violations = db.Column(db.Text)
        recommendations = db.Column(db.Text)
        details = db.Column(db.Text)
        
        user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
        consent_id = db.Column(db.String(50), db.ForeignKey('consents.id'))
        
        def __repr__(self):
            return f'<Audit {self.id} - {self.target}>'
        
        def to_dict(self):
            return {
                'id': self.id,
                'target': self.target,
                'status': self.status,
                'score': self.score,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                'user_id': self.user_id,
                'consent_id': self.consent_id
            }
        
        def run_audit(self):
            """Exécute l'audit RGPD complet"""
            # Import ici pour éviter imports circulaires
            from app.services.web_crawler import WebCrawler
            from app.services.content_scraper import ContentScraper
            from app.services.nlp_preprocessor import NLPPreprocessor
            
            try:
                crawler = WebCrawler()
                crawl_result = crawler.fetch_page(self.target)
                
                if not crawl_result['success']:
                    self.status = 'failed'
                    self.details = json.dumps({'error': crawl_result['error']})
                    db.session.commit()
                    return {'success': False, 'error': crawl_result['error']}
                
                scraper = ContentScraper()
                scrape_result = scraper.parse_html(crawl_result['html'], self.target)
                
                preprocessor = NLPPreprocessor()
                nlp_result = preprocessor.analyze_text(scrape_result['text_content'][:5000])
                
                score, violations, recommendations = self._calculate_compliance_score(
                    crawl_result, scrape_result, nlp_result
                )
                
                self.score = score
                self.status = 'completed'
                self.violations = json.dumps(violations, ensure_ascii=False)
                self.recommendations = json.dumps(recommendations, ensure_ascii=False)
                self.details = json.dumps({
                    'crawl': {
                        'cookies': crawl_result.get('cookies', []),
                        'status_code': crawl_result.get('status_code'),
                        'elapsed_time': crawl_result.get('elapsed_time')
                    },
                    'scrape': {
                        'title': scrape_result.get('title'),
                        'trackers': scrape_result.get('trackers', {}),
                        'forms_count': len(scrape_result.get('forms', [])),
                        'privacy_policy_link': scrape_result.get('privacy_policy_link'),
                        'cookies_mentioned': scrape_result.get('cookies_mentioned', False),
                        'rgpd_keywords': scrape_result.get('rgpd_keywords', [])
                    },
                    'nlp': {
                        'has_sensitive_data': nlp_result.get('has_sensitive_data', False),
                        'has_personal_data': nlp_result.get('has_personal_data', False),
                        'entities': nlp_result.get('entities', {}),
                        'sensitive_data': nlp_result.get('sensitive_data', {})
                    }
                }, ensure_ascii=False)
                
                db.session.commit()
                
                return {
                    'success': True,
                    'score': score,
                    'violations': violations,
                    'recommendations': recommendations
                }
            
            except Exception as e:
                self.status = 'failed'
                self.details = json.dumps({'error': str(e)})
                db.session.commit()
                return {'success': False, 'error': str(e)}
        
        def _calculate_compliance_score(self, crawl_result, scrape_result, nlp_result):
            """Calcule le score de conformité RGPD"""
            score = 100.0
            violations = []
            recommendations = []
            
            if not scrape_result.get('privacy_policy_link'):
                score -= 30
                violations.append({
                    'article': 'Article 13 RGPD',
                    'description': 'Absence de politique de confidentialité',
                    'severity': 'high',
                    'category': 'transparency'
                })
                recommendations.append({
                    'title': 'Ajouter une politique de confidentialité',
                    'description': 'Créez une politique accessible',
                    'priority': 'high'
                })
            
            if not scrape_result.get('cookies_mentioned'):
                score -= 20
                violations.append({
                    'article': 'Article 5(3) ePrivacy',
                    'description': 'Pas d\'information cookies',
                    'severity': 'high',
                    'category': 'cookies'
                })
                recommendations.append({
                    'title': 'Informer sur les cookies',
                    'description': 'Ajoutez une bannière cookies',
                    'priority': 'high'
                })
            
            trackers_found = [name for name, found in scrape_result.get('trackers', {}).items() if found]
            if trackers_found and not scrape_result.get('cookies_mentioned'):
                score -= 20
                violations.append({
                    'article': 'Article 7 RGPD',
                    'description': f'Trackers sans consentement: {", ".join(trackers_found)}',
                    'severity': 'critical',
                    'category': 'consent'
                })
                recommendations.append({
                    'title': 'Consentement trackers',
                    'description': 'Implémentez une CMP',
                    'priority': 'critical'
                })
            
            if nlp_result.get('has_sensitive_data'):
                score -= 15
                violations.append({
                    'article': 'Article 32 RGPD',
                    'description': 'Données sensibles détectées',
                    'severity': 'medium',
                    'category': 'security'
                })
                recommendations.append({
                    'title': 'Protéger données sensibles',
                    'description': 'Masquez les données personnelles',
                    'priority': 'medium'
                })
            
            if not scrape_result.get('rgpd_keywords'):
                score -= 15
                violations.append({
                    'article': 'Article 12 RGPD',
                    'description': 'Pas d\'info RGPD',
                    'severity': 'medium',
                    'category': 'transparency'
                })
                recommendations.append({
                    'title': 'Informer droits RGPD',
                    'description': 'Mentionnez les droits',
                    'priority': 'medium'
                })
            
            score = max(0, score)
            return score, violations, recommendations
        
        def get_summary(self):
            """Retourne résumé de l'audit"""
            return {
                'audit_id': self.id,
                'target': self.target,
                'status': self.status,
                'score': self.score,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'violations': json.loads(self.violations) if self.violations else [],
                'recommendations': json.loads(self.recommendations) if self.recommendations else [],
                'details': json.loads(self.details) if self.details else {}
            }
    
    return Audit


# Création du modèle (sera appelé par __init__.py)
from app.models import db
Audit = init_audit_model(db)