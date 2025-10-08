"""
Web Crawler - Récupération du contenu HTML d'un site web

Ce module permet de :
- Récupérer le HTML d'une page web
- Gérer les erreurs de connexion
- Simuler un navigateur réel (User-Agent)
- Extraire les cookies et trackers
"""

import requests
from typing import Dict, Optional
from fake_useragent import UserAgent
import time

class WebCrawler:
    """
    Crawler pour récupérer le contenu HTML d'un site
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialise le crawler
        
        Args:
            timeout: Temps d'attente max pour une requête (secondes)
        """
        self.timeout = timeout
        self.session = requests.Session()
        
        # User-Agent pour simuler un navigateur réel
        try:
            ua = UserAgent()
            self.user_agent = ua.chrome
        except:
            # Fallback si fake_useragent ne fonctionne pas
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def fetch_page(self, url: str) -> Dict:
        """
        Récupère le contenu HTML d'une page
        
        Args:
            url: URL de la page à récupérer
            
        Returns:
            Dictionnaire avec le HTML, les cookies, headers, etc.
        """
        try:
            # Ajoute https:// si manquant
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fait la requête
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()  # Lève une exception si erreur HTTP
            
            # Récupère les cookies
            cookies = [
                {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'secure': cookie.secure
                }
                for cookie in self.session.cookies
            ]
            
            return {
                'success': True,
                'url': response.url,  # URL finale (après redirections)
                'status_code': response.status_code,
                'html': response.text,
                'headers': dict(response.headers),
                'cookies': cookies,
                'encoding': response.encoding,
                'elapsed_time': response.elapsed.total_seconds(),
                'error': None
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'url': url,
                'error': 'Timeout - Le site met trop de temps à répondre'
            }
        
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'url': url,
                'error': 'Erreur de connexion - Impossible de joindre le site'
            }
        
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'url': url,
                'status_code': e.response.status_code,
                'error': f'Erreur HTTP {e.response.status_code}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': f'Erreur inattendue: {str(e)}'
            }
    
    def fetch_multiple(self, urls: list) -> Dict:
        """
        Récupère plusieurs pages (utile pour analyse complète d'un site)
        
        Args:
            urls: Liste d'URLs à récupérer
            
        Returns:
            Dictionnaire avec résultats pour chaque URL
        """
        results = {}
        
        for url in urls:
            print(f"Récupération de {url}...")
            results[url] = self.fetch_page(url)
            time.sleep(1)  # Pause entre requêtes pour ne pas surcharger le serveur
        
        return results


# Instance globale du crawler
crawler = WebCrawler()


def fetch_url(url: str) -> Dict:
    """
    Fonction utilitaire pour récupérer une URL
    
    Args:
        url: URL à récupérer
        
    Returns:
        Résultat du crawl
    """
    return crawler.fetch_page(url)


# Test si exécuté directement
if __name__ == "__main__":
    # Test avec un site public
    test_url = "https://www.example.com"
    
    print("=" * 70)
    print(f"TEST WEB CRAWLER - {test_url}")
    print("=" * 70)
    
    result = fetch_url(test_url)
    
    if result['success']:
        print(f"\n✓ Succès !")
        print(f"URL finale      : {result['url']}")
        print(f"Status code     : {result['status_code']}")
        print(f"Temps réponse   : {result['elapsed_time']:.2f}s")
        print(f"Taille HTML     : {len(result['html'])} caractères")
        print(f"Nombre cookies  : {len(result['cookies'])}")
        print(f"\nCookies trouvés :")
        for cookie in result['cookies']:
            print(f"  - {cookie['name']} (domaine: {cookie['domain']})")
    else:
        print(f"\n✗ Échec : {result['error']}")