import time
from app.services.nlp_preprocessor import preprocessor

# Texte de différentes tailles
short_text = "Ce site utilise des cookies et collecte vos données."
medium_text = short_text * 10
long_text = short_text * 100

texts = [
    ("Court (50 mots)", short_text),
    ("Moyen (500 mots)", medium_text),
    ("Long (5000 mots)", long_text)
]

print("=" * 70)
print("TEST DE PERFORMANCE DU PREPROCESSOR")
print("=" * 70)

for name, text in texts:
    start = time.time()
    results = preprocessor.analyze_text(text)
    duration = time.time() - start
    
    print(f"\n{name}")
    print(f"  Temps d'exécution : {duration:.3f} secondes")
    print(f"  Tokens traités    : {results['total_tokens']}")
    print(f"  Tokens/seconde    : {results['total_tokens']/duration:.0f}")
