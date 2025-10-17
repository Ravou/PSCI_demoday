import React from 'react';
import { motion } from 'framer-motion';
import './Card.css';

/**
 * Composant Card réutilisable avec animations
 * Variantes: default, highlight, glass
 */
const Card = ({ 
  children, 
  variant = 'default',
  hoverable = true,
  glowEffect = false,
  className = '',
  onClick,
  ...props 
}) => {
  
  const cardClasses = `
    card 
    card-${variant} 
    ${hoverable ? 'card-hoverable' : ''} 
    ${glowEffect ? 'card-glow' : ''}
    ${onClick ? 'card-clickable' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  const motionProps = hoverable ? {
    whileHover: { y: -8, scale: 1.02 },
    transition: { duration: 0.3, ease: 'easeOut' }
  } : {};

  return (
    <motion.div
      className={cardClasses}
      onClick={onClick}
      {...motionProps}
      {...props}
    >
      {glowEffect && <div className="card-glow-effect" aria-hidden="true" />}
      <div className="card-content">
        {children}
      </div>
    </motion.div>
  );
};

export default Card;

