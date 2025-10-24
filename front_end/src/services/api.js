// src/services/api.js
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Configuration des headers par défaut
const defaultHeaders = {
  'Content-Type': 'application/json',
};

// Fonction helper pour gérer les erreurs
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Une erreur est survenue');
  }
  return response.json();
};

// API User endpoints
export const userAPI = {
  // Register un nouvel utilisateur
  register: async (name, email, password) => {
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({
        name,
        email,
        password,
        consent_given: true
      })
    });
    return handleResponse(response);
  },

  // Login utilisateur
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify({
        email,
        password
      })
    });
    return handleResponse(response);
  },

  // Récupérer tous les utilisateurs
  getAllUsers: async () => {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: 'GET',
      headers: defaultHeaders,
    });
    return handleResponse(response);
  },

  // Récupérer un utilisateur par ID
  getUserById: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'GET',
      headers: defaultHeaders,
    });
    return handleResponse(response);
  },

  // Mettre à jour un utilisateur
  updateUser: async (userId, name, email, password) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: defaultHeaders,
      body: JSON.stringify({
        name,
        email,
        password,
        consent_given: true
      })
    });
    return handleResponse(response);
  },

  // Supprimer un utilisateur
  deleteUser: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    return handleResponse(response);
  }
};

// API Audit endpoints (à développer plus tard)
export const auditAPI = {
  createAudit: async (userId, siteUrl, consentText) => {
    const response = await fetch(`${API_BASE_URL}/audit/${userId}/audits`, {
      method: 'POST',
      headers: defaultHeaders,
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
      headers: defaultHeaders,
    });
    return handleResponse(response);
  }
};

