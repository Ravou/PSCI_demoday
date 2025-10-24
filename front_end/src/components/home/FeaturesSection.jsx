import React from 'react';
import { motion } from 'framer-motion';
import photoAudit from '../../assets/images/photoaudit.jpg';
import photoIA from '../../assets/images/Photo-IA.jpg';
import photo5 from '../../assets/images/photo5.jpg';
import './FeaturesSection.css';

const FeaturesSection = () => {
  const features = [
    {
      title: 'GDPR Audits',
      description: 'Automated scanning, scoring, and actionable recommendations with versioned reports and compliance tracking.',
      image: photoAudit
    },
    {
      title: 'Consent Flows',
      description: 'Flexible consent policies with easy revocation, immutable logs, and full evidence retention for audits.',
      image: photoIA
    },
    {
      title: 'Secure by Design',
      description: 'JWT authentication, bcrypt password hashing, and least-privilege API access ready for production deployment.',
      image: photo5
    }
  ];

  return (
    <section id="features" className="features-section">
      <div className="features-container">
        <motion.div
          className="features-header"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="section-title">
            Proven Protection <span className="text-gradient">in Action</span>
          </h2>
          <p className="section-subtitle">
            At PSCI Security, we go beyond basic protection — we deliver strategic, 
            results-driven security tailored to your unique needs.
          </p>
        </motion.div>

        <div className="features-grid">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="feature-card"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
            >
              <div className="feature-image" style={{ backgroundImage: `url(${feature.image})` }}>
                <div className="feature-overlay" />
                <div className="feature-icon">{feature.icon}</div>
              </div>
              <div className="feature-content">
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
