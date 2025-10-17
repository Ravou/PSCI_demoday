import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '../common/Button';
import './Navbar.css';

const Navbar = ({ user, onLogout }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const location = useLocation();

  // Détection du scroll pour effet sticky
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Fermer le menu mobile lors du changement de route
  useEffect(() => {
    setIsMobileMenuOpen(false);
    setIsDropdownOpen(false);
  }, [location]);

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Dashboard', path: '/dashboard', protected: true },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' }
  ];

  const dropdownLinks = [
    { name: 'Services', path: '/services' },
    { name: 'Pricing', path: '/pricing' },
    { name: 'Documentation', path: 'http://localhost:5000/docs', external: true }
  ];

  return (
    <motion.nav 
      className={`navbar ${isScrolled ? 'navbar-scrolled' : ''}`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <motion.div 
            className="logo-wrapper"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            <span className="logo-icon">⚡</span>
            <span className="logo-text">PSCI</span>
          </motion.div>
          <div className="logo-glow" aria-hidden="true" />
        </Link>

        {/* Desktop Navigation */}
        <div className="navbar-links">
          {navLinks.map((link) => {
            // Masquer Dashboard si non connecté
            if (link.protected && !user) return null;
            
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`nav-link ${isActive ? 'nav-link-active' : ''}`}
              >
                {link.name}
                {isActive && <motion.div className="nav-link-indicator" layoutId="indicator" />}
              </Link>
            );
          })}

          {/* Dropdown "All Pages" */}
          <div 
            className="nav-dropdown"
            onMouseEnter={() => setIsDropdownOpen(true)}
            onMouseLeave={() => setIsDropdownOpen(false)}
          >
            <button className="nav-link nav-dropdown-trigger">
              All Pages
              <motion.span 
                className="dropdown-arrow"
                animate={{ rotate: isDropdownOpen ? 180 : 0 }}
              >
                ▼
              </motion.span>
            </button>
            
            <AnimatePresence>
              {isDropdownOpen && (
                <motion.div
                  className="dropdown-menu"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  {dropdownLinks.map((link) => (
                    link.external ? (
                      <a
                        key={link.path}
                        href={link.path}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="dropdown-item"
                      >
                        {link.name}
                        <span className="external-icon">↗</span>
                      </a>
                    ) : (
                      <Link
                        key={link.path}
                        to={link.path}
                        className="dropdown-item"
                      >
                        {link.name}
                      </Link>
                    )
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Actions (User / Auth buttons) */}
        <div className="navbar-actions">
          {user ? (
            <>
              <div className="user-info">
                <span className="user-avatar">{user.name?.[0] || user.email?.[0]}</span>
                <span className="user-name">{user.name || user.email}</span>
              </div>
              <Button variant="ghost" size="sm" onClick={onLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost" size="sm">Sign In</Button>
              </Link>
              <Link to="/register">
                <Button variant="primary" size="sm">Get Started</Button>
              </Link>
            </>
          )}
        </div>

        {/* Mobile Menu Toggle */}
        <button 
          className="mobile-menu-toggle"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle menu"
        >
          <span className={`hamburger ${isMobileMenuOpen ? 'hamburger-open' : ''}`} />
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            className="mobile-menu"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {navLinks.map((link) => {
              if (link.protected && !user) return null;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className="mobile-menu-link"
                >
                  {link.name}
                </Link>
              );
            })}
            {dropdownLinks.map((link) => (
              link.external ? (
                <a
                  key={link.path}
                  href={link.path}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mobile-menu-link"
                >
                  {link.name}
                </a>
              ) : (
                <Link
                  key={link.path}
                  to={link.path}
                  className="mobile-menu-link"
                >
                  {link.name}
                </Link>
              )
            ))}
            
            <div className="mobile-menu-actions">
              {user ? (
                <Button variant="ghost" size="md" fullWidth onClick={onLogout}>
                  Logout
                </Button>
              ) : (
                <>
                  <Link to="/login">
                    <Button variant="ghost" size="md" fullWidth>Sign In</Button>
                  </Link>
                  <Link to="/register">
                    <Button variant="primary" size="md" fullWidth>Get Started</Button>
                  </Link>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;

