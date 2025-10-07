from app.models.user import User
from content_scraper import ContentScraper
from extract_ssl import get_certificate_info
import requests
from bs4 import BeautifulSoup
import time


class WebCrawler:
    def __init__(self, start_url, max_depth=2, delay=1):
        """
        start_url: URL de départ
        max_depth: profondeur maximale du crawl
        delay: délai entre les requêtes en secondes
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        
        self.visited = set()

    def crawl(self, url=None, depth=1):
        """
        Fonction récursive pour parcourir les pages du site
        """
        if url is None:
            url = self.start_url

        if url in self.visited or depth > self.max_depth:
            return

        self.visited.add(url)
        print(f"Crawling: {url}")

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            print(f"Failed to access {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Parcours tous les liens internes et externes
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            if next_url.startswith('http'):
                self.crawl(next_url, depth + 1)
            elif next_url.startswith('/'):
                # Forme complète de l'URL pour liens relatifs
                base_url = self.start_url.rstrip('/')
                full_url = base_url + next_url
                self.crawl(full_url, depth + 1)

        # Pause pour ne pas surcharger le serveur
        time.sleep(self.delay)

    def get_visited(self):
        """Retourne la liste des URLs visitées"""
        return list(self.visited)


if __name__ == "__main__":
    url_input = input("Entrez l'URL du site à auditer : ")
    crawler = WebCrawler(start_url=url_input, max_depth=2, delay=1)
    crawler.crawl()
    visited_pages = crawler.get_visited()

    scraper = ContentScraper()
    all_results = []
    for page_url in visited_pages:
        static_data = scraper.scrape_static(page_url)
        dynamic_data = scraper.scrape_dynamic(page_url)
        all_results.append({
            "url": page_url,
            "static": static_data,
            "dynamic": dynamic_data
        })

    print("\n=== Résultats pour toutes les pages ===")
    for result in all_results:
        print(result)

