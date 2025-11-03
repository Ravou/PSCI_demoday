import React from 'react';
import './Contact.css';

// Import des images (ajoute-les dans front_end/src/assets/)
import oliviaPhoto from '../assets/images/olivia.jpg';
import dirimoPhoto from '../assets/images/dirimo.jpg';

const Contact = () => {
  return (
    <div className="contact-page">
      <div className="contact-container">
        <h1 className="contact-title">Contact</h1>
        <p className="contact-subtitle">
          Meet the founders of PSCI and learn more about our mission to simplify compliance auditing through innovative technology.
        </p>

        <div className="founders-grid">
          {/* Olivia Letchy */}
          <div className="founder-card">
            <div className="founder-image-wrapper">
              <img src={oliviaPhoto} alt="Olivia Letchy" className="founder-image" />
            </div>
            <h2 className="founder-name">Olivia Letchy</h2>
            <h3 className="founder-title">Founder and Chief Technical Officer</h3>
            <p className="founder-description">
              Olivia Letchy is an expert in cybersecurity and data protection. 
              With a master's degree in Information Systems Security, she has developed 
              specialized expertise in GDPR compliance analysis and vulnerability detection
              Passionate about technological innovation, she leads 
              PSCI's technical development with a clear vision: to make digital security 
              accessible to all.
            </p>
            <a 
              href="https://www.linkedin.com/in/olivia-letchy" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="social-link"
            >
              <span className="linkedin-icon">in</span>
            </a>
          </div>

          {/* Dirimo Iriarte */}
          <div className="founder-card">
            <div className="founder-image-wrapper">
              <img src={dirimoPhoto} alt="Dirimo Iriarte" className="founder-image" />
            </div>
            <h2 className="founder-name">Dirimo Iriarte</h2>
            <h3 className="founder-title">Consultant and Developer</h3>
            <p className="founder-description">
              Dirimo Iriarte is an entrepreneur passionate about digital transformation and privacy protection.
              With extensive experience in innovative project management and full-stack application development,
              he is a PSCI consultant with a mission to revolutionize compliance auditing.
              His user-centric approach and strategic vision make him a recognized leader 
              in the field of information technology.
            </p>
            <a 
              href="https://www.linkedin.com/in/dirimo-iriarte-1a00a0b5/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="social-link"
            >
              <span className="linkedin-icon">in</span>
            </a>
          </div>
        </div>

        {/* Section Contact supplémentaire */}
        <div className="contact-info">
          <h3 className="contact-info-title">Contact - Information</h3>
          <div className="contact-details">
            <div className="contact-item">
              <span className="contact-icon">📧</span>
              <a href="mailto:contact@psci.com" className="contact-value">
                contact@psci.com
              </a>
            </div>
            <div className="contact-item">
              <span className="contact-icon">🌐</span>
              <a href="https://www.psci.com" target="_blank" rel="noopener noreferrer" className="contact-value">
                www.psci.com
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;

