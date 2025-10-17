import React from 'react';
import HeroSection from './home/HeroSection';
import StatsSection from './home/StatsSection';
import FeaturesSection from './home/FeaturesSection';
import TestimonialsSection from './home/TestimonialsSection';
import BlogSection from './home/BlogSection';
import CTASection from './home/CTASection';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <HeroSection />
      <StatsSection />
      <FeaturesSection />
      <TestimonialsSection />
      <BlogSection />
      <CTASection />
    </div>
  );
};

export default LandingPage;
