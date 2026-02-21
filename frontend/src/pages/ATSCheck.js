import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaFileUpload, FaArrowLeft, FaCheck, FaTimes, FaExclamationTriangle, FaDownload } from 'react-icons/fa';
import '../styles/ATSCheck.css';

const ATSCheck = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file.type === 'application/pdf' || file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      setSelectedFile(file);
    } else {
      alert('Please upload a PDF or Word document');
    }
  };

  const analyzeResume = async () => {
    if (!selectedFile) return;
    
    setIsAnalyzing(true);
    
    // Simulate API call for ATS analysis
    setTimeout(() => {
      const mockResults = generateMockATSResults();
      setAnalysisResults(mockResults);
      setIsAnalyzing(false);
    }, 3000);
  };

  const generateMockATSResults = () => {
    const score = Math.floor(Math.random() * 30) + 70; // Score between 70-100
    
    const issues = [
      { type: 'format', severity: 'medium', message: 'Resume uses tables which may not be parsed correctly by all ATS systems' },
      { type: 'keywords', severity: 'high', message: 'Missing important keywords for your target role' },
      { type: 'contact', severity: 'low', message: 'Consider adding LinkedIn profile URL' }
    ];

    const strengths = [
      'Clear section headers',
      'Good use of bullet points',
      'Professional email address',
      'Consistent formatting'
    ];

    const recommendations = [
      'Remove tables and use standard formatting',
      'Add industry-specific keywords from job descriptions',
      'Include quantifiable achievements',
      'Optimize file name (e.g., "John_Doe_Resume.pdf")'
    ];

    return {
      overallScore: score,
      atsCompatibility: score >= 85 ? 'Excellent' : score >= 70 ? 'Good' : 'Needs Improvement',
      issues: issues,
      strengths: strengths,
      recommendations: recommendations,
      parsedSections: [
        { name: 'Contact Information', status: 'found' },
        { name: 'Professional Summary', status: 'found' },
        { name: 'Work Experience', status: 'found' },
        { name: 'Education', status: 'found' },
        { name: 'Skills', status: score > 75 ? 'found' : 'missing' }
      ]
    };
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setAnalysisResults(null);
    setIsAnalyzing(false);
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'high': return <FaExclamationTriangle className="severity-high" />;
      case 'medium': return <FaExclamationTriangle className="severity-medium" />;
      case 'low': return <FaTimes className="severity-low" />;
      default: return null;
    }
  };

  return (
    <div className="ats-check-container">
      <div className="ats-check-header">
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1><FaFileUpload /> ATS Resume Checker</h1>
        <p>Analyze your resume for Applicant Tracking System compatibility</p>
      </div>

      {!analysisResults ? (
        <div className="upload-section">
          <div className="upload-area">
            <form 
              className={`upload-form ${dragActive ? 'drag-active' : ''}`}
              onDragEnter={handleDrag}
              onSubmit={(e) => e.preventDefault()}
            >
              <input 
                type="file" 
                id="resume-upload"
                accept=".pdf,.doc,.docx"
                onChange={handleChange}
                style={{ display: 'none' }}
              />
              <label 
                htmlFor="resume-upload"
                className="upload-label"
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="upload-content">
                  <FaFileUpload className="upload-icon" />
                  <h3>Drop your resume here or click to browse</h3>
                  <p>Supported formats: PDF, DOC, DOCX</p>
                  {selectedFile && (
                    <div className="selected-file">
                      <span>Selected: {selectedFile.name}</span>
                    </div>
                  )}
                </div>
              </label>
            </form>
          </div>

          {selectedFile && (
            <div className="upload-actions">
              <button 
                className="analyze-btn primary"
                onClick={analyzeResume}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? 'Analyzing...' : 'Analyze Resume'}
              </button>
              <button className="analyze-btn secondary" onClick={resetAnalysis}>
                Choose Different File
              </button>
            </div>
          )}

          {isAnalyzing && (
            <div className="analyzing-indicator">
              <div className="spinner"></div>
              <p>Analyzing your resume with ATS scanner...</p>
            </div>
          )}
        </div>
      ) : (
        <div className="analysis-results">
          <div className="results-header">
            <h2>ATS Analysis Results</h2>
            <div className="score-display">
              <div className="score-circle">
                <span className="score-percentage">{analysisResults.overallScore}%</span>
                <span className="score-label">ATS Score</span>
              </div>
              <div className="compatibility-badge">
                <span className={`badge ${analysisResults.atsCompatibility.toLowerCase().replace(' ', '-')}`}>
                  {analysisResults.atsCompatibility}
                </span>
              </div>
            </div>
          </div>

          <div className="parsed-sections">
            <h3>Resume Sections Detected</h3>
            <div className="sections-grid">
              {analysisResults.parsedSections.map((section, index) => (
                <div key={index} className={`section-item ${section.status}`}>
                  <div className="section-icon">
                    {section.status === 'found' ? <FaCheck /> : <FaTimes />}
                  </div>
                  <span className="section-name">{section.name}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="issues-section">
            <h3>Issues Found</h3>
            <div className="issues-list">
              {analysisResults.issues.map((issue, index) => (
                <div key={index} className={`issue-item ${issue.severity}`}>
                  <div className="issue-icon">
                    {getSeverityIcon(issue.severity)}
                  </div>
                  <div className="issue-content">
                    <span className="issue-type">{issue.type}</span>
                    <p className="issue-message">{issue.message}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="strengths-section">
            <h3>Strengths</h3>
            <div className="strengths-list">
              {analysisResults.strengths.map((strength, index) => (
                <div key={index} className="strength-item">
                  <FaCheck className="strength-icon" />
                  <span>{strength}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="recommendations-section">
            <h3>Recommendations</h3>
            <div className="recommendations-list">
              {analysisResults.recommendations.map((rec, index) => (
                <div key={index} className="recommendation-item">
                  <span className="rec-number">{index + 1}</span>
                  <p>{rec}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="results-actions">
            <button className="action-btn primary" onClick={resetAnalysis}>
              Analyze Another Resume
            </button>
            <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </button>
            <button className="action-btn tertiary">
              <FaDownload /> Download Report
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ATSCheck;
