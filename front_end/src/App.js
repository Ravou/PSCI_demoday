import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import AuditForm from './components/AuditForm';
import LandingPage from './components/LandingPage';
import './styles/theme.css';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

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

  const handleLoginSuccess = (userProfile) => {
    setUser(userProfile);
    localStorage.setItem('user', JSON.stringify(userProfile));
  };

  const handleLogout = () => {
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
        <nav>
          <div className="navbar-content">
            <Link to="/" className="logo">
              <span>PSCI</span>
            </Link>
            
            {/* Menu de navigation */}
            <div className="nav-menu">
              <Link to="/" className="nav-link">Home</Link>
              <a href="#features" className="nav-link">About Us</a>
              <a href="#footer" className="nav-link">Contact</a>
            </div>

            <div className="nav-right">
              {user ? (
                <>
                  <span className="user-name">
                    <strong>{user.name || user.email}</strong>
                  </span>
                  <Link to="/dashboard" className="btn btn-ghost">
                    Dashboard
                  </Link>
                  <button onClick={handleLogout} className="btn btn-primary">
                    Logout
                  </button>
                </>
              ) : (
                <Link to="/login" className="btn btn-primary">Sign In</Link>
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
            <Route 
              path="/dashboard" 
              element={
                user ? 
                  <AuditForm userid={user.id || user.userid} /> : 
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
            <a href="http://localhost:5000/docs" target="_blank" rel="noopener noreferrer">
            </a>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
