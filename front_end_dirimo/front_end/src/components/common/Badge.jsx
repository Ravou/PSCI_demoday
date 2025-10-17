import React from 'react';
import { motion } from 'framer-motion';
import './Badge.css';

/**
 * Composant Badge réutilisable
 * Variantes: primary, secondary, outline, dot
 */
const Badge = ({ 
  children, 
  variant = 'primary',
  icon = null,
  dot = false,
  pulse = false,
  className = '',
  ...props 
}) => {
  
  const badgeClasses = `
    badge 
    badge-${variant} 
    ${pulse ? 'badge-pulse' : ''}
    ${dot ? 'badge-dot' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  return (
    <motion.div
      className={badgeClasses}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      {...props}
    >
      {dot && <span className="badge-dot-indicator" />}
      {icon && <span className="badge-icon">{icon}</span>}
      <span className="badge-text">{children}</span>
    </motion.div>
  );
};

export default Badge;

