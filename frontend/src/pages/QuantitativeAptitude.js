// src/pages/QuantitativeAptitude.js
import React from 'react';
import { Link } from 'react-router-dom';
import { FaArrowLeft, FaBrain, FaCalculator, FaChartLine, FaLightbulb, FaDownload, FaPlay } from 'react-icons/fa';
import '../styles/QuantitativeAptitude.css';

const QuantitativeAptitude = () => {
  return (
    <div className="quantitative-container">
      <div className="page-header">
        <Link to="/placements" className="back-button">
          <FaArrowLeft /> Back to Placements
        </Link>
        <h1>Quantitative Aptitude Excellence</h1>
        <p>Develop strong mathematical skills for placement tests and competitive exams</p>
        <div className="ai-badge">
          <FaBrain /> AI-Generated
        </div>
        <div className="updated-time">Updated just now</div>
      </div>

      {/* Number Systems Section */}
      <section className="topic-section">
        <div className="section-header">
          <h2><FaCalculator /> Number Systems</h2>
          <p>Master concepts of integers, fractions, decimals, and number properties</p>
        </div>

        <div className="topics-grid">
          <div className="topic-card">
            <h3>Prime Numbers</h3>
            <p>Understanding prime numbers, composite numbers, and their properties</p>
          </div>

          <div className="topic-card">
            <h3>LCM & HCF</h3>
            <p>Least Common Multiple and Highest Common Factor calculations</p>
          </div>

          <div className="topic-card">
            <h3>Factorials</h3>
            <p>Factorial calculations and applications in permutations</p>
          </div>

          <div className="topic-card">
            <h3>Number Series</h3>
            <p>Identify patterns and complete number sequences</p>
          </div>

          <div className="topic-card">
            <h3>Divisibility Rules</h3>
            <p>Quick divisibility tests for numbers 2-11 and beyond</p>
          </div>
        </div>
      </section>

      {/* Essential Formulas Section */}
      <section className="topic-section">
        <div className="section-header">
          <h2><FaChartLine /> Essential Formulas</h2>
          <p>Key mathematical formulas for quick problem solving</p>
        </div>

        <div className="topics-grid">
          <div className="topic-card">
            <h3>Percentage Calculations</h3>
            <p>Percentage to fraction conversion and percentage change problems</p>
          </div>

          <div className="topic-card">
            <h3>Profit and Loss</h3>
            <p>Calculate profit percentage, loss percentage, and break-even points</p>
          </div>

          <div className="topic-card">
            <h3>Simple and Compound Interest</h3>
            <p>Interest calculations for different time periods and rates</p>
          </div>

          <div className="topic-card">
            <h3>Ratio and Proportion</h3>
            <p>Direct and inverse proportions with practical applications</p>
          </div>

          <div className="topic-card">
            <h3>Time and Work</h3>
            <p>Work-rate problems and collaborative work calculations</p>
          </div>
        </div>
      </section>

      {/* Problem-Solving Techniques Section */}
      <section className="topic-section">
        <div className="section-header">
          <h2><FaLightbulb /> Problem-Solving Techniques</h2>
          <p>Strategic approaches to tackle quantitative problems</p>
        </div>

        <div className="topics-grid">
          <div className="topic-card">
            <h3>Back Calculation</h3>
            <p>Work backwards from answer choices to find the correct solution</p>
          </div>

          <div className="topic-card">
            <h3>Option Elimination</h3>
            <p>Eliminate incorrect options to narrow down choices</p>
          </div>

          <div className="topic-card">
            <h3>Approximation Methods</h3>
            <p>Use estimation techniques for quick calculations</p>
          </div>

          <div className="topic-card">
            <h3>Unitary Method</h3>
            <p>Find value of one unit to solve related problems</p>
          </div>

          <div className="topic-card">
            <h3>Allegation Method</h3>
            <p>Mix problems and weighted average calculations</p>
          </div>
        </div>
      </section>

      {/* Pro Tips Section */}
      <section className="tips-section">
        <div className="section-header">
          <h2><FaLightbulb /> Pro Tips for Success</h2>
        </div>

        <div className="tips-grid">
          <div className="tip-card">
            <div className="tip-icon">📚</div>
            <h3>Memorize important formulas and shortcuts</h3>
            <p>Create a formula sheet and review daily for quick recall during exams</p>
          </div>

          <div className="tip-card">
            <div className="tip-icon">⚡</div>
            <h3>Practice mental calculations to improve speed</h3>
            <p>Do basic arithmetic mentally without calculators to build speed</p>
          </div>

          <div className="tip-card">
            <div className="tip-icon">🧠</div>
            <h3>Understand the logic behind each formula</h3>
            <p>Don't just memorize - understand why formulas work the way they do</p>
          </div>

          <div className="tip-card">
            <div className="tip-icon">📝</div>
            <h3>Solve previous year question papers</h3>
            <p>Practice with actual exam questions to understand patterns and focus areas</p>
          </div>
        </div>
      </section>

      {/* Action Buttons */}
      <section className="action-section">
        <div className="action-buttons">
          <Link to="/qa-evaluation?area=aptitude" className="primary-button">
            <FaPlay /> Start Practice Test
          </Link>

          <button className="secondary-button">
            <FaDownload /> Download Study Material
          </button>
        </div>
      </section>
    </div>
  );
};

export default QuantitativeAptitude;
