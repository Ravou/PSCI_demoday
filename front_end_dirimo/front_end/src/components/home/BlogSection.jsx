import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';
import './BlogSection.css';

const BlogCard = ({ article, delay = 0 }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  return (
    <motion.article
      ref={ref}
      className="blog-card"
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay }}
    >
      <div className="blog-image">
        <div className="blog-image-placeholder">
          {article.icon}
        </div>
        <div className="blog-image-overlay" />
      </div>
      
      <div className="blog-content">
        <time className="blog-date">{article.date}</time>
        <h3 className="blog-title">{article.title}</h3>
        <p className="blog-excerpt">{article.excerpt}</p>
        
        <a href={article.link} className="blog-link">
          Read More
          <span className="blog-arrow">→</span>
        </a>
      </div>
    </motion.article>
  );
};

const BlogSection = () => {
  const articles = [
    {
      icon: '📱',
      date: 'June 4, 2025',
      title: 'How Mobile Patrols Are Changing Modern Security',
      excerpt: 'Explore the evolution of security patrols and how mobile technology is revolutionizing real-time monitoring.',
      link: '#'
    },
    {
      icon: '🤖',
      date: 'June 11, 2025',
      title: 'Artificial Intelligence: Revolutionizing Customer Service',
      excerpt: 'Discover how AI is transforming customer interactions and enhancing service quality across industries.',
      link: '#'
    },
    {
      icon: '☁️',
      date: 'September 15, 2025',
      title: 'Understanding Edge Computing: Benefits and Use Cases',
      excerpt: 'Learn about edge computing technology and its practical applications in modern infrastructure.',
      link: '#'
    }
  ];

  return (
    <section className="blog-section">
      <div className="blog-container">
        {/* Header */}
        <motion.div
          className="blog-header"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="section-title">
            Latest from <span className="text-gradient">Our Blog</span>
          </h2>
          <p className="section-subtitle">
            At PSCI Security, we believe that security starts with awareness. 
            Our blog features expert tips, industry insights, and best practices.
          </p>
        </motion.div>

        {/* Articles Grid */}
        <div className="blog-grid">
          {articles.map((article, index) => (
            <BlogCard 
              key={index} 
              article={article} 
              delay={index * 0.15}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default BlogSection;

