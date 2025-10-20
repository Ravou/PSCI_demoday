import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List, Dict, Any, Optional
from app.models.base_model import BaseModel
import time
import json

class ContentScraper(BaseModel):
    _scrapers: List['ContentScraper'] = []

    allowed_update_fields = ['remote_url']

    def __init__(self, remote_url: str = "http://localhost:4444/wd/hub"):
        super().__init__()
        self.remote_url = remote_url
        self.results: Optional[Dict[str, Any]] = None
        self.rgpd_checklist = {
            "cookies": ["cookie", "consent", "traceur"],
            "confidentialite": ["confidentialité", "privacy", "données personnelles"],
            "mentions_legales": ["mentions légales", "legal notice"],
            "formulaires": ["formulaire", "contact", "newsletter"],
            "securite": ["https", "securite", "cryptage", "chiffrement"]
        }
        ContentScraper._scrapers.append(self)

    # ------------------------------------------------------------
    # 📄 SCRAPING STATIQUE
    # ------------------------------------------------------------
    def scrape_static(self, url: str) -> Dict[str, Any]:
        """Analyse statique : liens RGPD et texte complet des pages RGPD."""
        if not url.startswith("http"):
            url = "https://" + url

        result = {"url": url, "liens_rgpd": [], "textes_rgpd": {}}

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraction des liens RGPD
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            rgpd_links = [
                l for l in links
                if any(word in l.lower() for word in ["cookie", "privacy", "confidentialite", "legal", "rgpd"])
            ]
            result["liens_rgpd"] = rgpd_links

            # Extraction du texte des pages RGPD
            for link in rgpd_links:
                full_url = link if link.startswith("http") else url.rstrip("/") + "/" + link.lstrip("/")
                try:
                    r = requests.get(full_url, timeout=10)
                    r.raise_for_status()
                    soup_page = BeautifulSoup(r.text, "html.parser")
                    result["textes_rgpd"][full_url] = soup_page.get_text(separator="\n").strip()
                except Exception:
                    result["textes_rgpd"][full_url] = ""
            return result

        except requests.RequestException as e:
            print(f"Erreur lors de la requête statique : {e}")
            return result

    # ------------------------------------------------------------
    # 🧠 DÉTECTION DE SIGNAUX RGPD
    # ------------------------------------------------------------
    def detect_rgpd_signals(self, text: str) -> Dict[str, bool]:
        """Détection rapide des thèmes RGPD dans le texte général de la page"""
        checks = {
            "cookies": ["cookie", "consent", "traceur"],
            "confidentialite": ["confidentialité", "privacy", "données personnelles", "protection des données"],
            "mentions": ["mentions légales", "legal notice"],
            "formulaires": ["formulaire", "contact", "newsletter", "inscription"],
            "securite": ["https", "ssl", "sécurité", "chiffrement"],
            "droits": ["droit d'accès", "effacement", "rectification", "portabilité", "opposition"],
            "prospection": ["newsletter", "désinscription", "email marketing"]
        }
        detected = {}
        lower_text = text.lower()
        for theme, keywords in checks.items():
            detected[theme] = any(k in lower_text for k in keywords)
        return detected

    # ------------------------------------------------------------
    # ⚙️ SCRAPING DYNAMIQUE COMPLET AVEC SNIPPETS
    # ------------------------------------------------------------
    def scrape_dynamic(self, url: str, wait_time: int = 5, implicit_wait: int = 2, snippet_words: int = 200) -> Dict[str, Any]:
        """Scraping dynamique RGPD complet + création de snippets pour NLP"""
        if not url.startswith("http"):
            url = "https://" + url

        results = {
            "url": url,
            "signals_detected": {},
            "html_text_snippet": "",
            "snippets_nlp": {},  # dict indexé pour NLP
            "bandeau_cookie": {"present": False, "texts": []},
            "privacy_sections": {"present": False, "texts": []},
            "mentions_legales": {"present": False, "texts": []},
            "formulaires_detectes": 0,
            "formulaires_info": [],
            "security_info": {"https": False, "mentions": []}
        }

        driver = None
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Remote(command_executor=self.remote_url, options=options)
            driver.implicitly_wait(implicit_wait)
            driver.get(url)
            time.sleep(wait_time)

            # ---- Récupération du texte principal ----
            main_content = driver.find_elements(By.TAG_NAME, "main")
            if main_content:
                full_text = "\n".join([el.text for el in main_content if el.text.strip()])
            else:
                body = driver.find_element(By.TAG_NAME, "body")
                full_text = body.text or ""

            # Nettoyage simple pour NLP
            full_text = "\n".join([line.strip() for line in full_text.splitlines() if line.strip()])
            results["html_text_snippet"] = full_text

            # ---- Création des snippets NLP ----
            paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]
            snippets = []
            for p in paragraphs:
                words = p.split()
                for i in range(0, len(words), snippet_words):
                    snippets.append(" ".join(words[i:i + snippet_words]))
            results["snippets_nlp"] = {i: s for i, s in enumerate(snippets)}

            # ---- Détection des signaux RGPD ----
            rgpd_signals = self.detect_rgpd_signals(full_text)
            results["signals_detected"] = rgpd_signals
            lower_html = driver.page_source.lower()

            # ---- Bandeau cookie ----
            if rgpd_signals.get("cookies"):
                cookie_elements = driver.find_elements(
                    By.XPATH,
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'consent')]"
                )
                results["bandeau_cookie"]["present"] = len(cookie_elements) > 0
                results["bandeau_cookie"]["texts"] = [el.text.strip() for el in cookie_elements if el.text.strip()]

            # ---- Sections privacy ----
            if rgpd_signals.get("confidentialite"):
                for kw in ["privacy", "confidentialit", "données personnelles"]:
                    elems = driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw}')]")
                    for el in elems:
                        t = el.text.strip()
                        if t and t not in results["privacy_sections"]["texts"]:
                            results["privacy_sections"]["texts"].append(t)
                results["privacy_sections"]["present"] = len(results["privacy_sections"]["texts"]) > 0

            # ---- Mentions légales ----
            if rgpd_signals.get("mentions"):
                for kw in ["mentions légales", "legal notice"]:
                    elems = driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw}')]")
                    for el in elems:
                        t = el.text.strip()
                        if t and t not in results["mentions_legales"]["texts"]:
                            results["mentions_legales"]["texts"].append(t)
                results["mentions_legales"]["present"] = len(results["mentions_legales"]["texts"]) > 0

            # ---- Formulaires ----
            if rgpd_signals.get("formulaires"):
                forms = driver.find_elements(By.TAG_NAME, "form")
                results["formulaires_detectes"] = len(forms)
                for f in forms:
                    info = {
                        "action": f.get_attribute("action") or "",
                        "method": (f.get_attribute("method") or "").lower(),
                        "inputs": [],
                        "checkboxes_count": 0,
                        "all_unchecked": True
                    }
                    inputs = f.find_elements(By.XPATH, ".//input | .//textarea | .//select")
                    for i in inputs:
                        tag = i.tag_name.lower()
                        itype = (i.get_attribute("type") or "").lower() if tag == "input" else tag
                        name = i.get_attribute("name") or ""
                        placeholder = i.get_attribute("placeholder") or ""
                        checked = False
                        if itype == "checkbox":
                            info["checkboxes_count"] += 1
                            checked = i.is_selected()
                            if checked:
                                info["all_unchecked"] = False
                        info["inputs"].append({
                            "tag": tag,
                            "type": itype,
                            "name": name,
                            "placeholder": placeholder,
                            "checked": checked
                        })
                    results["formulaires_info"].append(info)

            # ---- Sécurité ----
            if rgpd_signals.get("securite"):
                results["security_info"]["https"] = url.startswith("https")
                if "sécurité" in lower_html or "ssl" in lower_html:
                    results["security_info"]["mentions"].append("Mention de sécurité trouvée")

            driver.quit()
            return results

        except Exception as e:
            print(f"Erreur scraping dynamique : {e}")
            if driver:
                driver.quit()
            return results

    def __repr__(self):
        return f"ContentScraper(id='{self.id}', remote_url='{self.remote_url}')"

