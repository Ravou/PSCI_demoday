import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';  // ✅ AJOUT
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

  const handleRegisterSuccess = () => {
    window.location.href = '/login';
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
        {/* Navbar avec logo PSCI */}
        <nav>
          <div className="navbar-content">
            <Link to="/" className="logo">
              <span>PSCI</span>
            </Link>
            <div className="nav-right">
              {user ? (
                <>
                  <Link to="/dashboard" className="nav-link">Dashboard</Link>
                  <span className="user-name">
                    <strong>{user.name || user.email}</strong>
                  </span>
                  <button onClick={handleLogout} className="btn">
                    Déconnexion
                  </button>
                </>
              ) : (
                <div className="auth-buttons">
                  <Link to="/login" className="btn btn-link">Connexion</Link>
                  <Link to="/register" className="btn btn-primary">Inscription</Link>
                </div>
              )}
            </div>
          </div>
        </nav>

        {/* Contenu principal */}
        <main className="main-content-wrapper">
          <Routes>
            <Route path="/" element={user ? <Navigate to="/dashboard" replace /> : <LandingPage />} />
            <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <div className="main-content"><Login onLoginSuccess={handleLoginSuccess} /></div>} />
            <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <div className="main-content"><Register onRegisterSuccess={handleRegisterSuccess} /></div>} />
            {/* ✅ MODIFICATION : Utiliser Dashboard au lieu de AuditForm */}
            <Route path="/dashboard" element={user ? <div className="main-content"><Dashboard userid={user.id || user.userid} /></div> : <Navigate to="/login" replace />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Footer amélioré */}
        <footer style={{
          background: 'var(--noir-fonce)',
          borderTop: '2px solid var(--vert-principal)',
          padding: '40px 20px',
          marginTop: '60px'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '40px'
          }}>
            {/* Colonne 1 : À propos */}
            <div>
              <h3 style={{
                color: 'var(--vert-principal)',
                marginBottom: '15px',
                fontSize: '20px',
                fontWeight: 'bold'
              }}>
                PSCI Audit RGPD
              </h3>
              <p style={{
                color: 'var(--gris-clair)',
                lineHeight: '1.6',
                fontSize: '14px'
              }}>
                Solution automatisée d'analyse de conformité RGPD pour entreprises et organisations.
              </p>
            </div>

            {/* Colonne 2 : Accès rapide */}
            <div>
              <h4 style={{
                color: 'var(--vert-secondaire)',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                Accès rapide
              </h4>
              <ul style={{
                listStyle: 'none',
                padding: 0,
                margin: 0
              }}>
                <li style={{marginBottom: '10px'}}>
                  <Link to="/" style={{
                    color: 'var(--gris-clair)',
                    textDecoration: 'none',
                    fontSize: '14px',
                    transition: 'color 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--vert-principal)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--gris-clair)'}
                  >
                    Accueil
                  </Link>
                </li>
                <li style={{marginBottom: '10px'}}>
                  <Link to="/register" style={{
                    color: 'var(--gris-clair)',
                    textDecoration: 'none',
                    fontSize: '14px',
                    transition: 'color 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--vert-principal)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--gris-clair)'}
                  >
                    Créer un compte
                  </Link>
                </li>
                <li style={{marginBottom: '10px'}}>
                  <Link to="/login" style={{
                    color: 'var(--gris-clair)',
                    textDecoration: 'none',
                    fontSize: '14px',
                    transition: 'color 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--vert-principal)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--gris-clair)'}
                  >
                    Se connecter
                  </Link>
                </li>
              </ul>
            </div>

            {/* Colonne 3 : Nos services */}
            <div>
              <h4 style={{
                color: 'var(--vert-secondaire)',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                Nos services
              </h4>
              <ul style={{
                listStyle: 'none',
                padding: 0,
                margin: 0
              }}>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  ✓ Audit automatisé
                </li>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  ✓ Intelligence artificielle
                </li>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  ✓ Rapports détaillés
                </li>
              </ul>
            </div>

            {/* Colonne 4 : Contact */}
            <div>
              <h4 style={{
                color: 'var(--vert-secondaire)',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                Contact
              </h4>
              <p style={{
                color: 'var(--gris-clair)',
                marginBottom: '10px',
                fontSize: '14px'
              }}>
                <a 
                  href="mailto:contact@psci.com"
                  style={{
                    color: 'var(--vert-principal)',
                    textDecoration: 'none',
                    transition: 'color 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--vert-secondaire)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--vert-principal)'}
                >
                  contact@psci.com
                </a>
              </p>
              <p style={{
                color: 'var(--gris-clair)',
                fontSize: '14px'
              }}>
                <a 
                  href="http://localhost:5000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    color: 'var(--vert-principal)',
                    textDecoration: 'none',
                    transition: 'color 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--vert-secondaire)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--vert-principal)'}
                >
                  📖 API Documentation
                </a>
              </p>
            </div>
          </div>

          {/* Copyright */}
          <div style={{
            textAlign: 'center',
            marginTop: '40px',
            paddingTop: '20px',
            borderTop: '1px solid var(--gris-moyen)',
            color: 'var(--gris-clair)',
            fontSize: '14px'
          }}>
            © 2025 PSCI | Application d'audit de conformité RGPD | Tous droits réservés
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;


