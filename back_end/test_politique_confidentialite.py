from app.services.nlp_preprocessor import preprocessor

# Exemple de politique de confidentialité
politique_text = """
POLITIQUE DE CONFIDENTIALITÉ

1. COLLECTE DES DONNÉES
Nous collectons les informations suivantes : nom, prénom, adresse email, 
numéro de téléphone, adresse postale et adresse IP.

2. UTILISATION DES COOKIES
Notre site utilise des cookies pour :
- Mémoriser vos préférences
- Analyser le trafic avec Google Analytics
- Afficher des publicités ciblées via Facebook Pixel

3. VOS DROITS
Conformément au RGPD, vous disposez des droits suivants :
- Droit d'accès à vos données
- Droit de rectification
- Droit à l'effacement (droit à l'oubli)
- Droit à la portabilité

4. CONTACT
Responsable de traitement : Entreprise XYZ SARL
DPO : Jean Dupont
Email : dpo@entreprise-xyz.fr
Téléphone : 01 23 45 67 89
Adresse : 10 rue de la République, 75001 Paris

5. SOUS-TRAITANTS
Nous partageons vos données avec :
- Google LLC (Analytics)
- Mailchimp (Newsletter)
- OVH (Hébergement)
"""

print("=" * 70)
print("ANALYSE D'UNE POLITIQUE DE CONFIDENTIALITÉ")
print("=" * 70)

# Analyse
results = preprocessor.analyze_text(politique_text)

print(f"\n✓ Données personnelles collectées trouvées : {results['has_personal_data']}")
print(f"✓ Présence de données sensibles : {results['has_sensitive_data']}")

print(f"\n🏢 Organisations mentionnées :")
for org in results['entities']['ORG']:
    print(f"  - {org}")

print(f"\n📧 Contacts trouvés :")
if 'email' in results['sensitive_data']:
    for email in results['sensitive_data']['email']:
        print(f"  - Email: {email}")
if 'telephone' in results['sensitive_data']:
    for tel in results['sensitive_data']['telephone']:
        print(f"  - Téléphone: {tel}")

print(f"\n👤 Personnes mentionnées :")
for person in results['entities']['PERSON']:
    print(f"  - {person}")

print(f"\n📍 Lieux mentionnés :")
for loc in results['entities']['LOC']:
    print(f"  - {loc}")

print(f"\n🔑 Termes RGPD importants :")
rgpd_terms = [word for word, freq in results['word_frequency'] 
              if word in ['données', 'rgpd', 'cookies', 'droit', 'traitement']]
for term in rgpd_terms:
    print(f"  - {term}")
