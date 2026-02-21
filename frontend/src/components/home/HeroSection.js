import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/Hero.css';

const HeroSection = () => {
  const heroStyle = {
    backgroundImage: `linear-gradient(rgba(30, 58, 138, 0.9), rgba(30, 64, 175, 0.9)), 
                     url('/discussion.jpg')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundAttachment: 'fixed',
  };

  return (
    <section className="hero" style={heroStyle}>
      <div className="hero-content">
        <div className="hero-text">
          <h1>AI-Driven Student Skill Gap Analyzer</h1>
          <p>Empowering students to understand their industry readiness and identify missing skills with intelligent analysis.</p>
          <div className="hero-cta">
            <Link to="/register" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/about" className="btn btn-outline">
              Learn More
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;