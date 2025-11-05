from app.service.content_scraper import ContentScraper
from app.service.extract_ssl import ExtractSSL
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json


class WebCrawler:


    def __init__(self, start_url, max_depth=2, delay=1):
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.ssl_objects = []  # List to store ExtractSSL instances
        self.scraper = ContentScraper()  # Instantiate the scraper


    def crawl(self, url=None, depth=1):
        """Recursive function to crawl site pages"""
        if url is None:
            url = self.start_url


        if url in self.visited or depth > self.max_depth:
            return


        self.visited.add(url)
        print(f"Crawling: {url}")


        # 🔹 SSL extraction for this page
        ssl_obj = ExtractSSL(url)
        self.ssl_objects.append(ssl_obj)
        print(f"SSL info: {ssl_obj.info.get('common_name', 'N/A')}")


        # 🔹 HTTP request for static scraping
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            print(f"Failed to access {url}")
            return


        soup = BeautifulSoup(response.text, 'html.parser')


        # 🔹 Traverse links to continue crawling
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            full_url = urljoin(url, next_url)
            if full_url.startswith(("http://", "https://")):
                if full_url not in self.visited:
                    self.crawl(full_url, depth + 1)


        time.sleep(self.delay)


    def get_visited(self):
        """Returns the list of visited URLs"""
        return list(self.visited)


    def get_ssl_info(self):
        """Returns the list of collected SSL certificates"""
        return [obj.info for obj in self.ssl_objects]


    def run_scraping(self):
        """Performs static and dynamic scraping on all visited pages"""
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


    def run(self):
        """Chains crawling and scraping, returning everything in memory"""
        self.crawl()
        results = self.run_scraping()
        return results


    def __repr__(self):
        return (
            f"WebCrawler(start_url='{self.start_url}', "
            f"pages_visited={len(self.visited)})"
        )


if __name__ == "__main__":
    url_input = input("Enter the website URL to audit: ")
    crawler = WebCrawler(start_url=url_input, max_depth=2, delay=1)
    results = crawler.run()

    print(json.dumps(results, indent=2, ensure_ascii=False))
