import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import AuditForm from './components/AuditForm';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Charger l'utilisateur depuis localStorage au démarrage
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Erreur parsing user:', error);
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  // Fonction appelée après connexion réussie (ADAPTÉ pour Login.jsx)
  const handleLoginSuccess = (userProfile) => {
    console.log('Utilisateur connecté:', userProfile);
    setUser(userProfile);
    localStorage.setItem('user', JSON.stringify(userProfile));
  };

  // Fonction appelée après inscription réussie (ADAPTÉ pour Register.jsx)
  const handleRegisterSuccess = (registeredUser) => {
    console.log('Utilisateur inscrit:', registeredUser);
    // Après inscription, rediriger vers login
    window.location.href = '/login';
  };

  // Fonction de déconnexion
  const handleLogout = () => {
    console.log('Déconnexion');
    setUser(null);
    localStorage.removeItem('user');
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Chargement...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <nav>
          <div className="navbar-content">
            <div className="logo">
                <span>PSCI</span>
            </div>
            
            <div className="nav-right">
              {user ? (
                <>
                  <span className="user-name">
                    Bienvenue, <strong>{user.name || user.email}</strong>
                  </span>
                  <button onClick={handleLogout} className="btn">
                    Déconnexion
                  </button>
                </>
              ) : (
                <div className="auth-buttons">
                  <Link to="/login" className="btn">Connexion</Link>
                  <Link to="/register" className="btn">Inscription</Link>
                </div>
              )}
            </div>
          </div>
        </nav>

        {/* Contenu principal */}
        <main className="main-content">
          <Routes>
            {/* Redirect racine */}
            <Route 
              path="/" 
              element={user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />} 
            />

            {/* Page de connexion - ADAPTÉ avec onLoginSuccess */}
            <Route 
              path="/login" 
              element={
                user ? 
                  <Navigate to="/dashboard" replace /> : 
                  <Login onLoginSuccess={handleLoginSuccess} />
              } 
            />

            {/* Page d'inscription - ADAPTÉ avec onRegisterSuccess */}
            <Route 
              path="/register" 
              element={
                user ? 
                  <Navigate to="/dashboard" replace /> : 
                  <Register onRegisterSuccess={handleRegisterSuccess} />
              } 
            />

            {/* Dashboard - ADAPTÉ avec userid au lieu de user */}
            <Route 
              path="/dashboard" 
              element={
                user ? 
                  <AuditForm userid={user.id || user.userid} /> : 
                  <Navigate to="/login" replace />
              } 
            />

            {/* Page 404 */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>© 2025 Projet PSCI | Application d'audit de conformité RGPD</p>
          <div className="footer-links">
            <a href="http://localhost:5000/docs" target="_blank" rel="noopener noreferrer">
              Documentation API Backend
            </a>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;


