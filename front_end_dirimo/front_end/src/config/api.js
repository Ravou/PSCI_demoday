const API_CONFIG = {
  // URL de base de l'API (avec le préfixe /api)
  BASE_URL: (process.env.REACT_APP_API_URL || 'http://localhost:5000') + '/api',

  // Endpoints de l'API Flask-RESTX
  ENDPOINTS: {
    // System
    HEALTH: '/health',

    // Users
    REGISTER: '/users/register',       // POST /api/users/register
    LOGIN: '/users/login',             // POST /api/users/login
    USER_PROFILE: '/users/',           // GET /api/users/{user_id}
    UPDATE_PROFILE: '/users',          // PUT /api/users/{user_id} (compléter dans l'appel)
    DELETE_USER: '/users',             // DELETE /api/users/{user_id}
    USER_AUDITS: '/audits',            // GET /api/audits/{user_id}/audits
    USER_CONSENTS: '/consents',        // GET /api/consents/{user_id}

    // Consents
    CONSENT_RECORD: '/consents/',      // POST /api/consents/
    CONSENT_REVOKE: '/consents/revoke',
    CONSENT_LIST: '/consents',         // GET /api/consents/{user_id}
    CONSENT_VERIFY: '/consents/verify',

    // Audits
    AUDIT_CREATE: '/audits',           // POST /api/audits/{user_id}/audits
    AUDIT_LIST: '/audits',             // GET /api/audits/{user_id}/audits
    AUDIT_DETAIL: '/audits',           // GET /api/audits/{audit_id} si implémenté
    AUDIT_RUN: '/audits',              // POST /api/audits/{audit_id}/run
    AUDIT_SUMMARY: '/audits',          // GET /api/audits/{audit_id}/summary
    AUDIT_DELETE: '/audits'            // DELETE /api/audits/{audit_id} si implémenté
  }
};

export default API_CONFIG;


