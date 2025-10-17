import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import Button from '../common/Button';
import Badge from '../common/Badge';
import './HeroSection.css';

const HeroSection = () => {
  return (
    <section className="hero-section">
      {/* Grille de fond animée */}
      <div className="hero-grid" aria-hidden="true" />
      
      {/* Halos lumineux */}
      <motion.div 
        className="hero-glow hero-glow-1"
        animate={{ 
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{ 
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div 
        className="hero-glow hero-glow-2"
        animate={{ 
          scale: [1, 1.1, 1],
          opacity: [0.2, 0.4, 0.2]
        }}
        transition={{ 
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1
        }}
      />

      <div className="hero-container">
        <motion.div
          className="hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {/* Badge */}
          <Badge variant="outline" pulse>
            Trusted Protection for Every Doorstep
          </Badge>

          {/* Titre principal */}
          <h1 className="hero-title">
            Reliable Cyber Security for Your{' '}
            <span className="text-gradient">Peace of Mind</span>
          </h1>

          {/* Sous-titre */}
          <p className="hero-subtitle">
            At PSCI we provide trusted, around-the-clock security solutions 
            tailored to protect your data with GDPR compliance, consent management, 
            and automated audits.
          </p>

          {/* CTA Buttons */}
          <div className="hero-cta">
            <Link to="/register">
              <Button variant="primary" size="xl">
                Start Protecting Your Presence
              </Button>
            </Link>
            <a href="#features">
              <Button variant="ghost" size="xl">
                Discover More
              </Button>
            </a>
          </div>

          {/* Trust badges */}
          <motion.div 
            className="hero-trust"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            <span className="trust-text">Trusted by 2700+ startups & brands</span>
            <div className="trust-logos">
              <span className="trust-logo">Veltrix</span>
              <span className="trust-logo">Trivexa</span>
              <span className="trust-logo">Brilora</span>
              <span className="trust-logo">Revomia</span>
            </div>
          </motion.div>
        </motion.div>

        {/* Globe 3D animé (version CSS) */}
        <motion.div
          className="hero-visual"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
        >
          <div className="globe-container">
            <div className="globe">
              <div className="globe-inner">
                {/* Points du globe (Amériques) */}
                <div className="globe-dots">
                  {[...Array(80)].map((_, i) => (
                    <motion.div
                      key={i}
                      className="globe-dot"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                      }}
                      animate={{
                        opacity: [0.2, 0.8, 0.2],
                        scale: [1, 1.5, 1]
                      }}
                      transition={{
                        duration: 3 + Math.random() * 2,
                        repeat: Infinity,
                        delay: Math.random() * 2
                      }}
                    />
                  ))}
                </div>
                {/* Anneaux du globe */}
                <div className="globe-ring globe-ring-1" />
                <div className="globe-ring globe-ring-2" />
              </div>
            </div>
            <div className="globe-glow" />
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;

