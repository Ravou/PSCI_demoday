import React from 'react';

const AboutUs = () => {
  return (
    <section id="about" style={{
      padding: '100px 40px',
      maxWidth: '1400px',
      margin: '0 auto',
      position: 'relative'
    }}>
      {/* Who We Are Section */}
      <div style={{textAlign: 'center', marginBottom: '80px'}}>
        <h2 style={{
          fontSize: '14px',
          color: 'var(--vert-neon)',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          marginBottom: '15px'
        }}>
          WHO WE ARE
        </h2>
        <h3 style={{
          fontSize: 'clamp(32px, 4vw, 48px)',
          fontWeight: '900',
          color: 'var(--texte-blanc)',
          marginBottom: '20px'
        }}>
          We Don't Just Defend.
          <br />
          We Adapt.
        </h3>
        <p style={{
          fontSize: '18px',
          color: 'var(--texte-gris)',
          maxWidth: '700px',
          margin: '0 auto',
          lineHeight: '1.7'
        }}>
          At PSCI, we believe GDPR threats don't sleep and neither should your defense. 
          We build intelligent, evolving security systems powered by AI and real-time data.
        </p>
      </div>

      {/* Stats Bars */}
      <div style={{
        maxWidth: '900px',
        margin: '0 auto 80px'
      }}>
        <div style={{marginBottom: '40px'}}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: '10px'
          }}>
            <span style={{
              color: 'var(--texte-gris)',
              fontSize: '14px',
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              REAL-TIME PROTECTION
            </span>
            <span style={{
              color: 'var(--vert-neon)',
              fontSize: '14px',
              fontWeight: '700'
            }}>
              99%
            </span>
          </div>
          <div style={{
            width: '100%',
            height: '8px',
            background: 'var(--gris-moyen)',
            borderRadius: '10px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: '99%',
              height: '100%',
              background: 'linear-gradient(90deg, var(--vert-neon) 0%, var(--vert-principal) 100%)',
              borderRadius: '10px',
              boxShadow: '0 0 20px rgba(0, 255, 136, 0.5)'
            }}></div>
          </div>
        </div>

        <div style={{marginBottom: '40px'}}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: '10px'
          }}>
            <span style={{
              color: 'var(--texte-gris)',
              fontSize: '14px',
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              TRUSTED DEFENSE
            </span>
            <span style={{
              color: 'var(--vert-neon)',
              fontSize: '14px',
              fontWeight: '700'
            }}>
              0%
            </span>
          </div>
          <div style={{
            width: '100%',
            height: '8px',
            background: 'var(--gris-moyen)',
            borderRadius: '10px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: '86%',
              height: '100%',
              background: 'linear-gradient(90deg, var(--vert-neon) 0%, var(--vert-principal) 100%)',
              borderRadius: '10px',
              boxShadow: '0 0 20px rgba(0, 255, 136, 0.5)'
            }}></div>
          </div>
        </div>
      </div>

      {/* Bottom Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '60px',
        maxWidth: '1000px',
        margin: '0 auto 100px',
        textAlign: 'center'
      }}>
        <div>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--vert-neon)',
            marginBottom: '10px'
          }}>
            0+
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            fontWeight: '600'
          }}>
            Attendees
          </div>
        </div>

        <div>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--vert-neon)',
            marginBottom: '10px'
          }}>
            0+
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            fontWeight: '600'
          }}>
            Project Complete
          </div>
        </div>

        <div>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--vert-neon)',
            marginBottom: '10px'
          }}>
            0+
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            fontWeight: '600'
          }}>
            Company Satisfied
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 204, 112, 0.05) 100%)',
        borderRadius: '20px',
        padding: '80px 40px',
        marginTop: '100px',
        border: '1px solid rgba(0, 255, 136, 0.2)'
      }}>
        <div style={{textAlign: 'center', marginBottom: '60px'}}>
          <h2 style={{
            fontSize: '14px',
            color: 'var(--vert-neon)',
            fontWeight: '700',
            textTransform: 'uppercase',
            letterSpacing: '2px',
            marginBottom: '15px'
          }}>
            OUR TEAM
          </h2>
          <h3 style={{
            fontSize: 'clamp(32px, 4vw, 48px)',
            fontWeight: '900',
            color: 'var(--texte-blanc)',
            marginBottom: '20px'
          }}>
            Meet The Team
          </h3>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '60px',
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          {/* Olivia Letchy */}
          <div style={{
            textAlign: 'center'
          }}>
            <div style={{
              width: '200px',
              height: '200px',
              borderRadius: '50%',
              margin: '0 auto 30px',
              background: 'linear-gradient(135deg, var(--vert-neon) 0%, var(--vert-principal) 100%)',
              padding: '5px',
              boxShadow: '0 10px 40px rgba(0, 255, 136, 0.3)'
            }}>
              <div style={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                background: 'var(--gris-fonce)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '48px',
                fontWeight: '900',
                color: 'var(--vert-neon)'
              }}>
                OL
              </div>
            </div>

            <h4 style={{
              fontSize: '28px',
              fontWeight: '800',
              color: 'var(--texte-blanc)',
              marginBottom: '10px'
            }}>
              Olivia Letchy
            </h4>
            
            <p style={{
              fontSize: '16px',
              color: 'var(--vert-neon)',
              fontWeight: '700',
              marginBottom: '20px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              Co-Founder & CEO
            </p>

            <p style={{
              fontSize: '15px',
              color: 'var(--texte-gris)',
              lineHeight: '1.7',
              marginBottom: '20px'
            }}>
              Graduate in Computer Science and specialized in Cybersecurity. 
              Olivia leads PSCI's vision and strategic direction with expertise in GDPR compliance solutions.
            </p>

            <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer" style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              background: 'rgba(0, 255, 136, 0.1)',
              border: '1px solid rgba(0, 255, 136, 0.3)',
              color: 'var(--vert-neon)',
              textDecoration: 'none',
              transition: 'all 0.3s',
              fontSize: '18px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'var(--vert-neon)';
              e.currentTarget.style.color = 'var(--noir-profond)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(0, 255, 136, 0.1)';
              e.currentTarget.style.color = 'var(--vert-neon)';
            }}>
              in
            </a>
          </div>

          {/* Dirimo Iriarte */}
          <div style={{
            textAlign: 'center'
          }}>
            <div style={{
              width: '200px',
              height: '200px',
              borderRadius: '50%',
              margin: '0 auto 30px',
              background: 'linear-gradient(135deg, var(--vert-neon) 0%, var(--vert-principal) 100%)',
              padding: '5px',
              boxShadow: '0 10px 40px rgba(0, 255, 136, 0.3)'
            }}>
              <div style={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                background: 'var(--gris-fonce)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '48px',
                fontWeight: '900',
                color: 'var(--vert-neon)'
              }}>
                DI
              </div>
            </div>

            <h4 style={{
              fontSize: '28px',
              fontWeight: '800',
              color: 'var(--texte-blanc)',
              marginBottom: '10px'
            }}>
              Dirimo Iriarte
            </h4>
            
            <p style={{
              fontSize: '16px',
              color: 'var(--vert-neon)',
              fontWeight: '700',
              marginBottom: '20px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              Co-Founder & CTO
            </p>

            <p style={{
              fontSize: '15px',
              color: 'var(--texte-gris)',
              lineHeight: '1.7',
              marginBottom: '20px'
            }}>
              Software engineer with expertise in backend development and AI systems. 
              Dirimo drives the technical innovation behind PSCI's automated compliance platform.
            </p>

            <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer" style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              background: 'rgba(0, 255, 136, 0.1)',
              border: '1px solid rgba(0, 255, 136, 0.3)',
              color: 'var(--vert-neon)',
              textDecoration: 'none',
              transition: 'all 0.3s',
              fontSize: '18px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'var(--vert-neon)';
              e.currentTarget.style.color = 'var(--noir-profond)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(0, 255, 136, 0.1)';
              e.currentTarget.style.color = 'var(--vert-neon)';
            }}>
              in
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutUs;
