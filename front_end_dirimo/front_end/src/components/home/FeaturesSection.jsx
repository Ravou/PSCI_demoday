import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';
import Card from '../common/Card';
import './FeaturesSection.css';

const FeatureCard = ({ icon, title, description, delay = 0 }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay }}
    >
      <Card variant="highlight" hoverable glowEffect>
        <div className="feature-icon">{icon}</div>
        <h3 className="feature-title">{title}</h3>
        <p className="feature-description">{description}</p>
      </Card>
    </motion.div>
  );
};

const FeaturesSection = () => {
  const features = [
    {
      icon: '🔍',
      title: 'GDPR Audits',
      description: 'Automated scanning, scoring, and actionable recommendations with versioned reports and compliance tracking.'
    },
    {
      icon: '✓',
      title: 'Consent Flows',
      description: 'Flexible consent policies with easy revocation, immutable logs, and full evidence retention for audits.'
    },
    {
      icon: '🔒',
      title: 'Secure by Design',
      description: 'JWT authentication, bcrypt password hashing, and least-privilege API access ready for production deployment.'
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
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={index * 0.15}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;

