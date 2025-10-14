import React from 'react';

const AboutUs = () => {
  return (
    <section id="about" style={{
      padding: '100px 40px',
      maxWidth: '1400px',
      margin: '0 auto',
      position: 'relative'
    }}>
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
              86%
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

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '60px',
        maxWidth: '1000px',
        margin: '0 auto',
        textAlign: 'center'
      }}>
        <div>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--vert-neon)',
            marginBottom: '10px'
          }}>
            600+
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
            1,600+
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
            800+
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
    </section>
  );
};

export default AboutUs;
