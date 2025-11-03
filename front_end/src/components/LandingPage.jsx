import React from 'react';
import HeroSection from './home/HeroSection';
import FeaturesSection from './home/FeaturesSection';
import StatsSection from './home/StatsSection';
import TestimonialsSection from './home/TestimonialsSection';
import BlogSection from './home/BlogSection';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <HeroSection />
      <FeaturesSection />
      <StatsSection />
      <TestimonialsSection />
      <BlogSection />
    </div>
  );
};

export default LandingPage;
