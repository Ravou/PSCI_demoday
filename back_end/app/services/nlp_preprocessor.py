"""
NLP Preprocessor - Préparation et nettoyage de textes pour analyse RGPD

Ce module fournit des fonctions pour :
- Nettoyer le texte (ponctuation, caractères spéciaux)
- Tokeniser (découper en mots)
- Supprimer les stopwords (mots courants inutiles)
- Identifier les entités nommées (personnes, organisations, dates)
- Détecter des patterns RGPD (emails, numéros de téléphone, adresses IP)
"""

import re
import string
from typing import List, Dict, Tuple, Optional
import spacy
from collections import Counter

# Charger le modèle français de spaCy pour NER
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    print("⚠️ Modèle français spaCy non trouvé. Installation...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "fr_core_news_sm"])
    nlp = spacy.load("fr_core_news_sm")

# Stopwords français courants
FRENCH_STOPWORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
    'donc', 'car', 'ni', 'que', 'qui', 'quoi', 'dont', 'où', 'ce', 'cet',
    'cette', 'ces', 'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes',
    'ses', 'notre', 'votre', 'leur', 'nos', 'vos', 'leurs', 'je', 'tu',
    'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'on', 'me', 'te', 'se',
    'lui', 'moi', 'toi', 'soi', 'en', 'y', 'à', 'au', 'aux', 'dans', 'par',
    'pour', 'sur', 'avec', 'sans', 'sous', 'vers', 'chez', 'être', 'avoir',
    'faire', 'dire', 'aller', 'voir', 'savoir', 'pouvoir', 'falloir', 'vouloir'
}

# Patterns regex pour détecter des données RGPD sensibles
PATTERNS_RGPD = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'telephone': r'\b(?:0|\+33)[1-9](?:[0-9]{2}){4}\b',
    'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'carte_credit': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
    'secu_sociale': r'\b[12]\d{2}(?:0[1-9]|1[0-2])\d{2}\d{3}\d{3}\d{2}\b',
    'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
}


class NLPPreprocessor:
    """
    Classe principale pour le preprocessing NLP
    """
    
    def __init__(self):
        """Initialise le preprocessor avec le modèle spaCy"""
        self.nlp = nlp
        self.stopwords = FRENCH_STOPWORDS
    
    def clean_text(self, text: str) -> str:
        """
        Nettoie le texte brut
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé (minuscules, sans ponctuation excessive)
        """
        if not text:
            return ""
        
        # Convertir en minuscules
        text = text.lower()
        
        # Supprimer les URLs (on les détectera séparément si nécessaire)
        text = re.sub(PATTERNS_RGPD['url'], ' URL ', text)
        
        # Supprimer les caractères spéciaux excessifs (garder les points, virgules)
        text = re.sub(r'[^\w\s.,!?;:\-\'\"àâäéèêëïîôùûüÿçæœ]', ' ', text)
        
        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text: str, remove_stopwords: bool = False) -> List[str]:
        """
        Découpe le texte en tokens (mots)
        
        Args:
            text: Texte à tokeniser
            remove_stopwords: Si True, supprime les stopwords
            
        Returns:
            Liste de tokens
        """
        # Utilise spaCy pour tokeniser intelligemment
        doc = self.nlp(text)
        
        tokens = [token.text for token in doc if not token.is_space]
        
        if remove_stopwords:
            tokens = [token for token in tokens if token.lower() not in self.stopwords]
        
        return tokens
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extrait les entités nommées (NER - Named Entity Recognition)
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les entités par type (PER, ORG, LOC, DATE, etc.)
        """
        doc = self.nlp(text)
        
        entities = {
            'PERSON': [],      # Personnes
            'ORG': [],         # Organisations
            'LOC': [],         # Lieux
            'DATE': [],        # Dates
            'MISC': []         # Divers
        }
        
        for ent in doc.ents:
            entity_type = ent.label_
            entity_text = ent.text
            
            if entity_type == 'PER':
                entities['PERSON'].append(entity_text)
            elif entity_type == 'ORG':
                entities['ORG'].append(entity_text)
            elif entity_type == 'LOC':
                entities['LOC'].append(entity_text)
            elif entity_type in ['DATE', 'TIME']:
                entities['DATE'].append(entity_text)
            else:
                entities['MISC'].append(entity_text)
        
        # Supprimer les doublons
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def detect_sensitive_data(self, text: str) -> Dict[str, List[str]]:
        """
        Détecte les données sensibles RGPD (emails, téléphones, IPs, etc.)
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les données sensibles détectées
        """
        sensitive_data = {}
        
        for data_type, pattern in PATTERNS_RGPD.items():
            matches = re.findall(pattern, text)
            if matches:
                sensitive_data[data_type] = list(set(matches))  # Supprimer doublons
        
        return sensitive_data
    
    def get_word_frequency(self, text: str, top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Calcule la fréquence des mots (utile pour analyser le vocabulaire RGPD)
        
        Args:
            text: Texte à analyser
            top_n: Nombre de mots les plus fréquents à retourner
            
        Returns:
            Liste de tuples (mot, fréquence)
        """
        # Tokenize et supprime stopwords
        tokens = self.tokenize(text, remove_stopwords=True)
        
        # Compte les occurrences
        word_freq = Counter(tokens)
        
        # Retourne les top_n plus fréquents
        return word_freq.most_common(top_n)
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyse complète du texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec toutes les analyses
        """
        # Nettoie le texte
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        tokens_no_stop = self.tokenize(cleaned_text, remove_stopwords=True)
        
        # Extrait entités nommées
        entities = self.extract_entities(text)
        
        # Détecte données sensibles
        sensitive_data = self.detect_sensitive_data(text)
        
        # Calcule fréquence des mots
        word_freq = self.get_word_frequency(cleaned_text)
        
        return {
            'original_text_length': len(text),
            'cleaned_text': cleaned_text,
            'cleaned_text_length': len(cleaned_text),
            'total_tokens': len(tokens),
            'tokens_without_stopwords': len(tokens_no_stop),
            'entities': entities,
            'sensitive_data': sensitive_data,
            'word_frequency': word_freq,
            'has_sensitive_data': len(sensitive_data) > 0,
            'has_personal_data': len(entities['PERSON']) > 0 or 'email' in sensitive_data
        }


# Instance globale du preprocessor
preprocessor = NLPPreprocessor()


def preprocess_text(text: str) -> Dict:
    """
    Fonction utilitaire pour préprocesser un texte
    
    Args:
        text: Texte à préprocesser
        
    Returns:
        Résultats de l'analyse NLP
    """
    return preprocessor.analyze_text(text)


def extract_rgpd_keywords(text: str) -> List[str]:
    """
    Extrait les mots-clés liés au RGPD
    
    Args:
        text: Texte à analyser
        
    Returns:
        Liste de mots-clés RGPD trouvés
    """
    rgpd_keywords = [
        'cookie', 'donnée', 'données', 'personnel', 'personnelle', 'vie privée',
        'consentement', 'rgpd', 'gdpr', 'cnil', 'traitement', 'collecte',
        'protection', 'confidentialité', 'politique', 'utilisateur', 'tracking',
        'analytics', 'statistique', 'publicitaire', 'tracker', 'identifiant'
    ]
    
    tokens = preprocessor.tokenize(text.lower())
    found_keywords = [token for token in tokens if token in rgpd_keywords]
    
    return list(set(found_keywords))


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    # Texte de test
    test_text = """
    Ce site collecte vos données personnelles via des cookies. 
    Contactez-nous à contact@example.com ou au 01 23 45 67 89.
    Notre organisation est située à Paris et respecte la CNIL.
    Votre adresse IP 192.168.1.1 est enregistrée.
    """
    
    print("=== Test du NLP Preprocessor ===\n")
    
    # Analyse complète
    results = preprocessor.analyze_text(test_text)
    
    print(f"Longueur texte original : {results['original_text_length']}")
    print(f"Longueur texte nettoyé : {results['cleaned_text_length']}")
    print(f"Nombre de tokens : {results['total_tokens']}")
    print(f"Tokens sans stopwords : {results['tokens_without_stopwords']}")
    
    print(f"\n=== Entités nommées ===")
    for entity_type, entities in results['entities'].items():
        if entities:
            print(f"{entity_type}: {', '.join(entities)}")
    
    print(f"\n=== Données sensibles détectées ===")
    for data_type, data_list in results['sensitive_data'].items():
        print(f"{data_type}: {', '.join(data_list)}")
    
    print(f"\n=== Mots-clés RGPD ===")
    keywords = extract_rgpd_keywords(test_text)
    print(f"{', '.join(keywords)}")
    
    print(f"\n=== Mots les plus fréquents ===")
    for word, freq in results['word_frequency'][:10]:
        print(f"{word}: {freq}")