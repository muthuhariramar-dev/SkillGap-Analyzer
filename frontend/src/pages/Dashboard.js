import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FaUser,
  FaEnvelope,
  FaEdit,
  FaFilePdf,
  FaUpload,
  FaRobot,
  FaChartLine,
  FaExclamationTriangle,
  FaRoad,
  FaCheckCircle,
  FaTimesCircle,
  FaLightbulb
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user, logout, authFetch, setUser } = useAuth();
  const navigate = useNavigate();
  const [isUploading, setIsUploading] = useState(false);
  const [atsResults, setAtsResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showATS, setShowATS] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null); // { type: 'success' | 'error', text: string }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const goToProfile = () => {
    navigate('/profile');
  };

  const downloadResume = () => {
    if (user?.resumeUrl) {
      const downloadUrl = `http://localhost:8000${user.resumeUrl}/download`;
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'Resume.pdf';
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const viewResume = () => {
    if (user?.resumeUrl) {
      const fullUrl = `http://localhost:8000${user.resumeUrl}`;
      window.open(fullUrl, '_blank');
    } else {
      goToProfile();
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setStatusMessage({ type: 'error', text: 'Only PDF files are allowed!' });
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);
    setStatusMessage(null);

    try {
      setIsUploading(true);
      const result = await authFetch('/api/resume/upload', {
        method: 'POST',
        body: formData,
      });

      if (result.fileUrl) {
        // Update the user state
        const updatedUser = { ...user, resumeUrl: result.fileUrl };
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));

        setStatusMessage({ type: 'success', text: 'Resume verified and uploaded successfully!' });

        // Automatically trigger ATS analysis
        handleATSCheck(result.fileUrl);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setStatusMessage({ type: 'error', text: error.message || 'Upload failed' });
    } finally {
      setIsUploading(false);
    }
  };

  const handleATSCheck = async (url) => {
    const resumeUrl = url || user?.resumeUrl;
    if (!resumeUrl) {
      setStatusMessage({ type: 'error', text: 'Please upload a resume first!' });
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await authFetch('/api/ats-check', {
        method: 'POST',
        body: JSON.stringify({ resumeUrl }),
      });

      setAtsResults(result);
      setShowATS(true);
      setStatusMessage({ type: 'success', text: 'ATS scan completed!' });
    } catch (error) {
      console.error('ATS analysis failed:', error);
      setStatusMessage({ type: 'error', text: `ATS analysis failed: ${error.message}` });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleStudentFeature = (feature) => {
    // Handle different student features - redirect to specific pages
    switch (feature) {
      case 'qa-evaluation':
        navigate('/qa-evaluation');
        break;
      case 'skill-analysis':
        navigate('/skill-analysis');
        break;
      case 'placement-risk':
        navigate('/preparation');
        break;
      case 'improvement-roadmap':
        navigate('/roadmap');
        break;
      default:
        setStatusMessage({ type: 'info', text: 'Feature coming soon!' });
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        <div className="user-info">
          <div className="user-avatar">
            <FaUser size={60} />
          </div>
          <div className="user-details">
            <h2>{user?.fullName || 'User'}</h2>
            <p><FaEnvelope /> {user?.email}</p>
            <span className="user-type">{user?.userType || 'student'}</span>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Resume Section */}
        <div className="resume-section">
          <div className="resume-header">
            <h2><FaFilePdf /> Resume Management</h2>
            <div className="resume-actions">
              {user?.resumeUrl && (
                <>
                  <button onClick={viewResume} className="btn btn-primary">
                    <FaFilePdf /> View
                  </button>
                  <button onClick={downloadResume} className="btn btn-secondary">
                    <FaFilePdf /> Download
                  </button>
                </>
              )}
              <div className="upload-wrapper">
                <input
                  type="file"
                  id="resume-upload-dash"
                  accept=".pdf"
                  onChange={handleResumeUpload}
                  style={{ display: 'none' }}
                />
                <label htmlFor="resume-upload-dash" className={`btn ${isUploading ? 'btn-disabled' : 'btn-ats'}`}>
                  <FaUpload /> {isUploading ? 'Uploading...' : user?.resumeUrl ? 'Update Resume' : 'Upload Resume'}
                </label>
              </div>
              {user?.resumeUrl && (
                <button
                  onClick={() => handleATSCheck()}
                  className="btn btn-ats"
                  disabled={isAnalyzing}
                >
                  <FaRobot /> {isAnalyzing ? 'Analyzing...' : 'Scan Resume (ATS)'}
                </button>
              )}
            </div>
          </div>

          {statusMessage && (
            <div className={`status-banner banner-${statusMessage.type}`}>
              {statusMessage.type === 'error' ? <FaExclamationTriangle /> : <FaCheckCircle />}
              <span>{statusMessage.text}</span>
              {statusMessage.type === 'error' && statusMessage.text.includes('mismatch') && (
                <p className="error-hint">Please ensure your resume contains your full name (<strong>{user?.fullName}</strong>) and email (<strong>{user?.email}</strong>).</p>
              )}
            </div>
          )}

          {!user?.resumeUrl && !statusMessage ? (
            <div className="no-resume-mini">
              <p>No resume uploaded. Upload a PDF resume to get an ATS score and optimization tips.</p>
            </div>
          ) : (
            <div className="resume-current-info">
              {user?.resumeUrl && (
                <>
                  <p>Current Resume: <strong>{user.resumeUrl.split('/').pop()}</strong></p>
                  {showATS && atsResults && (
                    <div className="dashboard-ats-results">
                      <div className="ats-main-stats">
                        <div className="ats-score-card">
                          <div className="score-value">{atsResults.score}%</div>
                          <div className="score-label">Overall ATS Score</div>
                        </div>
                        {atsResults.breakdown && (
                          <div className="ats-breakdown-card">
                            <h4>Score Breakdown</h4>
                            <div className="breakdown-item">
                              <span>Keywords</span>
                              <div className="progress-bar"><div className="progress" style={{ width: `${atsResults.breakdown.keywords}%` }}></div></div>
                            </div>
                            <div className="breakdown-item">
                              <span>Formatting</span>
                              <div className="progress-bar"><div className="progress" style={{ width: `${atsResults.breakdown.formatting}%` }}></div></div>
                            </div>
                            <div className="breakdown-item">
                              <span>Impact</span>
                              <div className="progress-bar"><div className="progress" style={{ width: `${atsResults.breakdown.impact}%` }}></div></div>
                            </div>
                            <div className="breakdown-item">
                              <span>Sections</span>
                              <div className="progress-bar"><div className="progress" style={{ width: `${atsResults.breakdown.sections}%` }}></div></div>
                            </div>
                          </div>
                        )}
                      </div>

                      <div className="ats-summary-grid">
                        <div className="ats-details-card">
                          <h4><FaCheckCircle className="icon-success" /> Strengths</h4>
                          <ul>
                            {atsResults.analysis?.strengths?.map((s, i) => <li key={i}>{s}</li>)}
                          </ul>
                        </div>
                        <div className="ats-details-card">
                          <h4><FaTimesCircle className="icon-warning" /> Improvements</h4>
                          <ul>
                            {atsResults.analysis?.improvements?.map((s, i) => <li key={i}>{s}</li>)}
                          </ul>
                        </div>
                      </div>

                      {atsResults.detected_skills?.length > 0 && (
                        <div className="ats-skills-cloud">
                          <h4>Keywords Detected</h4>
                          <div className="skills-tags">
                            {atsResults.detected_skills.map((skill, i) => (
                              <span key={i} className="skill-tag">{skill}</span>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="ats-optimization-section">
                        <h4><FaLightbulb className="icon-tip" /> Optimized Format Suggestions</h4>
                        <div className="optimization-grid">
                          {atsResults.analysis?.optimized_format?.map((tip, i) => (
                            <div key={i} className="optimization-tip">
                              {tip}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>

        {/* Quick Actions Section - Conditional based on user type */}
        <div className="quick-actions-section">
          <h2>{user?.userType === 'student' ? 'Student Quick Actions' : 'Professor Quick Actions'}</h2>
          <div className="action-grid">
            <button onClick={() => handleStudentFeature('qa-evaluation')} className="action-card">
              <FaRobot className="action-icon" />
              <span>Skill-based Q&A Evaluation</span>
            </button>
            <button onClick={() => handleStudentFeature('skill-analysis')} className="action-card">
              <FaChartLine className="action-icon" />
              <span>Role-specific Skill Analysis</span>
            </button>
            <button onClick={() => handleStudentFeature('placement-risk')} className="action-card">
              <FaExclamationTriangle className="action-icon" />
              <span>Placement Risk Awareness</span>
            </button>
            <button onClick={() => handleStudentFeature('improvement-roadmap')} className="action-card">
              <FaRoad className="action-icon" />
              <span>Personalized Improvement Roadmap</span>
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-actions">
        <button className="btn btn-primary" onClick={goToProfile}>
          <FaEdit /> Edit Profile
        </button>
        <button className="btn btn-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard;

