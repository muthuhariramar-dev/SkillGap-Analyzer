// src/pages/Placements.js
import React from 'react';
import { Link } from 'react-router-dom';
import { FaArrowLeft, FaChartLine, FaUsers, FaGraduationCap, FaTrophy, FaBrain, FaHistory, FaBook, FaBuilding } from 'react-icons/fa';
import '../styles/PlacementsPage.css';

const Placements = () => {
  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/dashboard" className="back-button">
          <FaArrowLeft /> Back to Dashboard
        </Link>
        <h1>Placements</h1>
      </div>
      
      {/* Hero Section */}
      <div className="placement-hero" style={{
        backgroundImage: `url('/australia.png')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.85)',
          zIndex: 1
        }}></div>
        <div className="hero-content" style={{ position: 'relative', zIndex: 2 }}>
          <h2>Placement Readiness System</h2>
          <p className="hero-subtitle">We help students and placement cells understand real readiness beyond marks.</p>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h3>Features</h3>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <FaChartLine />
            </div>
            <h4>Skill proficiency score</h4>
            <p>Comprehensive assessment of technical and soft skills with detailed analytics</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <FaUsers />
            </div>
            <h4>Role-based comparison</h4>
            <p>Compare student profiles against industry requirements for specific roles</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <FaHistory />
            </div>
            <h4>Historical placement pattern analysis</h4>
            <p>Analyze trends and patterns from previous placement data for better insights</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <FaChartLine />
            </div>
            <h4>Readiness dashboard</h4>
            <p>Real-time monitoring of student readiness with interactive visualizations</p>
          </div>
          <Link to="/preparation" className="feature-card">
            <div className="feature-icon">
              <FaBook />
            </div>
            <h4>Preparation</h4>
            <p>Comprehensive study materials, practice tests, and personalized learning paths for placement success</p>
          </Link>
          <a href="/companyanalysis.html" className="feature-card">
            <div className="feature-icon">
              <FaBuilding />
            </div>
            <h4>Company insights</h4>
            <p>Detailed company profiles, interview patterns, and culture fit analysis for better placement decisions</p>
          </a>
        </div>
        
        {/* Feature Content Boxes */}
        <div className="feature-content-boxes">
          <div className="content-box">
            <h4>Preparation Resources</h4>
            <ul>
              <li>Technical Interview Questions</li>
              <li>Aptitude Test Practice</li>
              <li>Mock Interviews</li>
              <li>Resume Building Tips</li>
            </ul>
            <Link to="/preparation" className="box-link">Explore More →</Link>
          </div>
          <div className="content-box">
            <h4>Company Insights</h4>
            <ul>
              <li>Top Hiring Companies</li>
              <li>Interview Process Insights</li>
              <li>Salary Benchmarks</li>
              <li>Culture Fit Assessment</li>
            </ul>
            <a href="/companyanalysis.html" className="box-link">View Details →</a>
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="benefits-section">
        <h3>Benefits for Placement Cells</h3>
        <p className="benefits-subtitle">
          Empower your placement cell with data-driven insights and systematic approach to student success
        </p>
        <div className="benefits-grid">
          <div className="benefit-card">
            <div className="benefit-icon">
              <FaBrain />
            </div>
            <h4>Early identification of high-risk students</h4>
            <p>Proactively identify students who need additional support before placement season through AI-powered risk assessment</p>
            <div className="benefit-highlight">Reduce placement failures by 40%</div>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">
              <FaGraduationCap />
            </div>
            <h4>Better training planning</h4>
            <p>Data-driven insights to design targeted training programs that address specific skill gaps and industry requirements</p>
            <div className="benefit-highlight">Improve training efficiency by 60%</div>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">
              <FaTrophy />
            </div>
            <h4>Improved placement success rate</h4>
            <p>Increase overall placement success through systematic readiness improvement and personalized guidance</p>
            <div className="benefit-highlight">Boost placement rate by 35%</div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="placement-stats">
        <div className="stat-card">
          <h3>Students Assessed</h3>
          <div className="stat-value">1,248</div>
          <div className="stat-change positive">+18% ↑</div>
        </div>
        <div className="stat-card">
          <h3>Placement Success Rate</h3>
          <div className="stat-value">87%</div>
          <div className="stat-change positive">+12% ↑</div>
        </div>
        <div className="stat-card">
          <h3>Companies Partnered</h3>
          <div className="stat-value">156</div>
          <div className="stat-change positive">+24% ↑</div>
        </div>
        <div className="stat-card">
          <h3>Avg. Package Increase</h3>
          <div className="stat-value">32%</div>
          <div className="stat-change positive">+8% ↑</div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="cta-section">
        <h3>Ready to Transform Your Placement Process?</h3>
        <p>Join leading institutions using our AI-powered readiness system</p>
        <div className="cta-buttons">
          <Link to="/placement-risk" className="primary-button">
            <FaChartLine /> View Dashboard
          </Link>
          <button className="secondary-button">
            <FaUsers /> Schedule Demo
          </button>
        </div>
      </div>
    </div>
  );
};

export default Placements;