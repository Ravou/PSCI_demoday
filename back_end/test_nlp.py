from app.services.nlp_preprocessor import NLPPreprocessor, extract_rgpd_keywords

# instantiate the preprocessor so `preprocessor` is defined
preprocessor = NLPPreprocessor()

# Texte de test réaliste pour un site web
test_text = """
Bienvenue sur notre site web. Nous collectons vos données personnelles 
pour améliorer votre expérience utilisateur. En utilisant ce site, 
vous acceptez notre politique de confidentialité et l'utilisation de cookies.

Pour toute question, contactez notre DPO à dpo@monsite.fr ou 
au 01 42 68 53 00. Notre société est basée à Lyon et respecte 
le Règlement Général sur la Protection des Données (RGPD).

Vos informations (nom, prénom, adresse email, adresse IP) sont traitées 
de manière sécurisée. Vous disposez d'un droit d'accès, de rectification 
et de suppression de vos données.

Notre système enregistre automatiquement votre adresse IP (exemple: 192.168.1.100)
et utilise Google Analytics pour les statistiques de visite.
"""

print("=" * 70)
print("TEST DU NLP PREPROCESSOR - TEXTE RGPD")
print("=" * 70)

# Analyse complète
results = preprocessor.analyze_text(test_text)

print(f"\n📊 STATISTIQUES GÉNÉRALES")
print(f"{'─' * 70}")
print(f"Longueur texte original    : {results['original_text_length']} caractères")
print(f"Longueur texte nettoyé     : {results['cleaned_text_length']} caractères")
print(f"Nombre total de tokens     : {results['total_tokens']}")
print(f"Tokens sans stopwords      : {results['tokens_without_stopwords']}")
print(f"Données sensibles trouvées : {'✓ OUI' if results['has_sensitive_data'] else '✗ NON'}")
print(f"Données personnelles       : {'✓ OUI' if results['has_personal_data'] else '✗ NON'}")

print(f"\n🏢 ENTITÉS NOMMÉES (NER)")
print(f"{'─' * 70}")
for entity_type, entities in results['entities'].items():
    if entities:
        print(f"{entity_type:12} : {', '.join(entities)}")

print(f"\n🔒 DONNÉES SENSIBLES DÉTECTÉES")
print(f"{'─' * 70}")
if results['sensitive_data']:
    for data_type, data_list in results['sensitive_data'].items():
        print(f"{data_type:15} : {', '.join(data_list)}")
else:
    print("Aucune donnée sensible détectée")

print(f"\n🔑 MOTS-CLÉS RGPD TROUVÉS")
print(f"{'─' * 70}")
keywords = extract_rgpd_keywords(test_text)
if keywords:
    print(f"{', '.join(keywords)}")
else:
    print("Aucun mot-clé RGPD trouvé")

print(f"\n📈 MOTS LES PLUS FRÉQUENTS (Top 15)")
print(f"{'─' * 70}")
for word, freq in results['word_frequency'][:15]:
    bar = '█' * freq
    print(f"{word:20} : {bar} ({freq})")

print(f"\n💾 TEXTE NETTOYÉ (extrait)")
print(f"{'─' * 70}")
print(results['cleaned_text'][:300] + "...")

print(f"\n{'=' * 70}")
print("✓ Test terminé avec succès")
print(f"{'=' * 70}")

