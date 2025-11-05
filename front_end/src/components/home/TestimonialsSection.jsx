import React from 'react';
import { motion } from 'framer-motion';
import './TestimonialsSection.css';

const TestimonialsSection = () => {
  const testimonials = [
    {
      name: 'Mark Johnson',
      role: 'Chief Technology Officer',
      company: 'TechCorp',
      rating: 4.9,
      text: 'Working with Secuby® Security has transformed our approach to safety. Their proactive strategies and commitment have ensured our operations run smoothly and securely. We couldn\'t ask for a better partner.',
      avatar: 'MJ'
    },
    {
      name: 'David Chowdhury',
      role: 'Software Engineer',
      company: 'DevSolutions',
      rating: 4,
      text: 'Excellent service! Their team was professional and ensured our property was secured 24/7. We feel much safer now. Highly recommend for anyone looking for reliable security.',
      avatar: 'DC'
    },
    {
      name: 'Rayhan Karim',
      role: 'Real Estate Developer',
      company: 'PropInvest',
      rating: 4.9,
      text: 'Quick response time and highly trained personnel. They handled every situation with care and efficiency. I\'m very satisfied with the level of protection provided. Highly recommended for anyone looking for top-tier security.',
      avatar: 'RK'
    }
  ];

  return (
    <section className="testimonials-section">
      <div className="testimonials-container">
        <motion.div
          className="testimonials-header"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="section-title">What Our <span className="text-gradient">Clients Say</span></h2>
          <p className="section-subtitle">
            At PSCI® , we believe great service speaks for itself, but our clients say it even better. 
            Here's what they have to say:
          </p>
          <div className="overall-rating">
            <span className="rating-value">4.9/5</span>
            <div className="stars">
              {[...Array(5)].map((_, i) => (
                <span key={i} className="star">★</span>
              ))}
            </div>
          </div>
        </motion.div>

        <div className="testimonials-grid">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              className="testimonial-card"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
            >
              <div className="testimonial-header">
                <div className="avatar">{testimonial.avatar}</div>
                <div className="client-info">
                  <h4 className="client-name">{testimonial.name}</h4>
                  <p className="client-role">{testimonial.role}</p>
                </div>
              </div>

              <p className="testimonial-text">"{testimonial.text}"</p>

              <div className="testimonial-footer">
                <div className="rating">
                  <span className="rating-number">{testimonial.rating}/5</span>
                  <div className="stars">
                    {[...Array(5)].map((_, i) => (
                      <span key={i} className={`star ${i < Math.floor(testimonial.rating) ? 'filled' : ''}`}>★</span>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="pagination-dots">
          {testimonials.map((_, i) => (
            <span key={i} className={`dot ${i === 0 ? 'active' : ''}`} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;

