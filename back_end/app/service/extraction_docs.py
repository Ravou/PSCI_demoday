import os
import re
import json
import requests
import pdfplumber
from hashlib import sha256
from datetime import datetime, timezone
from app.service.nlp_preprocessor import NLPPreprocessor
import schedule
import time


PDF_URL = "https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:32016R0679"
JSON_PATH = "gdpr_structure.json"
TEMP_PDF = "gdpr_temp.pdf"
SNIPPET_WORDS = 200



class GDPRScraper:
    def __init__(self, pdf_url=PDF_URL, json_path=JSON_PATH):
        self.pdf_url = pdf_url
        self.json_path = json_path
        self.data = {
            "regulation": {
                "version": "1.0",
                "source_url": self.pdf_url,
                "last_checked": None,
                "last_modified_online": None,
                "etag": None,
                "hash_content": None,
                "preliminary_parts": {},
                "normative_provisions": {"chapters": []},
                "case_law": [],
                "last_modifications": {"date": None, "modified_articles": []},
                "snippets_nlp": []
            }
        }
        self.load_json()


    def load_json(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)


    def check_update(self):
        try:
            response = requests.head(self.pdf_url, allow_redirects=True, timeout=10)
        except requests.RequestException:
            print("❌ Unable to check server changes.")
            return False


        last_modified = response.headers.get("Last-Modified")
        etag = response.headers.get("ETag")


        if etag != self.data["regulation"].get("etag") or last_modified != self.data["regulation"].get("last_modified_online"):
            print("🔔 The GDPR PDF has been updated.")
            self.data["regulation"]["etag"] = etag
            self.data["regulation"]["last_modified_online"] = last_modified
            return True
        print("✅ No change detected.")
        return False


    def download_pdf(self):
        response = requests.get(self.pdf_url)
        response.raise_for_status()
        with open(TEMP_PDF, "wb") as f:
            f.write(response.content)
        return TEMP_PDF


    def extract_text(self):
        full_text = ""
        with pdfplumber.open(TEMP_PDF) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text


    def hash_text(self, text):
        return sha256(text.encode("utf-8")).hexdigest()


    def parse_sections(self, text):
        prelim_match = re.search(r"(Considerations\s.*?)(?=CHAPTER\sI)", text, re.DOTALL | re.IGNORECASE)
        if prelim_match:
            self.data["regulation"]["preliminary_parts"] = {"text": prelim_match.group(1).strip()}


        case_law = re.findall(r"(Case Law\s.*?)(?=CHAPTER\s|Article\s\d+|$)", text, re.DOTALL | re.IGNORECASE)
        self.data["regulation"]["case_law"] = [j.strip() for j in case_law]


        chap_pattern = re.compile(r"(CHAPTER\s+[IVXLC]+)\s+(.*?)\n(.*?)(?=CHAPTER\s+[IVXLC]+|$)", re.DOTALL)
        new_chap = []
        for chap_match in chap_pattern.finditer(text):
            chap_num = chap_match.group(1).strip()
            chap_title = chap_match.group(2).strip()
            chap_content = chap_match.group(3).strip()


            articles = []
            art_pattern = re.compile(r"(Article\s+\d+[A-Z]?)\s*(.*?)(?=Article\s+\d+[A-Z]?|CHAPTER\s+[IVXLC]|$)", re.DOTALL)
            for art_match in art_pattern.finditer(chap_content):
                art_num = art_match.group(1).strip()
                art_text = art_match.group(2).strip()
                articles.append({"number": art_num, "content": art_text})


            new_chap.append({
                "number": chap_num,
                "title": chap_title,
                "articles": articles
            })
        return new_chap


    def create_snippets(self, text, max_words=SNIPPET_WORDS):
        """Split the text into snippets for NLP."""
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        snippets = []
        for p in paragraphs:
            words = p.split()
            for i in range(0, len(words), max_words):
                snippets.append(" ".join(words[i:i + max_words]))
        return snippets


    def compare_and_update(self, new_chap):
        modified_articles = []
        old_chap = {c["number"]: c for c in self.data["regulation"]["normative_provisions"]["chapters"]}


        for chap in new_chap:
            chap_num = chap["number"]
            if chap_num not in old_chap:
                self.data["regulation"]["normative_provisions"]["chapters"].append(chap)
                modified_articles.extend([a["number"] for a in chap["articles"]])
            else:
                old_articles = {a["number"]: a for a in old_chap[chap_num]["articles"]}
                for art in chap["articles"]:
                    num = art["number"]
                    if num not in old_articles or art["content"] != old_articles[num]["content"]:
                        if num in old_articles:
                            old_articles[num]["content"] = art["content"]
                        else:
                            old_chap[chap_num]["articles"].append(art)
                        modified_articles.append(num)


        self.data["regulation"]["last_modifications"] = {
            "date": datetime.now(timezone.utc).isoformat(),
            "modified_articles": modified_articles
        }


    def save_json(self, text_hash, snippets):
        self.data["regulation"]["last_checked"] = datetime.now(timezone.utc).isoformat()
        self.data["regulation"]["hash_content"] = text_hash
        self.data["regulation"]["snippets_nlp"] = snippets
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"💾 JSON saved to {self.json_path}")


    def scrape(self):
        print("⬇️ Downloading PDF...")
        self.download_pdf()
        print("📄 Extracting text...")
        full_text = self.extract_text()
        text_hash = self.hash_text(full_text)
        print("🗂️ Splitting sections...")
        new_chap = self.parse_sections(full_text)
        print("🔍 Comparing with existing version...")
        self.compare_and_update(new_chap)
        print("✂️ Creating NLP snippets...")
        snippets = self.create_snippets(full_text)
        print("💾 Saving JSON...")
        self.save_json(text_hash, snippets)
        os.remove(TEMP_PDF)
        print("✅ Done.")
    
    def __repr__(self):
        return f"GDPRScraper(pdf_url='{self.pdf_url}', json_path='{self.json_path}')"




if __name__ == "__main__":
    scraper = GDPRScraper()


    print("🚀 Initial GDPR scraping...")
    scraper.scrape()


    def weekly_check():
        print("🔎 Weekly GDPR check...")
        if scraper.check_update():
            scraper.scrape()


            from app.service.rgpd_updater import RGPDUpdater
            updater = RGPDUpdater()
            updater.update_rgpd_cache()
        else:
            print("✅ No change detected, scraping not required.")


    schedule.every().monday.at("09:00").do(weekly_check)
    print("⏳ Weekly checking system started...")


    while True:
        schedule.run_pending()
        time.sleep(60)


