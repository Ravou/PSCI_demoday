import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

function LandingPage() {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>PSCI</h1>
          <h2 className="hero-subtitle-main">Audit RGPD Automatisé</h2>
          <p className="hero-subtitle">
            Analysez la conformité RGPD de votre site web en quelques clics. 
            Intelligence artificielle et expertise juridique combinées.
          </p>
          <div className="hero-buttons">
            <Link to="/register" className="btn btn-primary-large">
              Commencer maintenant
            </Link>
            <Link to="/login" className="btn btn-secondary-large">
              Se connecter
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <div className="hero-illustration">
            <span className="icon-large">🔐</span>
            <span className="floating-icon">📊</span>
            <span className="floating-icon delay-1">⚖️</span>
            <span className="floating-icon delay-2">🛡️</span>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="services-section">
        <h2 className="section-title">Nos Services</h2>
        <div className="services-grid">
          <div className="service-card">
            <div className="service-icon">📋</div>
            <h3>Audit Automatisé</h3>
            <p>
              Analyse complète de votre site web en temps réel. 
              Détection automatique des non-conformités RGPD.
            </p>
            <Link to="/register" className="service-link">
              En savoir plus →
            </Link>
          </div>

          <div className="service-card">
            <div className="service-icon">🤖</div>
            <h3>Intelligence Artificielle</h3>
            <p>
              Algorithmes avancés pour identifier les cookies, 
              trackers et collectes de données non conformes.
            </p>
            <Link to="/register" className="service-link">
              En savoir plus →
            </Link>
          </div>

          <div className="service-card">
            <div className="service-icon">📊</div>
            <h3>Rapports Détaillés</h3>
            <p>
              Recevez des rapports complets avec recommandations 
              et plan d'action pour la mise en conformité.
            </p>
            <Link to="/register" className="service-link">
              En savoir plus →
            </Link>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="about-section">
        <div className="about-content">
          <div className="about-text">
            <h2>À propos de PSCI</h2>
            <p>
              Pionnier dans l'audit RGPD automatisé, PSCI accompagne les entreprises 
              dans leur mise en conformité avec le Règlement Général sur la Protection des Données.
            </p>
            <p>
              Notre plateforme analyse quotidiennement des centaines de sites web 
              pour garantir leur conformité et protéger les données personnelles des utilisateurs.
            </p>
            <Link to="/register" className="btn btn-primary">
              Démarrer un audit gratuit
            </Link>
          </div>
          <div className="about-image">
            <div className="stats-box">
              <div className="stat">
                <span className="stat-number">1000+</span>
                <span className="stat-label">Audits réalisés</span>
              </div>
              <div className="stat">
                <span className="stat-number">95%</span>
                <span className="stat-label">Taux de satisfaction</span>
              </div>
              <div className="stat">
                <span className="stat-number">24/7</span>
                <span className="stat-label">Support disponible</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2>Prêt à auditer votre site ?</h2>
        <p>Commencez votre audit RGPD avec PSCI en moins de 2 minutes</p>
        <Link to="/register" className="btn btn-primary-large">
          Créer un compte gratuitement
        </Link>
      </section>
    </div>
  );
}

export default LandingPage;
