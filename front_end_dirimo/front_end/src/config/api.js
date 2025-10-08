const API_CONFIG = {
  // URL de base de l'API
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // Endpoints de l'API Flask-RESTX
  ENDPOINTS: {
    // System
    HEALTH: '/health',
    
    // Users (Flask-RESTX : /users/)
    REGISTER: '/users/',
    LOGIN: '/users/',  // Pas de route /login dans Flask-RESTX, on utilise GET /users/
    USER_PROFILE: '/users/',
    UPDATE_PROFILE: '/users',
    DELETE_USER: '/users',
    USER_AUDITS: '/audits',  // GET /audits/{userid}/audits
    USER_CONSENTS: '/consents',  // GET /consents/{userid}
    
    // Consents (Flask-RESTX : /consents/)
    CONSENT_RECORD: '/consents/',
    CONSENT_REVOKE: '/consents/revoke',
    CONSENT_LIST: '/consents',
    CONSENT_VERIFY: '/consents/verify',
    
    // Audits (Flask-RESTX : /audits/)
    AUDIT_CREATE: '/audits',  // POST /audits/{userid}/audits
    AUDIT_LIST: '/audits',
    AUDIT_DETAIL: '/audits',
    AUDIT_RUN: '/audits',  // POST /audits/{auditId}/run
    AUDIT_SUMMARY: '/audits',  // GET /audits/{auditId}/summary
    AUDIT_DELETE: '/audits'
  }
};

export default API_CONFIG;

