import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';
import './StatsSection.css';

const StatCard = ({ number, suffix = '', label, delay = 0 }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      className="stat-card"
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay }}
    >
      <div className="stat-number">
        <span className="stat-value">{number}</span>
        <span className="stat-suffix">{suffix}</span>
      </div>
      <div className="stat-label">{label}</div>
      <div className="stat-glow" aria-hidden="true" />
    </motion.div>
  );
};

const StatsSection = () => {
  const stats = [
    { number: '150', suffix: '+', label: 'Certified Security Officers' },
    { number: '12', suffix: '+', label: 'Years of Experience' },
    { number: '4.9', suffix: '/5', label: 'Client Satisfaction Rating' },
    { number: '99.9', suffix: '%', label: 'Incident-Free Rate' }
  ];

  return (
    <section className="stats-section">
      <div className="stats-container">
        <div className="stats-grid">
          {stats.map((stat, index) => (
            <StatCard 
              key={index}
              number={stat.number}
              suffix={stat.suffix}
              label={stat.label}
              delay={index * 0.1}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;

