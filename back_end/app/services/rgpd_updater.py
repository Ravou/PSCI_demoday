import os
import json
from datetime import datetime
from app.service.nlp_preprocessor import NLPPreprocessor  # ton module de scraping

class RGPDUpdater:
    def __init__(self,
                 rgpd_path="data/rgpd_structure.json",
                 embeddings_path="data/rgpd_embeddings.json",
                 log_path="data/rgpd_update_log.txt"):
        self.rgpd_path = rgpd_path
        self.embeddings_path = embeddings_path
        self.log_path = log_path
        self.scraper = RGPDUpdater()
        self.nlp_proc = NLPPreprocessor()

    def check_and_update(self):
        print("🔍 Vérification des mises à jour RGPD...")

        has_changed = self.scraper.check_for_update()

        if not has_changed:
            print("✅ Aucun changement détecté dans le RGPD.")
            return False

        print("⚠️ Nouvelle version du RGPD détectée !")
        self.update_rgpd()
        return True

    def update_rgpd(self):
        # Scraping RGPD
        new_data = self.scraper.scrape_rgpd()

        # Sauvegarde nouvelle structure RGPD
        os.makedirs(os.path.dirname(self.rgpd_path), exist_ok=True)
        with open(self.rgpd_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        print(f"🆕 Fichier RGPD mis à jour : {self.rgpd_path}")

        # Supprime l’ancien cache d’embeddings
        if os.path.exists(self.embeddings_path):
            os.remove(self.embeddings_path)
            print(f"🗑️ Ancien cache RGPD supprimé : {self.embeddings_path}")

        # Recalcule les embeddings
        self.nlp_proc.save_rgpd_embeddings(self.rgpd_path, self.embeddings_path)
        print(f"✅ RGPD embeddings mis à jour avec succès : {self.embeddings_path}")

        # Historique
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now()} - RGPD mis à jour et embeddings régénérés\n")
        print(f"📜 Historique mis à jour : {self.log_path}")


# ==========================
# 🔹 Main
# ==========================
if __name__ == "__main__":
    updater = RGPDUpdater()
    updater.check_and_update()
