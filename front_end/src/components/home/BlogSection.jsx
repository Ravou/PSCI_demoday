import React from 'react';
import { motion } from 'framer-motion';
import phoneImage from '../../assets/images/phone.jpg';
import iaImage from '../../assets/images/IAphoto.jpg';
import edgeImage from '../../assets/images/edgecomputing.jpg';
import './BlogSection.css';

const BlogSection = () => {
  const blogPosts = [
    {
      date: 'June 4, 2025',
      title: 'How Mobile Patrols Are Changing Modern Security',
      category: 'Security Trends',
      image: phoneImage,
      link: 'https://www.sentinelone.com/cybersecurity-101/endpoint-security/mobile-device-security/'
    },
    {
      date: 'June 11, 2025',
      title: 'Artificial Intelligence: Revolutionizing Customer Service',
      category: 'Technology',
      image: iaImage,
      link: 'https://www.ibm.com/fr-fr/think/insights/customer-service-future'
    },
    {
      date: 'September 16, 2025',
      title: 'Understanding Edge Computing: Benefits and Use Cases',
      category: 'Cloud & Edge',
      image: edgeImage,
      link: 'https://medium.com/@network3/the-evolution-of-edge-ai-3faa0348c4be'
    }
  ];

  return (
    <section className="blog-section">
      <div className="blog-container">
        <motion.div
          className="blog-header"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="section-title">
            Latest from our <span className="text-gradient">blog</span>
          </h2>
          <p className="section-subtitle">
            At PSCI company, we believe that GRPD compliance is not just a legal requirement. 
            Our blog features expert tips, industry insights, and the latest trends.
          </p>
        </motion.div>

        <div className="blog-grid">
          {blogPosts.map((post, index) => (
            <motion.a
              href={post.link}
              target="_blank"
              rel="noopener noreferrer"
              key={index}
              className="blog-card"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
            >
              <div className="blog-image" style={{ backgroundImage: `url(${post.image})` }}>
                <div className="blog-overlay" />
              </div>

              <div className="blog-content">
                <span className="blog-date">{post.date}</span>
                <h3 className="blog-title">{post.title}</h3>
                <div className="blog-footer">
                  <span className="read-more">
                    Read More <span className="arrow">→</span>
                  </span>
                </div>
              </div>
            </motion.a>
          ))}
        </div>

        <motion.div
          className="blog-cta"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <div className="cta-content">
            <p className="cta-subtitle">24/7 Protection With Live Recording</p>
            <h3 className="cta-title">Your safety is our mission. Your trust is our commitment.</h3>
            <p className="cta-text">
              Click below to schedule your free risk assessment and learn how we can help protect your world.
            </p>
            <button className="btn btn-primary btn-xl">Start Protecting Your Presence</button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default BlogSection;
