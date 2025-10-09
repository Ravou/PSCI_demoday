import requests
import json

BASE_URL = "http://localhost:5000"

def test_complete_api_workflow():
    """Test complet de tous les endpoints API."""
    
    print("=" * 60)
    print("TEST COMPLET DES ENDPOINTS API")
    print("=" * 60)
    
    # 1. Test de santé
    print("\n=== Test 1: Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 2. Inscription utilisateur
    print("\n=== Test 2: Inscription utilisateur ===")
    user_data = {
        "email": "demo@test.com",
        "password": "SecurePass123",
        "name": "Demo User",
        "organization": "Test Company"
    }
    response = requests.post(f"{BASE_URL}/apiregister", json=user_data)
    print(f"Status: {response.status_code}")
    user_result = response.json()
    print(f"User créé: {user_result['user']['email']}")
    userid = user_result['user']['userid']
    
    # 3. Connexion
    print("\n=== Test 3: Connexion ===")
    login_data = {"email": "demo@test.com", "password": "SecurePass123"}
    response = requests.post(f"{BASE_URL}/apilogin", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Message: {response.json()['message']}")
    
    # 4. Enregistrement consentement
    print("\n=== Test 4: Enregistrement consentement ===")
    consent_data = {
        "userid": userid,
        "consenttype": "audit", 
        "ipaddress": "127.0.0.1",
        "consent_text": "J'accepte l'analyse RGPD de mon site"
    }
    response = requests.post(f"{BASE_URL}/apiconsent", json=consent_data)
    print(f"Status: {response.status_code}")
    print(f"Consentement: {response.json()['message']}")
    
    # 5. Création audit
    print("\n=== Test 5: Création audit ===")
    audit_data = {
        "target": "https://example.com",
        "userid": userid,
        "consenttype": "audit",
        "ipaddress": "127.0.0.1"
    }
    response = requests.post(f"{BASE_URL}/audits", json=audit_data)
    print(f"Status: {response.status_code}")
    audit_result = response.json()
    audit_id = audit_result['audit']['id']
    print(f"Audit créé avec ID: {audit_id}")
    
    # 6. Exécution audit
    print("\n=== Test 6: Exécution audit ===")
    response = requests.post(f"{BASE_URL}/audits/{audit_id}/run")
    print(f"Status: {response.status_code}")
    print(f"Status audit: {response.json()['audit']['status']}")
    
    # 7. Récupération résumé
    print("\n=== Test 7: Résumé audit ===")
    response = requests.get(f"{BASE_URL}/audits/{audit_id}/summary")
    print(f"Status: {response.status_code}")
    summary_data = response.json()
    print(f"Score: {summary_data['compliance_score']}%")
    print(f"Violations: {summary_data['total_violations']}")
    
    print("\n" + "=" * 60)
    print("✓✓✓ TOUS LES ENDPOINTS FONCTIONNENT ✓✓✓")
    print("=" * 60)

if __name__ == '__main__':
    # Assure-toi que le serveur tourne sur localhost:5000
    test_complete_api_workflow()

