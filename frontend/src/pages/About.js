import React from 'react';
import '../styles/About.css';

const About = ({ id }) => {
  // Using placeholder images from Unsplash
  const teamImage = 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80';
  const discussionImage = 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80';

  return (
    <section id={id} className="about-section">
      <div className="container">
        <h2 className="section-title">About Us</h2>
        <div className="about-content">
          <div className="about-card">
            <div className="about-image">
              <img src={teamImage} alt="Our Team" />
            </div>
            <div className="about-text">
              <h3>Who We Are</h3>
              <p>We are an academic-driven innovation team focused on improving student employability through artificial intelligence. Our team consists of passionate educators, data scientists, and industry experts dedicated to bridging the gap between education and employment.</p>
            </div>
          </div>

          <div className="about-card reverse">
            <div className="about-image">
              <img src={discussionImage} alt="Our Mission" />
            </div>
            <div className="about-text">
              <h3>Our Mission</h3>
              <p>To help students understand their strengths, weaknesses, and placement readiness at an early stage. We believe in empowering the next generation of professionals with the tools and insights they need to succeed in today's competitive job market.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;