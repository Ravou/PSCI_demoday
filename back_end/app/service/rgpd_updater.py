import os
import json
from datetime import datetime
from app.service.extraction_docs import GDPRScraper  # ✅ le vrai scraper
from app.service.nlp_preprocessor import NLPPreprocessor


class RGPDUpdater:
    def __init__(self,
                 rgpd_path="data/rgpd_structure.json",
                 embeddings_path="data/rgpd_embeddings.json",
                 log_path="data/rgpd_update_log.txt"):
        self.rgpd_path = rgpd_path
        self.embeddings_path = embeddings_path
        self.log_path = log_path

        # ✅ On utilise le scraper réel
        self.scraper = GDPRScraper()
        self.nlp_proc = NLPPreprocessor()

    def check_and_update(self):
        """Vérifie si le RGPD a changé et le met à jour si nécessaire."""
        print("🔍 Vérification des mises à jour RGPD...")

        has_changed = self.scraper.check_update()

        if not has_changed:
            print("✅ Aucun changement détecté dans le RGPD.")
            return False

        print("⚠️ Nouvelle version du RGPD détectée !")
        self.update_rgpd()
        return True

    def update_rgpd(self):
        """Scrape, met à jour le JSON et régénère les embeddings NLP."""
        # 🧠 Scraping RGPD
        self.scraper.scrape()

        # Sauvegarde de la nouvelle structure
        if not os.path.exists(self.scraper.json_path):
            print("❌ Erreur : le fichier JSON RGPD n’a pas été généré.")
            return

        os.makedirs(os.path.dirname(self.rgpd_path), exist_ok=True)
        os.replace(self.scraper.json_path, self.rgpd_path)
        print(f"🆕 Fichier RGPD mis à jour : {self.rgpd_path}")

        # 🧹 Suppression de l’ancien cache d’embeddings
        if os.path.exists(self.embeddings_path):
            os.remove(self.embeddings_path)
            print(f"🗑️ Ancien cache RGPD supprimé : {self.embeddings_path}")

        # 🔁 Recalcul des embeddings NLP
        self.nlp_proc.save_rgpd_embeddings(self.rgpd_path, self.embeddings_path)
        print(f"✅ RGPD embeddings mis à jour avec succès : {self.embeddings_path}")

        # 🕒 Journalisation
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
