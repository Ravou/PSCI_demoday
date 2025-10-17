import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Card from '../common/Card';
import './TestimonialsSection.css';

const TestimonialCard = ({ testimonial }) => {
  return (
    <Card variant="default" hoverable={false}>
      <div className="testimonial-content">
        <div className="testimonial-header">
          <div className="testimonial-avatar">
            {testimonial.name.charAt(0)}
          </div>
          <div className="testimonial-info">
            <h4 className="testimonial-name">{testimonial.name}</h4>
            <p className="testimonial-role">{testimonial.role}</p>
          </div>
        </div>
        
        <p className="testimonial-text">"{testimonial.text}"</p>
        
        <div className="testimonial-footer">
          <div className="testimonial-rating">
            {[...Array(5)].map((_, i) => (
              <span 
                key={i} 
                className={`star ${i < Math.floor(testimonial.rating) ? 'star-filled' : ''}`}
              >
                ★
              </span>
            ))}
            <span className="rating-value">{testimonial.rating}/5</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

const TestimonialsSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const testimonials = [
    {
      name: 'Mark Johnson',
      role: 'Chief Technology Officer',
      text: 'Working with PSCI Security has transformed our approach to safety. Their proactive strategies and commitment have ensured our operations run smoothly and securely. We couldn\'t ask for more.',
      rating: 4.9,
      avatar: 'MJ'
    },
    {
      name: 'David Chowdhury',
      role: 'Software Engineer',
      text: 'Excellent service! Their team was professional and ensured our property was secured 24/7. We feel much safer now. Highly recommend for anyone looking for reliable security.',
      rating: 4.0,
      avatar: 'DC'
    },
    {
      name: 'Rayhan Karim',
      role: 'Real Estate Developer',
      text: 'Quick response time and highly trained personnel. They handled every situation with care and efficiency. I\'m very satisfied with the level of protection provided. Highly recommend for anyone looking.',
      rating: 4.9,
      avatar: 'RK'
    }
  ];

  const visibleTestimonials = testimonials.slice(currentIndex, currentIndex + 3);

  const handleNext = () => {
    if (currentIndex < testimonials.length - 3) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <section className="testimonials-section">
      <div className="testimonials-container">
        {/* Header */}
        <motion.div
          className="testimonials-header"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="testimonials-badge">Our clients & partners</div>
          <h2 className="section-title">
            What <span className="text-gradient">Our Clients Say</span>
          </h2>
          <p className="section-subtitle">
            At PSCI Security, we believe great service speaks for itself — but 
            our clients say it even better. Here's what they have to say.
          </p>
          <div className="testimonials-rating">
            <span className="rating-number">4.9/5</span>
            <div className="rating-stars">
              {[...Array(5)].map((_, i) => (
                <span key={i} className="star star-filled">★</span>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Carousel */}
        <div className="testimonials-carousel">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              className="testimonials-grid"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.4 }}
            >
              {visibleTestimonials.map((testimonial, index) => (
                <TestimonialCard 
                  key={currentIndex + index} 
                  testimonial={testimonial} 
                />
              ))}
            </motion.div>
          </AnimatePresence>

          {/* Navigation dots */}
          <div className="carousel-dots">
            {testimonials.map((_, index) => (
              <button
                key={index}
                className={`carousel-dot ${index === currentIndex ? 'carousel-dot-active' : ''}`}
                onClick={() => setCurrentIndex(index)}
                aria-label={`Go to testimonial ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;

