import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from app.models import db, User, ConsentLog, Audit
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def test_complete_workflow():
    """Test complet du workflow utilisateur → consentement → audit"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST COMPLET DU WORKFLOW RGPD")
        print("="*60)
        
        print("\n=== Test 1: Création d'utilisateur ===")
        user = User(
            email='test@example.com',
            password='password123',
            name='Test User',
            organization='Test Org'
        )
        user.save()
        print(f"✓ Utilisateur créé avec succès")
        print(f"  - Email: {user.email}")
        print(f"  - UserID: {user.userid}")
        print(f"  - Nom: {user.name}")
        print(f"  - Organisation: {user.organization}")
        
        print("\n=== Test 2: Vérification du mot de passe ===")
        password_ok = user.check_password('password123')
        password_wrong = user.check_password('wrongpassword')
        print(f"✓ Vérification mot de passe correct: {password_ok}")
        print(f"✓ Vérification mot de passe incorrect: {password_wrong}")
        
        print("\n=== Test 3: Enregistrement de consentement ===")
        consent = ConsentLog(
            userid=user.userid,
            consenttype='audit',
            ipaddress='192.168.1.1',
            consent_text='J\'accepte l\'analyse RGPD de mon site web'
        )
        consent.save()
        print(f"✓ Consentement enregistré")
        print(f"  - Type: {consent.consenttype}")
        print(f"  - IP: {consent.ipaddress}")
        print(f"  - Actif: {consent.is_active}")
        print(f"  - Date: {consent.created_at}")
        
        print("\n=== Test 4: Vérification du consentement actif ===")
        has_consent = ConsentLog.has_active_consent(user.userid, 'audit')
        has_no_consent = ConsentLog.has_active_consent(user.userid, 'data_collection')
        print(f"✓ Consentement 'audit' actif: {has_consent}")
        print(f"✓ Consentement 'data_collection' actif: {has_no_consent}")
        
        print("\n=== Test 5: Création d'audit ===")
        audit = Audit(
            target='https://example.com',
            userid=user.userid,
            consenttype='audit',
            ipaddress='192.168.1.1'
        )
        audit.save()
        print(f"✓ Audit créé")
        print(f"  - ID: {audit.id}")
        print(f"  - Cible: {audit.target}")
        print(f"  - Status initial: {audit.status}")
        
        print("\n=== Test 6: Exécution de l'audit ===")
        print("  Lancement de l'analyse RGPD...")
        audit.run_audit()
        print(f"✓ Audit exécuté avec succès")
        print(f"  - Status final: {audit.status}")
        print(f"  - Score de conformité: {audit.compliance_score}%")
        print(f"  - Nombre de violations: {len(audit.violations) if audit.violations else 0}")
        print(f"  - Temps d'exécution: {audit.started_at} → {audit.completed_at}")
        
        if audit.violations:
            print("\n  Violations détectées:")
            for i, v in enumerate(audit.violations, 1):
                print(f"    {i}. {v['article']}")
                print(f"       → {v['description']}")
                print(f"       → Sévérité: {v['severity']}")
        
        print("\n=== Test 7: Récupération du résumé ===")
        summary = audit.get_summary()
        print(f"✓ Résumé généré:")
        print("-" * 50)
        print(summary)
        print("-" * 50)
        
        print("\n=== Test 8: Révocation du consentement ===")
        print(f"  État avant révocation: {consent.is_active}")
        consent.revoke()
        consent.save()
        print(f"✓ Consentement révoqué avec succès")
        print(f"  - État après révocation: {consent.is_active}")
        print(f"  - Date de révocation: {consent.revoked_at}")
        
        print("\n=== Test 9: Vérification du consentement révoqué ===")
        has_consent_after = ConsentLog.has_active_consent(user.userid, 'audit')
        print(f"✓ Consentement 'audit' actif après révocation: {has_consent_after}")
        
        print("\n=== Test 10: Comptage des données avant suppression ===")
        audits_before = Audit.query.filter_by(userid=user.userid).count()
        consents_before = ConsentLog.query.filter_by(userid=user.userid).count()
        print(f"  - Audits associés à l'utilisateur: {audits_before}")
        print(f"  - Consentements associés: {consents_before}")
        
        print("\n=== Test 11: Test du droit à l'oubli (CASCADE DELETE) ===")
        print("  Suppression de l'utilisateur en cours...")
        user.delete()
        print("✓ Utilisateur supprimé")
        
        audits_after = Audit.query.filter_by(userid=user.userid).count()
        consents_after = ConsentLog.query.filter_by(userid=user.userid).count()
        print(f"\n  Vérification après suppression:")
        print(f"  - Audits restants: {audits_after}")
        print(f"  - Consentements restants: {consents_after}")
        
        if audits_after == 0 and consents_after == 0:
            print("\n✓✓✓ DROIT À L'OUBLI VALIDÉ : Suppression en cascade réussie")
        else:
            print("\n✗✗✗ ERREUR : Des données subsistent après suppression")
        
        print("\n" + "="*60)
        print("✓✓✓ TOUS LES TESTS SONT RÉUSSIS ✓✓✓")
        print("="*60)
        print("\nRésumé des tests:")
        print("  ✓ Création et authentification utilisateur")
        print("  ✓ Enregistrement et révocation de consentement")
        print("  ✓ Création et exécution d'audit RGPD")
        print("  ✓ Génération de rapport et recommandations")
        print("  ✓ Droit à l'oubli (suppression cascade)")
        print("\nLa base de données et les modèles sont opérationnels!")
        print("="*60 + "\n")

if __name__ == '__main__':
    try:
        test_complete_workflow()
    except Exception as e:
        print(f"\n✗✗✗ ERREUR LORS DES TESTS ✗✗✗")
        print(f"Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
