"""
Content Scraper - Extraction et parsing de contenu HTML

Ce module permet de :
- Parser le HTML avec BeautifulSoup
- Extraire le texte visible
- Identifier les scripts de tracking (Google Analytics, Facebook Pixel, etc.)
- Détecter les formulaires de collecte de données
- Extraire les liens de politique de confidentialité
"""

from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re
from urllib.parse import urljoin, urlparse

class ContentScraper:
    """
    Scraper pour extraire le contenu structuré d'une page HTML
    """
    
    def __init__(self):
        """Initialise le scraper"""
        # Patterns pour détecter les trackers courants
        self.tracker_patterns = {
            'google_analytics': r'google-analytics\.com|googletagmanager\.com|analytics\.js',
            'facebook_pixel': r'connect\.facebook\.net|fbq\(|facebook\.com/tr',
            'hotjar': r'hotjar\.com',
            'matomo': r'matomo\.js|piwik\.js',
            'linkedin': r'snap\.licdn\.com',
            'twitter': r'analytics\.twitter\.com',
            'tiktok': r'analytics\.tiktok\.com',
            'criteo': r'criteo\.com',
            'doubleclick': r'doubleclick\.net',
            'adroll': r'adroll\.com'
        }
    
    def parse_html(self, html: str, base_url: str = None) -> Dict:
        """
        Parse le HTML et extrait toutes les informations pertinentes
        
        Args:
            html: Contenu HTML à parser
            base_url: URL de base pour résoudre les liens relatifs
            
        Returns:
            Dictionnaire avec le contenu structuré
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        return {
            'title': self._extract_title(soup),
            'meta_description': self._extract_meta(soup, 'description'),
            'text_content': self._extract_visible_text(soup),
            'scripts': self._extract_scripts(soup),
            'trackers': self._detect_trackers(html),
            'forms': self._extract_forms(soup),
            'links': self._extract_links(soup, base_url),
            'privacy_policy_link': self._find_privacy_policy(soup, base_url),
            'cookies_mentioned': self._check_cookies_mention(soup),
            'rgpd_keywords': self._find_rgpd_keywords(soup)
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le titre de la page"""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else None
    
    def _extract_meta(self, soup: BeautifulSoup, name: str) -> Optional[str]:
        """Extrait une balise meta"""
        meta = soup.find('meta', attrs={'name': name})
        return meta.get('content') if meta else None
    
    def _extract_visible_text(self, soup: BeautifulSoup) -> str:
        """
        Extrait le texte visible (sans scripts, styles, etc.)
        """
        # Supprime scripts, styles, etc.
        for element in soup(['script', 'style', 'meta', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()
        
        # Récupère le texte
        text = soup.get_text(separator=' ', strip=True)
        
        # Nettoie les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _extract_scripts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait tous les scripts (externes et inline)"""
        scripts = []
        
        for script in soup.find_all('script'):
            script_data = {
                'type': 'external' if script.get('src') else 'inline',
                'src': script.get('src'),
                'content': script.string if script.string else None
            }
            scripts.append(script_data)
        
        return scripts
    
    def _detect_trackers(self, html: str) -> Dict[str, bool]:
        """Détecte les trackers présents dans le HTML"""
        trackers_found = {}
        
        for tracker_name, pattern in self.tracker_patterns.items():
            trackers_found[tracker_name] = bool(re.search(pattern, html, re.IGNORECASE))
        
        return trackers_found
    
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait les formulaires (collecte de données potentielle)"""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action'),
                'method': form.get('method', 'GET').upper(),
                'inputs': []
            }
            
            # Extrait les champs du formulaire
            for input_field in form.find_all(['input', 'textarea', 'select']):
                field_data = {
                    'type': input_field.get('type', 'text'),
                    'name': input_field.get('name'),
                    'id': input_field.get('id'),
                    'required': input_field.has_attr('required')
                }
                form_data['inputs'].append(field_data)
            
            forms.append(form_data)
        
        return forms
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str = None) -> List[str]:
        """Extrait tous les liens de la page"""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Résout les liens relatifs si base_url fournie
            if base_url and not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                href = urljoin(base_url, href)
            
            links.append(href)
        
        return list(set(links))  # Supprime doublons
    
    def _find_privacy_policy(self, soup: BeautifulSoup, base_url: str = None) -> Optional[str]:
        """Trouve le lien vers la politique de confidentialité"""
        privacy_keywords = [
            'politique de confidentialité', 'privacy policy', 'données personnelles',
            'mentions légales', 'rgpd', 'vie privée', 'confidentialité'
        ]
        
        for link in soup.find_all('a', href=True):
            link_text = link.get_text(strip=True).lower()
            link_href = link['href'].lower()
            
            for keyword in privacy_keywords:
                if keyword in link_text or keyword in link_href:
                    href = link['href']
                    if base_url and not href.startswith(('http://', 'https://')):
                        href = urljoin(base_url, href)
                    return href
        
        return None
    
    def _check_cookies_mention(self, soup: BeautifulSoup) -> bool:
        """Vérifie si les cookies sont mentionnés sur la page"""
        text = soup.get_text().lower()
        cookie_keywords = ['cookie', 'cookies', 'traceur', 'traceurs']
        
        return any(keyword in text for keyword in cookie_keywords)
    
    def _find_rgpd_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Trouve les mots-clés RGPD présents sur la page"""
        text = soup.get_text().lower()
        
        rgpd_keywords = [
            'rgpd', 'gdpr', 'cnil', 'consentement', 'données personnelles',
            'vie privée', 'droit à l\'oubli', 'portabilité', 'dpo',
            'responsable de traitement', 'sous-traitant'
        ]
        
        found_keywords = [kw for kw in rgpd_keywords if kw in text]
        return found_keywords


# Instance globale du scraper
scraper = ContentScraper()


def scrape_html(html: str, base_url: str = None) -> Dict:
    """
    Fonction utilitaire pour scraper du HTML
    
    Args:
        html: HTML à scraper
        base_url: URL de base
        
    Returns:
        Contenu structuré
    """
    return scraper.parse_html(html, base_url)


# Test si exécuté directement
if __name__ == "__main__":
    # HTML de test
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Site de Test RGPD</title>
        <meta name="description" content="Exemple de site pour test">
        <script src="https://www.google-analytics.com/analytics.js"></script>
        <script>
            fbq('track', 'PageView');
        </script>
    </head>
    <body>
        <h1>Bienvenue sur notre site</h1>
        <p>Nous utilisons des cookies pour améliorer votre expérience.</p>
        <p>Consultez notre politique de confidentialité pour en savoir plus.</p>
        
        <form action="/subscribe" method="POST">
            <input type="email" name="email" required>
            <input type="text" name="name">
            <button type="submit">S'inscrire</button>
        </form>
        
        <a href="/privacy">Politique de confidentialité</a>
        <a href="/rgpd">Informations RGPD</a>
        
        <script src="https://connect.facebook.net/fr_FR/fbevents.js"></script>
    </body>
    </html>
    """
    
    print("=" * 70)
    print("TEST CONTENT SCRAPER")
    print("=" * 70)
    
    result = scraper.parse_html(test_html, "https://example.com")
    
    print(f"\nTitre          : {result['title']}")
    print(f"Meta desc      : {result['meta_description']}")
    print(f"Cookies mentionnés : {result['cookies_mentioned']}")
    print(f"\nTrackers détectés :")
    for tracker, found in result['trackers'].items():
        if found:
            print(f"  ✓ {tracker}")
    
    print(f"\nFormuaires trouvés : {len(result['forms'])}")
    for i, form in enumerate(result['forms'], 1):
        print(f"  Formulaire {i} : {len(form['inputs'])} champs")
    
    print(f"\nLien privacy policy : {result['privacy_policy_link']}")
    print(f"\nMots-clés RGPD : {', '.join(result['rgpd_keywords'])}")