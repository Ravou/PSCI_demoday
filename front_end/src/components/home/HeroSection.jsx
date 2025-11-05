import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import './HeroSection.css';

const HeroSection = () => {
  return (
    <section className="hero-section">
      <div className="hero-grid" aria-hidden="true" />
      
      <motion.div 
        className="hero-glow hero-glow-1"
        animate={{ 
          scale: [1, 1.15, 1],
          opacity: [0.4, 0.6, 0.4]
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
          scale: [1, 1.12, 1],
          opacity: [0.3, 0.5, 0.3]
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
          <div className="hero-badge">
            Trusted Protection for Every Doorstep
          </div>

          <h1 className="hero-title">
            Reliable Compliance Security for Your{' '}
            <span className="text-gradient">Peace of Mind</span>
          </h1>

          <p className="hero-subtitle">
            At PSCI we provide trusted, around-the-clock security solutions 
            tailored to protect your data with GDPR compliance, consent management, 
            and automated audits.
          </p>

          <div className="hero-cta">
            <Link to="/register" className="btn btn-primary btn-xl">
              Start Protecting Your Presence
            </Link>
            <a href="#features" className="btn btn-ghost btn-xl">
              Discover More
            </a>
          </div>

          <div className="hero-trust">
            <span className="trust-text">Trusted by 2700+ startups & brands</span>
            <div className="trust-logos">
              <span className="trust-logo">Veltrix</span>
              <span className="trust-logo">Trivexa</span>
              <span className="trust-logo">Brilora</span>
              <span className="trust-logo">Revomia</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          className="hero-visual"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
        >
          <div className="globe-container">
            <div className="globe">
              <div className="globe-inner">
                <div className="globe-dots">
                  {[...Array(120)].map((_, i) => (
                    <motion.div
                      key={i}
                      className="globe-dot"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                      }}
                      animate={{
                        opacity: [0.3, 1, 0.3],
                        scale: [1, 1.8, 1]
                      }}
                      transition={{
                        duration: 2.5 + Math.random() * 2,
                        repeat: Infinity,
                        delay: Math.random() * 2
                      }}
                    />
                  ))}
                </div>
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

