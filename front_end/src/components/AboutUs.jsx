import React from 'react';
import './AboutUs.css';

function AboutUs() {
  return (
    <div className="about-page">
      <div className="about-container">
        <h1 className="about-title">Welcome to PSCI</h1>
        <p className="about-subtitle">
          PSCI is a platform designed to reduce the rate of GDPR non-compliance of websites
          and to guide website owners toward full compliance.
        </p>

        <div className="about-text">
          Today, the GDPR non-compliance rate remains high: over 70% of websites do not fully
          meet GDPR requirements, which can expose companies to penalties and undermine user trust.
          PSCI helps improve your website through an AI-generated automated audit that is
          both qualitative and pedagogical, making results easy to understand and apply.
        </div>

        <div className="about-how">
          <div className="about-how-title">How it works</div>
          <div className="about-step">
            1. Upon registration, you give consent to analyze your website.
          </div>
          <div className="about-step">
            2. We perform targeted scraping only on GDPR-related content (e.g., legal notices, privacy policy, cookie consent).
          </div>
          <div className="about-step">
            3. No personal data is collected; scraped data is used temporarily to generate the audit.
          </div>
          <div className="about-step">
            4. Once the audit is generated, only the audit results are saved in your account. You can delete them at any time.
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutUs;