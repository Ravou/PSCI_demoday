import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AboutUs from './components/AboutUs';
import Contact from './components/Contact';
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
        console.error('Error parsing user:', error);
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
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <nav>
          <div style={{
            position: 'relative',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            maxWidth: '1400px',
            margin: '0 auto',
            padding: '20px 40px'
          }}>
            <div style={{
              position: 'relative',
              display: 'inline-block'
            }}>
              <Link to="/" style={{
                position: 'relative',
                fontSize: '28px',
                fontWeight: '900',
                color: 'var(--vert-neon)',
                textDecoration: 'none',
                textTransform: 'uppercase',
                letterSpacing: '2px',
                textShadow: '0 0 30px rgba(0, 255, 136, 1), 0 0 60px rgba(0, 255, 136, 0.8), 0 0 90px rgba(0, 255, 136, 0.6)',
                transition: 'all 0.3s',
                zIndex: 2
              }}
              onMouseEnter={(e) => {
                e.target.style.textShadow = '0 0 40px rgba(0, 255, 136, 1), 0 0 80px rgba(0, 255, 136, 0.9), 0 0 120px rgba(0, 255, 136, 0.7)';
              }}
              onMouseLeave={(e) => {
                e.target.style.textShadow = '0 0 30px rgba(0, 255, 136, 1), 0 0 60px rgba(0, 255, 136, 0.8), 0 0 90px rgba(0, 255, 136, 0.6)';
              }}>
                PSCI
              </Link>
              
              <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '200px',
                height: '200px',
                background: 'radial-gradient(circle, rgba(0, 255, 136, 0.35) 0%, rgba(0, 255, 136, 0.2) 40%, transparent 70%)',
                borderRadius: '50%',
                filter: 'blur(30px)',
                zIndex: -1,
                pointerEvents: 'none',
                animation: 'pulse 2.5s ease-in-out infinite'
              }}></div>
            </div>

            <div style={{
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              gap: '35px'
            }}>
              <Link to="/" className="nav-link" style={{
                color: 'var(--texte-gris)',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: '15px',
                transition: 'all 0.3s',
                position: 'relative'
              }}>
                Home
              </Link>
              <Link to="/dashboard" className="nav-link" style={{
                color: 'var(--texte-gris)',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: '15px',
                transition: 'all 0.3s',
                position: 'relative'
              }}>
                Dashboard
              </Link>
              <Link to="/about" className="nav-link" style={{
                color: 'var(--texte-gris)',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: '15px',
                transition: 'all 0.3s',
                position: 'relative'
              }}>
                About Us
              </Link>
              <Link to="/contact" className="nav-link" style={{
                color: 'var(--texte-gris)',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: '15px',
                transition: 'all 0.3s',
                position: 'relative'
              }}>
                Contact
              </Link>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '25px'
            }}>
              {user ? (
                <>
                  <span style={{
                    color: 'var(--texte-blanc)',
                    fontWeight: '600',
                    padding: '10px 20px',
                    background: 'var(--gris-moyen)',
                    borderRadius: '8px',
                    border: '1px solid rgba(0, 255, 136, 0.2)'
                  }}>
                    <strong>{user.name || user.email}</strong>
                  </span>
                  <button onClick={handleLogout} style={{
                    padding: '12px 28px',
                    background: 'transparent',
                    color: 'var(--texte-gris)',
                    border: '2px solid var(--gris-moyen)',
                    borderRadius: '8px',
                    fontWeight: '700',
                    fontSize: '14px',
                    cursor: 'pointer',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    transition: 'all 0.3s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.color = 'var(--vert-neon)';
                    e.target.style.borderColor = 'var(--vert-neon)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.color = 'var(--texte-gris)';
                    e.target.style.borderColor = 'var(--gris-moyen)';
                  }}>
                    Logout
                  </button>
                </>
              ) : (
                <Link to="/register" style={{
                  padding: '12px 28px',
                  background: 'var(--vert-neon)',
                  color: 'var(--noir-profond)',
                  textDecoration: 'none',
                  borderRadius: '8px',
                  fontWeight: '700',
                  fontSize: '14px',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  boxShadow: '0 4px 15px rgba(0, 255, 136, 0.4)',
                  transition: 'all 0.3s',
                  display: 'inline-block'
                }}
                onMouseEnter={(e) => {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 6px 25px rgba(0, 255, 136, 0.6)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 4px 15px rgba(0, 255, 136, 0.4)';
                }}>
                  Get Started
                </Link>
              )}
            </div>
          </div>
        </nav>

        <main className="main-content-wrapper">
          <Routes>
            <Route path="/" element={user ? <Navigate to="/dashboard" replace /> : <LandingPage />} />
            <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <div className="main-content"><Login onLoginSuccess={handleLoginSuccess} /></div>} />
            <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <div className="main-content"><Register onRegisterSuccess={handleRegisterSuccess} /></div>} />
            <Route path="/dashboard" element={user ? <div className="main-content"><Dashboard userid={user.id || user.userid} /></div> : <Navigate to="/login" replace />} />
            <Route path="/about" element={<div className="main-content"><AboutUs /></div>} />
            <Route path="/contact" element={<div className="main-content"><Contact /></div>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

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
            <div>
              <h3 style={{
                color: 'var(--vert-principal)',
                marginBottom: '15px',
                fontSize: '20px',
                fontWeight: 'bold'
              }}>
                PSCI GDPR Audit
              </h3>
              <p style={{
                color: 'var(--gris-clair)',
                lineHeight: '1.6',
                fontSize: '14px'
              }}>
                Automated GDPR compliance analysis solution for businesses and organizations.
              </p>
            </div>

            <div>
              <h4 style={{
                color: 'var(--vert-secondaire)',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                Quick Access
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
                    fontSize: '14px'
                  }}>
                    Home
                  </Link>
                </li>
                <li style={{marginBottom: '10px'}}>
                  <Link to="/about" style={{
                    color: 'var(--gris-clair)',
                    textDecoration: 'none',
                    fontSize: '14px'
                  }}>
                    About Us
                  </Link>
                </li>
                <li style={{marginBottom: '10px'}}>
                  <Link to="/contact" style={{
                    color: 'var(--gris-clair)',
                    textDecoration: 'none',
                    fontSize: '14px'
                  }}>
                    Contact
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 style={{
                color: 'var(--vert-secondaire)',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                Our Services
              </h4>
              <ul style={{
                listStyle: 'none',
                padding: 0,
                margin: 0
              }}>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  Automated Audits
                </li>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  Artificial Intelligence
                </li>
                <li style={{marginBottom: '10px', color: 'var(--gris-clair)', fontSize: '14px'}}>
                  Detailed Reports
                </li>
              </ul>
            </div>

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
                    textDecoration: 'none'
                  }}>
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
                    textDecoration: 'none'
                  }}>
                  API Documentation
                </a>
              </p>
            </div>
          </div>

          <div style={{
            textAlign: 'center',
            marginTop: '40px',
            paddingTop: '20px',
            borderTop: '1px solid var(--gris-moyen)',
            color: 'var(--gris-clair)',
            fontSize: '14px'
          }}>
            © 2025 PSCI | GDPR Compliance Audit Application | All Rights Reserved
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;


