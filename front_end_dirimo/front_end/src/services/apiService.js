import axios from 'axios';
import API_CONFIG from '../config/api';

// Instance axios configurée
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000
});

// Intercepteur pour ajouter des headers
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
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

// Helpers d'auth
export const authService = {
  getToken: () => localStorage.getItem('authToken'),
  getUser: () => {
    const raw = localStorage.getItem('userProfile');
    try { return raw ? JSON.parse(raw) : null; } catch { return null; }
  },
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userProfile');
    window.location.href = '/login';
  }
};

// ==================== USERS API ====================
export const userService = {

  register: async (userData) => {
    try {

      const response = await apiClient.post(API_CONFIG.ENDPOINTS.REGISTER, userData);

      return response.data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


  login: async (credentials) => {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.LOGIN, {
        email: credentials.email,
        password: credentials.password
      });
      const data = response.data;

      if (data.token) localStorage.setItem('authToken', data.token);
      if (data.user) localStorage.setItem('userProfile', JSON.stringify(data.user));

      return data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


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

  record: async (consentData) => {
    try {

      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONSENT_RECORD, consentData);

      return response.data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


  list: async (userId) => {
    try {

      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.CONSENT_LIST}/${userId}`);

      return response.data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


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
  },


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

  create: async (auditData) => {
    try {

      const response = await apiClient.post(
        `${API_CONFIG.ENDPOINTS.AUDIT_CREATE}/${auditData.userid}/audits`,
        { target: auditData.target, consent_id: auditData.consent_id }
      );

      return response.data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


  list: async (userid) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_LIST}/${userid}/audits`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },


  get: async (auditId) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_DETAIL}/${auditId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },


  run: async (auditId) => {
    try {

      const response = await apiClient.post(`${API_CONFIG.ENDPOINTS.AUDIT_RUN}/${auditId}/run`);

      return response.data;
    } catch (error) {

      throw error.response?.data || { description: error.message };
    }
  },


  getSummary: async (auditId) => {
    try {
      const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.AUDIT_SUMMARY}/${auditId}/summary`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  },


  delete: async (auditId) => {
    try {
      const response = await apiClient.delete(`${API_CONFIG.ENDPOINTS.AUDIT_DELETE}/${auditId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { description: error.message };
    }
  }
};




