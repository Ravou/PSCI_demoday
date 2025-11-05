import os
import json
from datetime import datetime
from app.service.extraction_docs import GDPRScraper
from app.service.nlp_preprocessor import NLPPreprocessor


class GDPRUpdater:
    def __init__(self,
                 rgpd_path="data/gdpr_structure.json",
                 embeddings_path="data/gdpr_embeddings.json",
                 log_path="data/gdpr_update_log.txt"):
        self.rgpd_path = rgpd_path
        self.embeddings_path = embeddings_path
        self.log_path = log_path


        # ✅ We use the actual scraper
        self.scraper = GDPRScraper()
        self.nlp_proc = NLPPreprocessor()


    def check_and_update(self):
        """Checks if the GDPR has changed and updates it if necessary."""
        print("🔍 Checking GDPR updates...")


        has_changed = self.scraper.check_update()


        if not has_changed:
            print("✅ No changes detected in GDPR.")
            return False


        print("⚠️ New version of GDPR detected!")
        self.update_gdpr()
        return True


    def update_gdpr(self):
        """Scrapes, updates the JSON, and regenerates NLP embeddings."""
        # 🧠 GDPR scraping
        self.scraper.scrape()


        # Save the new structure
        if not os.path.exists(self.scraper.json_path):
            print("❌ Error: GDPR JSON file was not generated.")
            return


        os.makedirs(os.path.dirname(self.rgpd_path), exist_ok=True)
        os.replace(self.scraper.json_path, self.rgpd_path)
        print(f"🆕 GDPR file updated: {self.rgpd_path}")


        # 🧹 Remove old embeddings cache
        if os.path.exists(self.embeddings_path):
            os.remove(self.embeddings_path)
            print(f"🗑️ Old GDPR cache deleted: {self.embeddings_path}")


        # 🔁 Recalculate the NLP embeddings
        self.nlp_proc.save_rgpd_embeddings(self.rgpd_path, self.embeddings_path)
        print(f"✅ GDPR embeddings successfully updated: {self.embeddings_path}")


        # 🕒 Logging
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now()} - GDPR updated and embeddings regenerated\n")
        print(f"📜 Log updated: {self.log_path}")



# ==========================
# 🔹 Main
# ==========================
if __name__ == "__main__":
    updater = GDPRUpdater()
    updater.check_and_update()
