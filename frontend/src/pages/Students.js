import React from 'react';
import { FaGraduationCap, FaChartLine, FaLaptopCode, FaUserGraduate } from 'react-icons/fa';
import '../styles/Students.css';

const Students = ({ id }) => {
  return (
    <section id={id} className="students-section">
      <div className="container">
        <h2>For Students</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <FaGraduationCap />
            </div>
            <h3>Skill Assessment</h3>
            <p>Take our AI-powered skill assessment to evaluate your current abilities and get personalized feedback on your strengths and areas for improvement.</p>
            <button className="btn btn-outline">Start Assessment</button>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <FaChartLine />
            </div>
            <h3>Gap Analysis</h3>
            <p>Identify the gap between your skills and industry requirements with our comprehensive gap analysis tool.</p>
            <button className="btn btn-outline">Analyze Skills</button>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <FaLaptopCode />
            </div>
            <h3>Learning Path</h3>
            <p>Get personalized learning recommendations to bridge your skill gaps and enhance your employability.</p>
            <button className="btn btn-outline">View Learning Path</button>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <FaUserGraduate />
            </div>
            <h3>Career Guidance</h3>
            <p>Receive expert career advice based on your skills, interests, and market demand.</p>
            <button className="btn btn-outline">Get Guidance</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Students;