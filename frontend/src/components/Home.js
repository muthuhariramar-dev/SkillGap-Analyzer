import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  return (
    <section className="hero">
      <div className="container">
        <h1>AI-Driven Student <span className="highlight">Skill Gap Analyzer & Placement risk Awareness</span></h1>
        <p>Empowering students to understand their industry readiness, identify missing skills, and reduce placement risk using intelligent analysis.</p>
        
        <div className="cta-buttons">
          <Link to="/students" className="btn btn-primary">Get Started</Link>
          <Link to="/students#assessment" className="btn btn-secondary">Take Skill Assessment</Link>
        </div>
        
        <div className="key-highlights">
          <h3>Key Highlights:</h3>
          <div className="highlights-grid">
            <div className="highlight-card">
              <div className="icon">🤖</div>
              <h4>AI-Powered Analysis</h4>
              <p>Advanced algorithms to assess your skills accurately</p>
            </div>
            <div className="highlight-card">
              <div className="icon">📊</div>
              <h4>Risk Prediction</h4>
              <p>Understand your placement readiness level</p>
            </div>
            <div className="highlight-card">
              <div className="icon">🎯</div>
              <h4>Personalized Guidance</h4>
              <p>Customized learning paths for your growth</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Home;
