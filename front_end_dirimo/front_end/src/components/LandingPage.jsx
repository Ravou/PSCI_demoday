import React from 'react';
import { Link } from 'react-router-dom';
import AboutUs from './AboutUs';
import Contact from './Contact';

const LandingPage = () => {
  return (
    <div style={{position: 'relative', zIndex: 1}}>
      {/* Hero Section */}
      <section style={{
        minHeight: '90vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '0 40px',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '600px',
          height: '600px',
          background: 'radial-gradient(circle, rgba(0, 255, 136, 0.15) 0%, transparent 70%)',
          borderRadius: '50%',
          filter: 'blur(40px)',
          zIndex: -1
        }}></div>

        <div style={{maxWidth: '900px'}}>
          <div style={{
            display: 'inline-block',
            marginBottom: '40px',
            position: 'relative'
          }}>
            <h1 style={{
              fontSize: 'clamp(60px, 8vw, 120px)',
              fontWeight: '900',
              letterSpacing: '8px',
              background: 'linear-gradient(135deg, #ffffff 0%, #00ff88 50%, #ffffff 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundSize: '200% auto',
              animation: 'shine 3s linear infinite',
              textShadow: '0 0 80px rgba(0, 255, 136, 0.5)',
              margin: 0
            }}>
              PSCI
            </h1>
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '120%',
              height: '120%',
              background: 'radial-gradient(circle, rgba(0, 255, 136, 0.3) 0%, transparent 70%)',
              filter: 'blur(30px)',
              zIndex: -1,
              animation: 'pulse 2s ease-in-out infinite'
            }}></div>
          </div>

          <div style={{
            display: 'inline-block',
            padding: '8px 20px',
            background: 'rgba(0, 255, 136, 0.1)',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '50px',
            color: 'var(--vert-neon)',
            fontSize: '13px',
            fontWeight: '700',
            textTransform: 'uppercase',
            letterSpacing: '2px',
            marginBottom: '30px'
          }}>
            CYBER SECURITY NO. #1
          </div>

          <h2 style={{
            fontSize: 'clamp(40px, 6vw, 72px)',
            fontWeight: '900',
            lineHeight: '1.1',
            marginBottom: '30px',
            background: 'linear-gradient(135deg, #ffffff 0%, #00ff88 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            GDPR Compliance
            <br />
            That Evolves
            <br />
            Daily.
          </h2>

          <p style={{
            fontSize: '18px',
            color: 'var(--texte-gris)',
            marginBottom: '40px',
            maxWidth: '700px',
            margin: '0 auto 40px'
          }}>
            An AI-powered automated system to verify your GDPR compliance. 
            Get detailed real-time reports and protect your data.
          </p>

          <div style={{
            display: 'flex',
            gap: '20px',
            justifyContent: 'center',
            flexWrap: 'wrap'
          }}>
            <Link to="/register" style={{
              padding: '16px 40px',
              background: 'var(--vert-neon)',
              color: 'var(--noir-profond)',
              textDecoration: 'none',
              borderRadius: '10px',
              fontWeight: '700',
              fontSize: '16px',
              textTransform: 'uppercase',
              letterSpacing: '1px',
              boxShadow: '0 4px 20px rgba(0, 255, 136, 0.4)',
              transition: 'all 0.3s',
              display: 'inline-block'
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = 'translateY(-3px)';
              e.target.style.boxShadow = '0 6px 30px rgba(0, 255, 136, 0.6)';
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = '0 4px 20px rgba(0, 255, 136, 0.4)';
            }}
            >
              Get Started Free
            </Link>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '40px',
            marginTop: '80px',
            maxWidth: '600px',
            margin: '80px auto 0'
          }}>
            <div>
              <div style={{
                fontSize: '36px',
                fontWeight: '900',
                color: 'var(--vert-neon)',
                marginBottom: '5px'
              }}>
                1,600+
              </div>
              <div style={{
                fontSize: '14px',
                color: 'var(--texte-gris)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Sites Audited
              </div>
            </div>

            <div>
              <div style={{
                fontSize: '36px',
                fontWeight: '900',
                color: 'var(--vert-neon)',
                marginBottom: '5px'
              }}>
                300+
              </div>
              <div style={{
                fontSize: '14px',
                color: 'var(--texte-gris)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Companies
              </div>
            </div>

            <div>
              <div style={{
                fontSize: '36px',
                fontWeight: '900',
                color: 'var(--vert-neon)',
                marginBottom: '5px'
              }}>
                99.9%
              </div>
              <div style={{
                fontSize: '14px',
                color: 'var(--texte-gris)',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Accuracy
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section style={{
        padding: '100px 40px',
        maxWidth: '1400px',
        margin: '0 auto'
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: '60px'
        }}>
          <h2 style={{
            fontSize: '14px',
            color: 'var(--vert-neon)',
            fontWeight: '700',
            textTransform: 'uppercase',
            letterSpacing: '2px',
            marginBottom: '15px'
          }}>
            OUR SERVICES
          </h2>
          <h3 style={{
            fontSize: 'clamp(32px, 4vw, 48px)',
            fontWeight: '900',
            color: 'var(--texte-blanc)',
            marginBottom: '20px'
          }}>
            Our Cybersecurity
            <br />
            Services at a Glance
          </h3>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '30px'
        }}>
          <div className="card" style={{
            position: 'relative',
            backgroundImage: 'url(/images/photoaudit.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '16px',
            padding: '50px 40px',
            minHeight: '420px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
            overflow: 'hidden',
            transition: 'all 0.3s',
            filter: 'brightness(1.2) contrast(1.05)'
          }}>
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(180deg, rgba(10, 14, 20, 0) 0%, rgba(10, 14, 20, 0.4) 100%)',
              zIndex: 0
            }}></div>

            <div style={{position: 'relative', zIndex: 1}}>
              <h4 style={{
                fontSize: '28px',
                fontWeight: '800',
                color: 'var(--texte-blanc)',
                marginBottom: '20px',
                textShadow: '0 2px 20px rgba(0, 0, 0, 0.95)'
              }}>
                Automated Audits
              </h4>
              <p style={{
                color: 'rgba(255, 255, 255, 0.95)',
                fontSize: '16px',
                lineHeight: '1.8',
                textShadow: '0 1px 10px rgba(0, 0, 0, 0.9)'
              }}>
                Complete and automatic analysis of your GDPR compliance in seconds thanks to our advanced AI.
              </p>
            </div>
          </div>

          <div className="card" style={{
            position: 'relative',
            backgroundImage: 'url(/images/Photo-IA.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '16px',
            padding: '50px 40px',
            minHeight: '420px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
            overflow: 'hidden',
            transition: 'all 0.3s',
            filter: 'brightness(1.5) contrast(1.2)'
          }}>
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(180deg, rgba(10, 14, 20, 0) 0%, rgba(10, 14, 20, 0.35) 100%)',
              zIndex: 0
            }}></div>

            <div style={{position: 'relative', zIndex: 1}}>
              <h4 style={{
                fontSize: '28px',
                fontWeight: '800',
                color: 'var(--texte-blanc)',
                marginBottom: '20px',
                textShadow: '0 2px 20px rgba(0, 0, 0, 0.95)'
              }}>
                Artificial Intelligence
              </h4>
              <p style={{
                color: 'rgba(255, 255, 255, 0.95)',
                fontSize: '16px',
                lineHeight: '1.8',
                textShadow: '0 1px 10px rgba(0, 0, 0, 0.9)'
              }}>
                Intelligent analysis system that continuously improves to detect all non-conformities.
              </p>
            </div>
          </div>

          <div className="card" style={{
            position: 'relative',
            backgroundImage: 'url(/images/photo5.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '16px',
            padding: '50px 40px',
            minHeight: '420px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
            overflow: 'hidden',
            transition: 'all 0.3s',
            filter: 'brightness(1.4) contrast(1.15)'
          }}>
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(180deg, rgba(10, 14, 20, 0) 0%, rgba(10, 14, 20, 0.35) 100%)',
              zIndex: 0
            }}></div>

            <div style={{position: 'relative', zIndex: 1}}>
              <h4 style={{
                fontSize: '28px',
                fontWeight: '800',
                color: 'var(--texte-blanc)',
                marginBottom: '20px',
                textShadow: '0 2px 20px rgba(0, 0, 0, 0.95)'
              }}>
                Detailed Reports
              </h4>
              <p style={{
                color: 'rgba(255, 255, 255, 0.95)',
                fontSize: '16px',
                lineHeight: '1.8',
                textShadow: '0 1px 10px rgba(0, 0, 0, 0.9)'
              }}>
                Receive complete reports with personalized recommendations to improve your compliance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* About Us Section */}
      <AboutUs />

      {/* Contact Section */}
      <Contact />
    </div>
  );
};

export default LandingPage;
