import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard'; // ✅ Nouveau Dashboard
import Settings from './components/Settings'; // ✅ Nouvelle page Settings
import LandingPage from './components/LandingPage';
import './styles/theme.css';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // ✅ MODIFIÉ: Utilise localStorage directement au lieu de JSON.parse
    const userId = localStorage.getItem('user_id');
    const userName = localStorage.getItem('user_name');
    const userEmail = localStorage.getItem('user_email');

    if (userId) {
      setUser({
        id: userId,
        name: userName,
        email: userEmail
      });
    }
    setLoading(false);
  }, []);

  const handleLoginSuccess = (userProfile) => {
    setUser(userProfile);
    // ✅ MODIFIÉ: Stocke les données séparément
    localStorage.setItem('user_id', userProfile.id);
    localStorage.setItem('user_name', userProfile.name);
    localStorage.setItem('user_email', userProfile.email);
  };

  const handleLogout = () => {
    setUser(null);
    // ✅ MODIFIÉ: Supprime toutes les données utilisateur
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('user_email');
    localStorage.removeItem('auth_token');
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <nav className="nav">
          <div className="navbar-content">
            <Link to="/" className="logo">
              <span>PSCI</span>
            </Link>
            
            {/* Menu de navigation */}
            <div className="nav-menu">
              <Link to="/" className="nav-link">Home</Link>
              {user && <Link to="/dashboard" className="nav-link">Dashboard</Link>}
              {user && <Link to="/settings" className="nav-link">Settings</Link>}
              <a href="#features" className="nav-link">About Us</a>
              <a href="#footer" className="nav-link">Contact</a>
            </div>

            <div className="nav-right">
              {user ? (
                <>
                  <span className="user-name">
                    Welcome, <strong>{user.name || user.email}</strong>
                  </span>
                  <button onClick={handleLogout} className="btn btn-primary">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="btn btn-ghost">Sign In</Link>
                  <Link to="/register" className="btn btn-primary">Sign Up</Link>
                </>
              )}
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            
            <Route 
              path="/login" 
              element={
                user ? 
                  <Navigate to="/dashboard" replace /> : 
                  <Login onLoginSuccess={handleLoginSuccess} />
              } 
            />
            
            <Route 
              path="/register" 
              element={
                user ? 
                  <Navigate to="/dashboard" replace /> : 
                  <Register />
              } 
            />
            
            {/* ✅ MODIFIÉ: Utilise le nouveau Dashboard */}
            <Route 
              path="/dashboard" 
              element={
                user ? 
                  <Dashboard /> : 
                  <Navigate to="/login" replace />
              } 
            />

            {/* ✅ NOUVEAU: Route Settings */}
            <Route 
              path="/settings" 
              element={
                user ? 
                  <Settings /> : 
                  <Navigate to="/login" replace />
              } 
            />
            
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <footer className="footer" id="footer">
          <p>© 2025 Projet PSCI | All rights reserved</p>
          <div className="footer-links">
            <a href="mailto:contact@psci.com">contact@psci.com</a>
            <span> | </span>
            <Link to="/settings">Privacy Policy</Link>
            <span> | </span>
            <a href="http://localhost:5000/api/" target="_blank" rel="noopener noreferrer">
              API Docs
            </a>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
