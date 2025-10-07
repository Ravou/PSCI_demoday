import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class ContentScraper:
    def __init__(self):
        """Scraper pour analyser la conformité RGPD d’un site web."""
        self.remote_url = "http://localhost:4444/wd/hub"  # Docker Selenium (Chrome)
        self.rgpd_checklist = {
            "cookies": ["cookie", "consent", "traceur"],
            "confidentialite": ["confidentialité", "privacy", "données personnelles"],
            "mentions_legales": ["mentions légales", "legal notice"],
            "formulaires": ["formulaire", "contact", "newsletter"],
            "securite": ["https", "securite", "cryptage", "chiffrement"]
        }

    def scrape_static(self, url):
        """Analyse statique : liens RGPD et texte complet des pages RGPD."""
        if not url.startswith("http"):
            url = "https://" + url

        result = {"url": url, "liens_rgpd": [], "textes_rgpd": {}}

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Recherche des liens RGPD
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            rgpd_links = [
                l for l in links
                if any(word in l.lower() for word in ["cookie", "privacy", "confidentialite", "legal", "rgpd"])
            ]
            result["liens_rgpd"] = rgpd_links

            # Récupération du texte complet de chaque page RGPD
            for link in rgpd_links:
                full_url = link if link.startswith("http") else url.rstrip("/") + "/" + link.lstrip("/")
                try:
                    r = requests.get(full_url, timeout=10)
                    r.raise_for_status()
                    soup_page = BeautifulSoup(r.text, 'html.parser')
                    result["textes_rgpd"][full_url] = soup_page.get_text(separator="\n").strip()
                except Exception:
                    result["textes_rgpd"][full_url] = ""
            return result

        except requests.RequestException as e:
            print(f"Erreur lors de la requête statique : {e}")
            return result

    def scrape_dynamic(self, url, wait_time=5):
        """Analyse dynamique pour détecter popups, formulaires et sécurité front."""
        if not url.startswith("http"):
            url = "https://" + url

        results = {}

        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Remote(command_executor=self.remote_url, options=options)
            driver.get(url)
            time.sleep(wait_time)

            html = driver.page_source.lower()

            # Vérifie la présence de mots-clés RGPD
            for theme, keywords in self.rgpd_checklist.items():
                results[theme] = any(kw in html for kw in keywords)

            # Détection d’un bandeau cookie
            banners = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie')]"
            )
            results["bandeau_cookie"] = len(banners) > 0

            # Analyse des formulaires : consentement actif et clarté de la finalité
            forms = driver.find_elements(By.TAG_NAME, "form")
            results["formulaires_detectes"] = len(forms)
            forms_info = []
            for f in forms:
                inputs = f.find_elements(By.TAG_NAME, "input")
                checkboxes = [i for i in inputs if i.get_attribute("type") == "checkbox"]
                forms_info.append({
                    "checkboxes_count": len(checkboxes),
                    "all_unchecked": all(not c.is_selected() for c in checkboxes)
                })
            results["formulaires_info"] = forms_info

            driver.quit()
            return {"url": url, "resultats": results}

        except Exception as e:
            print(f"Erreur lors du scraping dynamique : {e}")
            return {"url": url, "resultats": results}


if __name__ == "__main__":
    scraper = ContentScraper()
    url = input("Veuillez entrer l'URL du site à analyser : ")

    # Scraping statique
    static_data = scraper.scrape_static(url)

    # Scraping dynamique
    dynamic_data = scraper.scrape_dynamic(url)

    # Résultat combiné prêt pour l'IA
    audit_data = {
        "url": url,
        "liens_rgpd": static_data["liens_rgpd"],
        "textes_rgpd": static_data["textes_rgpd"],
        "resultats_dynamiques": dynamic_data["resultats"]
    }

    print("\n=== Données brutes prêtes pour l'IA ===")
    print(audit_data)

