import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List, Dict, Any, Optional
import time
import json


class ContentScraper:
    _scrapers: List['ContentScraper'] = []


    def __init__(self, remote_url: str = "http://localhost:4444/wd/hub"):
        self.remote_url = remote_url
        self.results: Optional[Dict[str, Any]] = None
        self.rgpd_checklist = {
            "cookies": ["cookie", "consent", "tracker"],
            "privacy": ["privacy", "data protection", "personal data"],
            "legal_notices": ["legal notice"],
            "forms": ["form", "contact", "newsletter"],
            "security": ["https", "security", "encryption", "cryptography"]
        }
        ContentScraper._scrapers.append(self)


    # ------------------------------------------------------------
    # 📄 STATIC SCRAPING
    # ------------------------------------------------------------
    def scrape_static(self, url: str) -> Dict[str, Any]:
        """Static analysis: GDPR links and full text of GDPR pages."""
        if not url.startswith("http"):
            url = "https://" + url


        result = {"url": url, "gdpr_links": [], "gdpr_texts": {}}


        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")


            links = [a.get("href") for a in soup.find_all("a", href=True)]
            gdpr_links = [
                l for l in links
                if any(word in l.lower() for word in ["cookie", "privacy", "confidentiality", "legal", "gdpr"])
            ]
            result["gdpr_links"] = gdpr_links


            # Extract texts from GDPR pages
            for link in gdpr_links:
                full_url = link if link.startswith("http") else url.rstrip("/") + "/" + link.lstrip("/")
                try:
                    r = requests.get(full_url, timeout=10)
                    r.raise_for_status()
                    soup_page = BeautifulSoup(r.text, "html.parser")
                    result["gdpr_texts"][full_url] = soup_page.get_text(separator="\n").strip()
                except Exception:
                    result["gdpr_texts"][full_url] = ""
            return result


        except requests.RequestException as e:
            print(f"Error during static request: {e}")
            return result


    # ------------------------------------------------------------
    # 🧠 GDPR SIGNAL DETECTION
    # ------------------------------------------------------------
    def detect_gdpr_signals(self, text: str) -> Dict[str, bool]:
        """Quick detection of GDPR themes in the general page text"""
        checks = {
            "cookies": ["cookie", "consent", "tracker"],
            "privacy": ["privacy", "data protection", "personal data", "data protection"],
            "legal_notices": ["legal notice"],
            "forms": ["form", "contact", "newsletter", "registration"],
            "security": ["https", "ssl", "security", "encryption"],
            "rights": ["right of access", "erasure", "rectification", "portability", "objection"],
            "marketing": ["newsletter", "unsubscription", "email marketing"]
        }
        detected = {}
        lower_text = text.lower()
        for theme, keywords in checks.items():
            detected[theme] = any(k in lower_text for k in keywords)
        return detected


    # ------------------------------------------------------------
    # ⚙️ FULL DYNAMIC SCRAPING WITH SNIPPETS
    # ------------------------------------------------------------
    def scrape_dynamic(self, url: str, wait_time: int = 5, implicit_wait: int = 2, snippet_words: int = 200) -> Dict[str, Any]:
        """Full dynamic GDPR scraping + snippet creation for NLP"""
        if not url.startswith("http"):
            url = "https://" + url


        results = {
            "url": url,
            "signals_detected": {},
            "html_text_snippet": "",
            "snippets_nlp": {},
            "cookie_banner": {"present": False, "texts": []},
            "privacy_sections": {"present": False, "texts": []},
            "legal_notices": {"present": False, "texts": []},
            "forms_detected": 0,
            "forms_info": [],
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


            # ---- Getting main text content ----
            main_content = driver.find_elements(By.TAG_NAME, "main")
            if main_content:
                full_text = "\n".join([el.text for el in main_content if el.text.strip()])
            else:
                body = driver.find_element(By.TAG_NAME, "body")
                full_text = body.text or ""


            # Simple cleaning for NLP
            full_text = "\n".join([line.strip() for line in full_text.splitlines() if line.strip()])
            results["html_text_snippet"] = full_text


            # ---- Creating NLP snippets ----
            paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]
            snippets = []
            for p in paragraphs:
                words = p.split()
                for i in range(0, len(words), snippet_words):
                    snippets.append(" ".join(words[i:i + snippet_words]))
            results["snippets_nlp"] = {i: s for i, s in enumerate(snippets)}


            # ---- Detect GDPR signals ----
            gdpr_signals = self.detect_gdpr_signals(full_text)
            results["signals_detected"] = gdpr_signals
            lower_html = driver.page_source.lower()


            # ---- Cookie banner ----
            if gdpr_signals.get("cookies"):
                cookie_elements = driver.find_elements(
                    By.XPATH,
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'consent')]"
                )
                results["cookie_banner"]["present"] = len(cookie_elements) > 0
                results["cookie_banner"]["texts"] = [el.text.strip() for el in cookie_elements if el.text.strip()]


            # ---- Privacy sections ----
            if gdpr_signals.get("privacy"):
                for kw in ["privacy", "confidentialit", "personal data"]:
                    elems = driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw}')]")
                    for el in elems:
                        t = el.text.strip()
                        if t and t not in results["privacy_sections"]["texts"]:
                            results["privacy_sections"]["texts"].append(t)
                results["privacy_sections"]["present"] = len(results["privacy_sections"]["texts"]) > 0


            # ---- Legal notices ----
            if gdpr_signals.get("legal_notices"):
                for kw in ["legal notice"]:
                    elems = driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw}')]")
                    for el in elems:
                        t = el.text.strip()
                        if t and t not in results["legal_notices"]["texts"]:
                            results["legal_notices"]["texts"].append(t)
                results["legal_notices"]["present"] = len(results["legal_notices"]["texts"]) > 0


            # ---- Forms ----
            if gdpr_signals.get("forms"):
                forms = driver.find_elements(By.TAG_NAME, "form")
                results["forms_detected"] = len(forms)
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
                    results["forms_info"].append(info)


            # ---- Security ----
            if gdpr_signals.get("security"):
                results["security_info"]["https"] = url.startswith("https")
                if "security" in lower_html or "ssl" in lower_html:
                    results["security_info"]["mentions"].append("Security mention found")


            driver.quit()
            return results


        except Exception as e:
            print(f"Dynamic scraping error: {e}")
            if driver:
                driver.quit()
            return results


    def __repr__(self):
        return f"ContentScraper(remote_url='{self.remote_url}')"

