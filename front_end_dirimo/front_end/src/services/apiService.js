import axios from 'axios';
import API_CONFIG from '../config/api';

// Instance axios configurée
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 secondes pour les audits
});

// Intercepteur pour ajouter des headers
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs globales
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userProfile');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ==================== USERS API ====================
export const userService = {
  // Inscription
  register: async (userData) => {
    try {
      console.log('=== DEBUG FRONTEND REGISTER ===');
      console.log('Data being sent:', userData);
      console.log('JSON stringified:', JSON.stringify(userData));
      console.log('API endpoint:', API_CONFIG.ENDPOINTS.REGISTER);
      console.log('Full URL:', `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.REGISTER}`);
      
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.REGISTER, userData);
      
      console.log('Response received:', response.data);
      console.log('Status:', response.status);
      console.log('================================\n');
      
      return response.data;
    } catch (error) {
      console.error('=== ERROR FRONTEND REGISTER ===');
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      console.error('Error message:', error.message);
      console.error('Full error:', error);
      console.error('================================\n');
      
      throw error.response?.data || { description: error.message };
    }
  },

  // Connexion (adapté pour Flask-RESTX)
  login: async (credentials) => {
    try {
      console.log('=== DEBUG FRONTEND LOGIN ===');
      console.log('Credentials:', { email: credentials.email, password: '***' });
      
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.LOGIN);
      const users = response.data;
      
      console.log('Users retrieved:', users.length);
      
      const user = users.find(u => u.email === credentials.email);
      
      if (user) {
        console.log('User found:', user.email);
        
        const loginResponse = {
          message: 'Connexion réussie',
          userprofile: user
        };
        

        localStorage.setItem('userProfile', JSON.stringify(user));
        
        console.log('Login successful');
        console.log('============================\n');
        
        return loginResponse;
      } else {
        console.error('User not found with email:', credentials.email);
        console.log('============================\n');
        throw { description: 'Email ou mot de passe incorrect' };
      }
    } catch (error) {
      console.error('=== ERROR FRONTEND LOGIN ===');
      console.error('Error:', error);
      console.error('============================\n');
      throw error.response?.data || { description: error.message };
    }
  },

  // Récupérer profil
  getProfile: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.USER_PROFILE}${userid}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  }
};

// ==================== CONSENTS API ====================
export const consentService = {
  // Enregistrer un consentement
  record: async (consentData) => {
    try {
      console.log('=== DEBUG CONSENT RECORD ===');
      console.log('Consent data:', consentData);
      
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_RECORD, consentData);
      
      console.log('Consent recorded:', response.data);
      console.log('============================\n');
      
      return response.data;
    } catch (error) {
      console.error('=== ERROR CONSENT RECORD ===');
      console.error('Error:', error.response?.data);
      console.error('============================\n');
      throw error.response?.data || { description: error.message };
    }
  },

  // ✅ AJOUT : Lister les consentements d'un utilisateur
  list: async (userId) => {
    try {
      console.log('=== DEBUG CONSENT LIST ===');
      console.log('User ID:', userId);
      
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.CONSENT_LIST}/${userId}`);
      
      console.log('Consents retrieved:', response.data);
      console.log('==========================\n');
      
      return response.data;
    } catch (error) {
      console.error('=== ERROR CONSENT LIST ===');
      console.error('Error:', error.response?.data);
      console.error('==========================\n');
      throw error.response?.data || { description: error.message };
    }
  },

  // Vérifier un consentement actif
  verify: async (userid, consenttype) => {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_VERIFY, {
        user_id: userid,
        consenttype: consenttype
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Révoquer un consentement
  revoke: async (userid, consenttype) => {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_REVOKE, {
        user_id: userid,
        consenttype
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  }

};

// ==================== AUDITS API ====================
export const auditService = {
  // Créer un audit
  create: async (auditData) => {
    try {
      console.log('=== DEBUG AUDIT CREATE ===');
      console.log('Audit data:', auditData);
      
      const response = await apiClient.post(
        `${API_CONFIG.ENDPOINTS.AUDIT_CREATE}/${auditData.userid}/audits`,
        {
          target: auditData.target,
          consent_id: auditData.consent_id
        }
      );
      
      console.log('Audit created:', response.data);
      console.log('==========================\n');
      
      return response.data;
    } catch (error) {
      console.error('=== ERROR AUDIT CREATE ===');
      console.error('Error:', error.response?.data);
      console.error('==========================\n');
      throw error.response?.data || { description: error.message };
    }
  },

  // Lister les audits d'un utilisateur
  list: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_LIST}/${userid}/audits`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Détail d'un audit
  get: async (auditId) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_DETAIL}/${auditId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Exécuter un audit
  run: async (auditId) => {
    try {
      console.log('=== DEBUG AUDIT RUN ===');
      console.log('Running audit ID:', auditId);
      
      const response = await apiClient.post(`${API_CONFIG.ENDPOINTS.AUDIT_RUN}/${auditId}/run`);
      
      console.log('Audit completed:', response.data);
      console.log('=======================\n');
      
      return response.data;
    } catch (error) {
      console.error('=== ERROR AUDIT RUN ===');
      console.error('Error:', error.response?.data);
      console.error('=======================\n');
      throw error.response?.data || { description: error.message };
    }
  },

  // Résumé d'un audit
  getSummary: async (auditId) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_SUMMARY}/${auditId}/summary`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Supprimer un audit
  delete: async (auditId) => {
    try {
      const response = await apiClient.delete(`${API_CONFIG.ENDPOINTS.AUDIT_DELETE}/${auditId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  }
};



export default apiClient;
