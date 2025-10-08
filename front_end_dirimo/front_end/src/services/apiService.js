import axios from 'axios';
import API_CONFIG from '../config/api';

// Instance axios configurée
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
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
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.REGISTER, userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Connexion (ADAPTÉ pour Flask-RESTX)
  login: async (credentials) => {
    try {
      // Flask-RESTX n'a pas de route /login, on récupère tous les users et on filtre
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.LOGIN);
      const users = response.data;
      const user = users.find(u => u.email === credentials.email);
      
      if (user) {
        // Simuler une réponse de connexion
        const loginResponse = {
          message: 'Connexion réussie',
          userprofile: user
        };
        
        // Sauvegarder le profil utilisateur
        localStorage.setItem('userProfile', JSON.stringify(user));
        
        return loginResponse;
      } else {
        throw { description: 'Email ou mot de passe incorrect' };
      }
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Récupérer profil
  getProfile: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.USER_PROFILE}/${userid}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Mettre à jour profil
  updateProfile: async (userid, updates) => {
    try {
      const response = await apiClient.put(`${API_CONFIG.ENDPOINTS.UPDATE_PROFILE}/${userid}`, updates);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Supprimer compte
  deleteAccount: async (userid) => {
    try {
      const response = await apiClient.delete(`${API_CONFIG.ENDPOINTS.DELETE_USER}/${userid}`);
      localStorage.clear();
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Récupérer les audits de l'utilisateur
  getUserAudits: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.USER_AUDITS}/${userid}/audits`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Récupérer les consentements de l'utilisateur
  getUserConsents: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.USER_CONSENTS}/${userid}`);
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
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_RECORD, consentData);
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
  },

  // Lister les consentements
  list: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.CONSENT_LIST}/${userid}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Vérifier un consentement actif
  verify: async (userid, consenttype) => {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_VERIFY, {
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
      const response = await apiClient.post(`${API_CONFIG.ENDPOINTS.AUDIT_CREATE}/${auditData.userid}/audits`, {
        target: auditData.target,
        consent_id: '1'
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },

  // Lister les audits (avec filtres optionnels)
  list: async (filters = {}) => {
    try {
      const params = new URLSearchParams(filters).toString();
      const url = params ? `${API_CONFIG.ENDPOINTS.AUDIT_LIST}?${params}` : API_CONFIG.ENDPOINTS.AUDIT_LIST;
      const response = await apiClient.get(url);
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
      const response = await apiClient.post(`${API_CONFIG.ENDPOINTS.AUDIT_RUN}/${auditId}/run`);
      return response.data;
    } catch (error) {
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

// ==================== SYSTEM API ====================
export const systemService = {
  // Vérifier l'état du serveur
  healthCheck: async () => {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.HEALTH);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  }
};

export default apiClient;