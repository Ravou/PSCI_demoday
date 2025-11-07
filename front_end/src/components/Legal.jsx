import React from 'react';
import './Legal.css'; // Crée un fichier CSS spécifique si tu veux

function Legal() {
  return (
    <div className="legal-page">
      <div className="legal-container">
        <h1 className="legal-title">Legal Information</h1>

        {/* Cookies */}
        <section className="legal-section">
          <h2 className="legal-section-title">Cookies</h2>
          <p className="legal-text">
            PSCI uses cookies to enhance your experience on our website. Cookies help us understand how you interact with our site, remember your preferences, and improve the quality of our services.
            You can manage or disable cookies in your browser settings, but some features may not function properly without them.
          </p>
        </section>

        {/* Privacy / RGPD */}
        <section className="legal-section">
          <h2 className="legal-section-title">Privacy & Data Protection (RGPD)</h2>
          <p className="legal-text">
            Your privacy is important to us. PSCI complies with GDPR regulations to ensure your personal data is processed securely and transparently.  
            When you use our services, we only collect data necessary to provide audits and improve your experience, and only with your consent.  
            All data scrapped from your website for audits is temporary and deleted after the audit is completed. You can also delete your audit results at any time.
          </p>
        </section>

        {/* Data Processing */}
        <section className="legal-section">
          <h2 className="legal-section-title">Data Processing</h2>
          <p className="legal-text">
            PSCI processes data strictly for audit purposes. We do not sell, rent, or share your data with third parties.  
            Only anonymized statistical data may be used internally to improve our services. You retain full control of your account data and can request its deletion at any time.
          </p>
        </section>

        {/* Terms of Use / CGU */}
        <section className="legal-section">
          <h2 className="legal-section-title">Terms of Use (CGU)</h2>
          <p className="legal-text">
            By using PSCI, you agree to respect our terms of use. You must not use our services for illegal activities, and you agree that PSCI is not responsible for the compliance of third-party websites.  
            PSCI reserves the right to suspend accounts that violate these terms.
          </p>
        </section>
      </div>
    </div>
  );
}

export default Legal;