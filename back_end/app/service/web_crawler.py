from content_scraper import ContentScraper
from extract_ssl import get_certificate_info
import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin

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
            full_url = urljoin(url, next_url)  # Résout les liens relatifs
            # Filtrer uniquement les URLs HTTP/HTTPS
            if full_url.startswith("http://") or full_url.startswith("https://"):
                if full_url not in self.visited:
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
        # Scraping statique
        static_data = scraper.scrape_static(page_url)
        # Scraping dynamique
        dynamic_data = scraper.scrape_dynamic(page_url)
        all_results.append({
            "url": page_url,
            "static": static_data,
            "dynamic": dynamic_data
        })

    # ===== Export JSON =====
    output_json = json.dumps(all_results, ensure_ascii=False, indent=4)
    
    # Affiche dans la console
    print(output_json)

    # Optionnel : sauvegarde dans un fichier
    with open("crawler_results.json", "w", encoding="utf-8") as f:
        f.write(output_json)
