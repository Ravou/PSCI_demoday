import React from 'react';
import './Contact.css';



const Contact = () => {
  const founders = [
    {
      id: 1,
      name: 'Olivia',
      lastName: 'Letchy',
      title: 'Founder and Chief Technical Officer',
      description: 'Olivia Letchy is an expert in cybersecurity and data protection. With a master\'s degree in Information Systems Security, she has developed specialized expertise in GDPR compliance analysis and vulnerability detection. Passionate about technological innovation, she leads PSCI\'s technical development with a clear vision: to make digital security accessible to all.',
      linkedin: 'https://www.linkedin.com/in/olivia-letchy/'
    },
    {
      id: 2,
      name: 'Dirimo',
      lastName: 'Iriarte',
      title: 'Consultant and Developer',
      description: 'Dirimo Iriarte is an entrepreneur passionate about digital transformation and privacy protection. With extensive experience in innovative project management and full-stack application development, he is a PSCI consultant with a mission to revolutionize compliance auditing. His user-centric approach and strategic vision make him a recognized leader in the field of information technology.',
      linkedin: 'https://www.linkedin.com/in/dirimo-iriarte-1a00a0b5/'
    }
  ];

  return (
    <div className="contact-page">
      <div className="contact-container">
        <h1 className="contact-title">Contact</h1>
        <p className="contact-subtitle">
          Meet the founders of PSCI and learn more about our mission to simplify compliance auditing through innovative technology.
        </p>

        <div className="founders-grid">
          {founders.map((founder) => (
            <div key={founder.id} className="founder-card">
              <div className="founder-circle">
                <span className="founder-initial">{founder.name.charAt(0)}</span>
              </div>
              <h2 className="founder-name">{founder.name} {founder.lastName}</h2>
              <h3 className="founder-title">{founder.title}</h3>
              <p className="founder-description">{founder.description}</p>
              <a 
                href={founder.linkedin} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="social-link"
              >
                <span className="linkedin-icon">in</span>
              </a>
            </div>
          ))}
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

