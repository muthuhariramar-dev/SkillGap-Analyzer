// src/pages/Assessments.js
import React from 'react';
import { Link } from 'react-router-dom';
import { FaArrowLeft, FaClipboardList, FaSearch, FaFilter } from 'react-icons/fa';
import '../styles/Assessments.css';

const Assessments = () => {
  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/dashboard" className="back-button">
          <FaArrowLeft /> Back to Dashboard
        </Link>
        <h1>Assessments</h1>
        <button className="primary-button">
          <FaClipboardList /> Create Assessment
        </button>
      </div>
      
      <div className="assessments-stats">
        <div className="stat-card">
          <h3>Total Assessments</h3>
          <div className="stat-value">156</div>
          <div className="stat-change positive">+8% ↑</div>
        </div>
        <div className="stat-card">
          <h3>Average Score</h3>
          <div className="stat-value">78%</div>
          <div className="stat-change positive">+3% ↑</div>
        </div>
      </div>

      <div className="search-filter-bar">
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input type="text" placeholder="Search assessments..." />
        </div>
        <button className="filter-button">
          <FaFilter /> Filters
        </button>
      </div>

      <div className="assessments-grid">
        {/* Assessment cards will be mapped here */}
        <div className="no-assessments">
          <h3>No assessments found</h3>
          <p>Create your first assessment to get started</p>
        </div>
      </div>
    </div>
  );
};

export default Assessments;