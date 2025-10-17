import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import Button from '../common/Button';
import Badge from '../common/Badge';
import './CTASection.css';

const CTASection = () => {
  return (
    <section className="cta-section">
      <div className="cta-gradient" aria-hidden="true" />
      
      <motion.div
        className="cta-container"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <Badge variant="primary" pulse>
          24/7 Protection with Live Reporting
        </Badge>

        <h2 className="cta-title">
          Your safety is our mission.
          <br />
          Your trust is our commitment.
        </h2>

        <p className="cta-subtitle">
          Click below to schedule your free risk assessment and learn 
          how we can help protect your world.
        </p>

        <div className="cta-actions">
          <Link to="/register">
            <Button variant="primary" size="xl">
              Start Protecting Your Presence
            </Button>
          </Link>
          <Link to="/contact">
            <Button variant="ghost" size="xl">
              Contact Us
            </Button>
          </Link>
        </div>

        {/* Decorative elements */}
        <div className="cta-glow cta-glow-1" aria-hidden="true" />
        <div className="cta-glow cta-glow-2" aria-hidden="true" />
      </motion.div>
    </section>
  );
};

export default CTASection;

