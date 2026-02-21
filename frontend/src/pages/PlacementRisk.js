import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaExclamationTriangle, FaArrowLeft, FaShieldAlt, FaTimes } from 'react-icons/fa';
import '../styles/PlacementRisk.css';

const PlacementRisk = () => {
  const navigate = useNavigate();

  return (
    <div className="placement-risk-container">
      <div className="placement-risk-header">
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1><FaExclamationTriangle /> Placement Risk Awareness</h1>
        <p>Understand your placement readiness with comprehensive risk assessment</p>
      </div>

      <div className="risk-analysis-intro">
        <div className="intro-card">
          <h2>Placement Risk Assessment</h2>
          <p>
            Our comprehensive placement risk assessment evaluates your readiness for the job market
            across multiple dimensions including technical skills, non-technical abilities,
            interview preparation, and portfolio strength.
          </p>

          <div className="risk-levels-info">
            <h3>Risk Levels Explained</h3>
            <div className="risk-levels-grid">
              <div className="risk-level-card low">
                <div className="risk-icon"><FaShieldAlt /></div>
                <h4>Low Risk</h4>
                <p>Candidate demonstrates strong technical and interview readiness and can confidently apply for jobs.</p>
              </div>

              <div className="risk-level-card medium">
                <div className="risk-icon"><FaExclamationTriangle /></div>
                <h4>Medium Risk</h4>
                <p>Candidate has foundational skills but requires improvement in selected areas before applying.</p>
              </div>

              <div className="risk-level-card high">
                <div className="risk-icon"><FaTimes /></div>
                <h4>High Risk</h4>
                <p>Candidate needs structured preparation across technical and non-technical skills.</p>
              </div>
            </div>
          </div>

          <div className="start-assessment-section" style={{ marginTop: '40px', textAlign: 'center' }}>
            <button
              className="analyze-risk-btn"
              onClick={() => navigate('/preparation')}
              style={{ width: '100%', maxWidth: '400px' }}
            >
              Start Risk Assessment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlacementRisk;
