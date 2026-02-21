import React from 'react';
import { FaRobot, FaUserGraduate, FaLaptopCode, FaClipboardCheck, FaChartLine, FaUsers } from 'react-icons/fa';
import '../../styles/Features.css';

const Features = () => {
  const features = [
    {
      icon: <FaRobot className="feature-icon" />,
      title: 'AI-Powered Analysis',
      description: 'Advanced analysis of your skills and identification of gaps using AI.'
    },
    {
      icon: <FaUserGraduate className="feature-icon" />,
      title: 'Performance Tracking',
      description: 'Monitor your academic progress and skill development over time.'
    },
    {
      icon: <FaLaptopCode className="feature-icon" />,
      title: 'Industry Skills',
      description: 'Learn the most in-demand skills that employers are looking for.'
    },
    {
      icon: <FaClipboardCheck className="feature-icon" />,
      title: 'Placement Prep',
      description: 'Get prepared for job interviews with our comprehensive resources.'
    },
    {
      icon: <FaChartLine className="feature-icon" />,
      title: 'Progress Analytics',
      description: 'Track your learning journey with detailed analytics and insights.'
    },
    {
      icon: <FaUsers className="feature-icon" />,
      title: 'Community Support',
      description: 'Connect with peers and mentors in our learning community.'
    }
  ];

  return (
    <section className="features-section">
      <div className="container">
        <h2 className="section-title">Our Features</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon-wrapper">
                {feature.icon}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;