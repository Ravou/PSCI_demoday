import React from 'react';
import { motion } from 'framer-motion';
import './Button.css';

/**
 * Composant Button réutilisable avec plusieurs variantes
 * Variantes: primary, secondary, ghost, outline
 * Tailles: sm, md, lg, xl
 */
const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md',
  icon = null,
  iconPosition = 'left',
  fullWidth = false,
  disabled = false,
  onClick,
  href,
  type = 'button',
  className = '',
  ...props 
}) => {
  
  const buttonClasses = `
    btn 
    btn-${variant} 
    btn-${size} 
    ${fullWidth ? 'btn-full' : ''} 
    ${disabled ? 'btn-disabled' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  const buttonContent = (
    <>
      {icon && iconPosition === 'left' && <span className="btn-icon btn-icon-left">{icon}</span>}
      <span className="btn-text">{children}</span>
      {icon && iconPosition === 'right' && <span className="btn-icon btn-icon-right">{icon}</span>}
    </>
  );

  const motionProps = {
    whileHover: disabled ? {} : { scale: 1.02, y: -2 },
    whileTap: disabled ? {} : { scale: 0.98 },
    transition: { duration: 0.2, ease: 'easeInOut' }
  };

  // Si href fourni, rendu en tant que lien
  if (href) {
    return (
      <motion.a
        href={href}
        className={buttonClasses}
        {...motionProps}
        {...props}
      >
        {buttonContent}
      </motion.a>
    );
  }

  // Sinon, rendu en tant que bouton
  return (
    <motion.button
      type={type}
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled}
      {...motionProps}
      {...props}
    >
      {buttonContent}
    </motion.button>
  );
};

export default Button;

