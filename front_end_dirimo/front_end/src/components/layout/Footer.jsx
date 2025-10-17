import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    mainPages: [
      { name: 'Home', path: '/' },
      { name: 'About', path: '/about' },
      { name: 'Services', path: '/services' },
      { name: 'Contact', path: '/contact' }
    ],
    supportPages: [
      { name: 'Contact Us', path: '/contact' },
      { name: 'Terms & Conditions', path: '/terms' },
      { name: 'Privacy Policy', path: '/privacy' },
      { name: 'Documentation', path: 'http://localhost:5000/docs', external: true }
    ]
  };

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Section Logo et Description */}
        <div className="footer-section footer-brand">
          <div className="footer-logo">
            <span className="footer-logo-icon">⚡</span>
            <span className="footer-logo-text">PSCI</span>
          </div>
          <p className="footer-description">
            Your trusted partner in professional and proactive GDPR compliance. 
            Automated audits, consent management, and detailed reporting.
          </p>
          <div className="footer-badge">
            <span className="badge-dot"></span>
            <span>24/7 Protection with Live Reporting</span>
          </div>
        </div>

        {/* Main Pages */}
        <div className="footer-section">
          <h4 className="footer-title">Main Pages</h4>
          <ul className="footer-links">
            {footerLinks.mainPages.map((link) => (
              <li key={link.path}>
                <Link to={link.path} className="footer-link">
                  {link.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Support Pages */}
        <div className="footer-section">
          <h4 className="footer-title">Support Pages</h4>
          <ul className="footer-links">
            {footerLinks.supportPages.map((link) => (
              <li key={link.path}>
                {link.external ? (
                  <a 
                    href={link.path}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="footer-link"
                  >
                    {link.name}
                  </a>
                ) : (
                  <Link to={link.path} className="footer-link">
                    {link.name}
                  </Link>
                )}
              </li>
            ))}
          </ul>
        </div>

        {/* Contact Us */}
        <div className="footer-section">
          <h4 className="footer-title">Contact Us</h4>
          <ul className="footer-contact">
            <li>123 Security Blvd, Dallas,</li>
            <li>TX 75201045</li>
            <li className="footer-contact-item">
              <a href="tel:+18005552214" className="footer-link">
                (800) 555-2214
              </a>
            </li>
            <li className="footer-contact-item">
              <a href="mailto:info@psci.com" className="footer-link">
                info@psci.com
              </a>
            </li>
          </ul>
        </div>
      </div>

      {/* Copyright */}
      <div className="footer-bottom">
        <div className="footer-bottom-container">
          <p className="footer-copyright">
            © {currentYear} PSCI. All rights reserved
          </p>
          <p className="footer-legal">
            GDPR Compliance Audit Application
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

