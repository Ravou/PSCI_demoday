// src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api';

// Configuration des headers par défaut avec token si disponible
const getHeaders = () => {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  const token = localStorage.getItem('auth_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
};

// Fonction helper pour gérer les erreurs
const handleResponse = async (response) => {
  if (!response.ok) {
    let errorMessage = 'Une erreur est survenue';
    try {
      const error = await response.json();
      errorMessage = error.error || error.message || errorMessage;
    } catch (e) {
      // Si la réponse n'est pas JSON, utiliser le message par défaut
    }
    throw new Error(errorMessage);
  }
  return response.json();
};

// API Auth endpoints
export const authAPI = {
  // Login utilisateur - ✅ CORRECTION: /auth/login au lieu de /users/login
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ email, password })
    });
    return handleResponse(response);
  }
};

// API User endpoints
export const userAPI = {
  // Register un nouvel utilisateur
  register: async (name, email, password, consent_given = true) => {
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ name, email, password, consent_given })
    });
    return handleResponse(response);
  },

  // Récupérer tous les utilisateurs
  getAllUsers: async () => {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  // Récupérer un utilisateur par ID
  getUserById: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  // Mettre à jour un utilisateur
  updateUser: async (userId, name, email, password = null) => {
    const body = { name, email, consent_given: true };
    if (password) {
      body.password = password;
    }
    
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(body)
    });
    return handleResponse(response);
  },

  // Supprimer un utilisateur
  deleteUser: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    return handleResponse(response);
  }
};

// API Audit endpoints
export const auditAPI = {
  createAudit: async (userId, siteUrl, consentText) => {
    const response = await fetch(`${API_BASE_URL}/audit/${userId}/audits`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        site_url: siteUrl,
        consent_text: consentText,
        run_nlp: true,
        run_semantic_matching: true,
        use_perplexity: false
      })
    });
    return handleResponse(response);
  },

  getAllAudits: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/audit/${userId}/audits`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  getAuditById: async (userId, auditId) => {
    const response = await fetch(`${API_BASE_URL}/audit/${userId}/audits/${auditId}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  }
};

export default { authAPI, userAPI, auditAPI };
