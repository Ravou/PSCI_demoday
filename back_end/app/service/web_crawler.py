from app.service.content_scraper import ContentScraper
from app.service.extract_ssl import ExtractSSL
from app.models.base_model import BaseModel
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

class WebCrawler(BaseModel):

    def __init__(self, start_url, max_depth=2, delay=1):
        super().__init__()
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.ssl_objects = []  # Liste pour stocker les instances ExtractSSL
        self.scraper = ContentScraper()  # Instance du scraper

    def crawl(self, url=None, depth=1):
        """Fonction récursive pour parcourir les pages du site"""
        if url is None:
            url = self.start_url

        if url in self.visited or depth > self.max_depth:
            return

        self.visited.add(url)
        print(f"Crawling: {url}")

        # 🔹 Extraction SSL pour cette page
        ssl_obj = ExtractSSL(url)
        self.ssl_objects.append(ssl_obj)
        print(f"SSL info: {ssl_obj.info.get('common_name', 'N/A')}")

        # 🔹 Requête HTTP pour scraping statique
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            print(f"Failed to access {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # 🔹 Parcours des liens pour continuer le crawl
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            full_url = urljoin(url, next_url)
            if full_url.startswith("http://") or full_url.startswith("https://"):
                if full_url not in self.visited:
                    self.crawl(full_url, depth + 1)

        time.sleep(self.delay)

    def get_visited(self):
        """Retourne la liste des URLs visitées"""
        return list(self.visited)

    def get_ssl_info(self):
        """Retourne la liste des certificats SSL collectés"""
        return [obj.info for obj in self.ssl_objects]

    def run_scraping(self):
        """Réalise le scraping statique et dynamique sur toutes les pages visitées"""
        all_results = []

        visited_pages = self.get_visited()
        ssl_data = self.get_ssl_info()

        for i, page_url in enumerate(visited_pages):
            static_data = self.scraper.scrape_static(page_url)
            dynamic_data = self.scraper.scrape_dynamic(page_url)

            ssl_info = ssl_data[i] if i < len(ssl_data) else {}

            all_results.append({
                "url": page_url,
                "ssl": ssl_info,
                "static": static_data,
                "dynamic": dynamic_data
            })

        return all_results

    def __repr__(self):
        return (
            f"WebCrawler(id='{self.id}', start_url='{self.start_url}', "
            f"pages_visited={len(self.visited)})"
        )


if __name__ == "__main__":
    url_input = input("Entrez l'URL du site à auditer : ")
    crawler = WebCrawler(start_url=url_input, max_depth=2, delay=1)
    crawler.crawl()
    results = crawler.run_scraping()

    # Export JSON
    output_json = json.dumps(results, ensure_ascii=False, indent=4)
    print(output_json)

    with open("crawler_results.json", "w", encoding="utf-8") as f:
        f.write(output_json)


