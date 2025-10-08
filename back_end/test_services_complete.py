"""
Test complet de tous les services d'extraction
"""

from app.services.web_crawler import WebCrawler
from app.services.content_scraper import ContentScraper
from app.services.nlp_preprocessor import NLPPreprocessor

print("=" * 80)
print("TEST COMPLET - ANALYSE RGPD D'UN SITE WEB")
print("=" * 80)

# URL à tester (site réel)
test_url = "https://www.example.com"

print(f"\n🌐 Étape 1 : Crawling de {test_url}")
print("-" * 80)

# 1. Récupère le HTML
crawler = WebCrawler()
crawl_result = crawler.fetch_page(test_url)

if not crawl_result['success']:
    print(f"✗ Erreur crawling : {crawl_result['error']}")
    exit(1)

print(f"✓ Page récupérée avec succès")
print(f"  - Status code  : {crawl_result['status_code']}")
print(f"  - Taille HTML  : {len(crawl_result['html'])} caractères")
print(f"  - Temps        : {crawl_result['elapsed_time']:.2f}s")
print(f"  - Cookies      : {len(crawl_result['cookies'])} détectés")

if crawl_result['cookies']:
    print(f"\n  Cookies trouvés :")
    for cookie in crawl_result['cookies'][:5]:  # Limite à 5
        print(f"    - {cookie['name']} (domaine: {cookie['domain']})")

# 2. Parse le HTML
print(f"\n📄 Étape 2 : Scraping du contenu HTML")
print("-" * 80)

scraper = ContentScraper()
scrape_result = scraper.parse_html(crawl_result['html'], test_url)

print(f"✓ Contenu extrait avec succès")
print(f"  - Titre        : {scrape_result['title']}")
print(f"  - Texte        : {len(scrape_result['text_content'])} caractères")
print(f"  - Scripts      : {len(scrape_result['scripts'])} détectés")
print(f"  - Formulaires  : {len(scrape_result['forms'])}")
print(f"  - Liens        : {len(scrape_result['links'])}")

# Détection trackers
print(f"\n🔍 Trackers de données détectés :")
trackers_found = [name for name, found in scrape_result['trackers'].items() if found]
if trackers_found:
    for tracker in trackers_found:
        print(f"  ⚠️  {tracker}")
else:
    print(f"  ✓ Aucun tracker détecté")

# Politique de confidentialité
print(f"\n📋 Politique de confidentialité :")
if scrape_result['privacy_policy_link']:
    print(f"  ✓ Trouvée : {scrape_result['privacy_policy_link']}")
else:
    print(f"  ✗ Non trouvée")

# Mentions RGPD
print(f"\n🔐 Conformité RGPD :")
print(f"  - Cookies mentionnés : {'✓ Oui' if scrape_result['cookies_mentioned'] else '✗ Non'}")
if scrape_result['rgpd_keywords']:
    print(f"  - Mots-clés RGPD : {', '.join(scrape_result['rgpd_keywords'])}")

# 3. Analyse NLP du texte
print(f"\n🤖 Étape 3 : Analyse NLP du contenu textuel")
print("-" * 80)

preprocessor = NLPPreprocessor()
nlp_result = preprocessor.analyze_text(scrape_result['text_content'][:5000])  # Limite à 5000 chars

print(f"✓ Analyse NLP terminée")
print(f"  - Tokens           : {nlp_result['total_tokens']}")
print(f"  - Données sensibles: {'✓ Détectées' if nlp_result['has_sensitive_data'] else '✗ Non détectées'}")
print(f"  - Données perso    : {'✓ Détectées' if nlp_result['has_personal_data'] else '✗ Non détectées'}")

# Entités nommées
if any(nlp_result['entities'].values()):
    print(f"\n  Entités nommées trouvées :")
    for entity_type, entities in nlp_result['entities'].items():
        if entities:
            print(f"    - {entity_type}: {', '.join(entities[:3])}")  # Limite à 3

# Données sensibles
if nlp_result['sensitive_data']:
    print(f"\n  ⚠️  Données sensibles détectées dans le texte :")
    for data_type, data_list in nlp_result['sensitive_data'].items():
        print(f"    - {data_type}: {len(data_list)} occurrence(s)")

# Mots fréquents
print(f"\n  Mots les plus fréquents :")
for word, freq in nlp_result['word_frequency'][:5]:
    print(f"    - {word}: {freq}")

# 4. Génération du résumé d'audit
print(f"\n" + "=" * 80)
print("📊 RÉSUMÉ DE L'AUDIT RGPD")
print("=" * 80)

# Score simple (à améliorer dans ai_report.py)
score = 100
issues = []

# Vérifications
if not scrape_result['privacy_policy_link']:
    score -= 30
    issues.append("❌ Absence de lien vers la politique de confidentialité")

if not scrape_result['cookies_mentioned']:
    score -= 20
    issues.append("❌ Aucune mention de cookies sur la page")

if trackers_found and not scrape_result['cookies_mentioned']:
    score -= 20
    issues.append("❌ Trackers détectés sans information sur les cookies")

if nlp_result['has_sensitive_data']:
    score -= 15
    issues.append("⚠️  Données sensibles détectées dans le contenu")

if not scrape_result['rgpd_keywords']:
    score -= 15
    issues.append("⚠️  Aucun mot-clé RGPD trouvé (RGPD, CNIL, consentement...)")

print(f"\n🎯 Score de conformité : {score}/100")
print(f"\n📋 Problèmes identifiés ({len(issues)}) :")
if issues:
    for issue in issues:
        print(f"  {issue}")
else:
    print(f"  ✓ Aucun problème majeur détecté")

print(f"\n" + "=" * 80)
print("✓ Audit terminé avec succès")
print("=" * 80)
