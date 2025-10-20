import json

def summarize_nlp_output_with_alerts(file_path, max_chars=200, min_length=20):
    """Résumé complet du NLP output avec alertes sur textes vides ou très courts"""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            print(f"✅ JSON chargé avec succès : {file_path}\n")
        except json.JSONDecodeError as e:
            print("❌ JSON invalide :", e)
            return

    # --- RGPD ---
    rgpd_articles = data.get("rgpd_analysis", [])
    print(f"Nombre total d'articles RGPD : {len(rgpd_articles)}")
    empty_articles = []
    for article in rgpd_articles:
        texte = article.get("contenu", "")
        if not texte.strip() or len(texte.strip()) < min_length:
            empty_articles.append(f"{article.get('numero')} - {article.get('titre_chapitre')}")
    print(f"Articles RGPD vides ou très courts : {len(empty_articles)}")
    if empty_articles:
        print("Liste des articles problématiques :", empty_articles)
    print()

    # --- Site Web ---
    site_pages = data.get("site_analysis", [])
    print(f"Nombre total de pages site : {len(site_pages)}")
    empty_sections = []
    for page in site_pages:
        url = page.get("url")
        sections = page.get("sections", [])
        for idx, sec in enumerate(sections):
            texte = sec.get("contenu", "")
            if not texte.strip() or len(texte.strip()) < min_length:
                empty_sections.append({
                    "page_url": url,
                    "section_index": idx + 1,
                    "section_type": sec.get("type")
                })

    print(f"Sections site vides ou très courtes : {len(empty_sections)}")
    if empty_sections:
        print("Détails des sections problématiques :")
        for s in empty_sections:
            print(f"- Page: {s['page_url']}, Section #{s['section_index']}, Type: {s['section_type']}")
    print("\n✅ Vérification terminée.")

# =======================================
# Exécution
# =======================================
if __name__ == "__main__":
    summarize_nlp_output_with_alerts("nlp_output.json")
