"""
Test avec une URL personnalisée
"""

import sys
from app.services.web_crawler import WebCrawler
from app.services.content_scraper import ContentScraper

# URL depuis argument ou défaut
url = sys.argv[1] if len(sys.argv) > 1 else "https://www.cnil.fr"

print(f"🔍 Analyse RGPD rapide de : {url}\n")

# Crawl
crawler = WebCrawler()
result = crawler.fetch_page(url)

if not result['success']:
    print(f"❌ Erreur : {result['error']}")
    exit(1)

print(f"✅ Page récupérée ({len(result['html'])} caractères)")

# Scrape
scraper = ContentScraper()
content = scraper.parse_html(result['html'], url)

print(f"\n📊 Résultats :")
print(f"  Titre     : {content['title']}")
print(f"  Cookies   : {'✓ Mentionnés' if content['cookies_mentioned'] else '✗ Non mentionnés'}")
print(f"  Privacy   : {content['privacy_policy_link'] or '✗ Non trouvée'}")
print(f"  Trackers  : {sum(1 for v in content['trackers'].values() if v)} détectés")
print(f"  RGPD      : {', '.join(content['rgpd_keywords']) if content['rgpd_keywords'] else '✗ Non mentionné'}")

