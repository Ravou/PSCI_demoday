import React, { useState } from 'react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const [status, setStatus] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulation d'envoi
    setStatus('Message sent successfully!');
    setTimeout(() => setStatus(''), 3000);
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  return (
    <section id="contact" style={{
      padding: '100px 40px',
      maxWidth: '1400px',
      margin: '0 auto'
    }}>
      {/* Section Title */}
      <div style={{textAlign: 'center', marginBottom: '60px'}}>
        <h2 style={{
          fontSize: '14px',
          color: 'var(--vert-neon)',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          marginBottom: '15px'
        }}>
          GET IN TOUCH
        </h2>
        <h3 style={{
          fontSize: 'clamp(32px, 4vw, 48px)',
          fontWeight: '900',
          color: 'var(--texte-blanc)',
          marginBottom: '20px'
        }}>
          Contact Us
        </h3>
        <p style={{
          fontSize: '18px',
          color: 'var(--texte-gris)',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          Have questions about GDPR compliance? We're here to help.
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '60px',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {/* Contact Info */}
        <div>
          <h4 style={{
            fontSize: '24px',
            fontWeight: '700',
            color: 'var(--texte-blanc)',
            marginBottom: '30px'
          }}>
            Contact Information
          </h4>

          <div style={{marginBottom: '30px'}}>
            <div style={{
              fontSize: '16px',
              fontWeight: '700',
              color: 'var(--vert-neon)',
              marginBottom: '10px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              Email
            </div>
            <a href="mailto:contact@psci.com" style={{
              color: 'var(--texte-gris)',
              textDecoration: 'none',
              fontSize: '18px',
              transition: 'color 0.3s'
            }}
            onMouseEnter={(e) => e.target.style.color = 'var(--vert-neon)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--texte-gris)'}>
              contact@psci.com
            </a>
          </div>

          <div style={{marginBottom: '30px'}}>
            <div style={{
              fontSize: '16px',
              fontWeight: '700',
              color: 'var(--vert-neon)',
              marginBottom: '10px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              Support
            </div>
            <a href="mailto:support@psci.com" style={{
              color: 'var(--texte-gris)',
              textDecoration: 'none',
              fontSize: '18px',
              transition: 'color 0.3s'
            }}
            onMouseEnter={(e) => e.target.style.color = 'var(--vert-neon)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--texte-gris)'}>
              support@psci.com
            </a>
          </div>

          <div>
            <div style={{
              fontSize: '16px',
              fontWeight: '700',
              color: 'var(--vert-neon)',
              marginBottom: '10px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              Documentation
            </div>
            <a href="http://localhost:5000/docs" target="_blank" rel="noopener noreferrer" style={{
              color: 'var(--texte-gris)',
              textDecoration: 'none',
              fontSize: '18px',
              transition: 'color 0.3s'
            }}
            onMouseEnter={(e) => e.target.style.color = 'var(--vert-neon)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--texte-gris)'}>
              API Documentation
            </a>
          </div>
        </div>

        {/* Contact Form */}
        <div style={{
          background: 'rgba(26, 31, 46, 0.6)',
          border: '1px solid rgba(0, 255, 136, 0.2)',
          borderRadius: '16px',
          padding: '40px',
          backdropFilter: 'blur(10px)'
        }}>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Your name"
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="your.email@example.com"
              />
            </div>

            <div className="form-group">
              <label>Subject</label>
              <input
                type="text"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                required
                placeholder="Subject"
              />
            </div>

            <div className="form-group">
              <label>Message</label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
                rows="5"
                placeholder="Your message..."
                style={{resize: 'vertical'}}
              />
            </div>

            {status && (
              <div className="success-message">
                {status}
              </div>
            )}

            <button type="submit" className="btn btn-primary" style={{width: '100%'}}>
              Send Message
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Contact;

