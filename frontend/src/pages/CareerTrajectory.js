import React, { useState } from 'react';
import { careerTrajectoryService } from '../services/apiService';
import './CareerTrajectory.css';

const CareerTrajectory = () => {
  const [loading, setLoading] = useState(false);
  const [careerPath, setCareerPath] = useState(null);
  const [nextRoles, setNextRoles] = useState([]);
  const [formData, setFormData] = useState({
    current_role: '',
    target_role: '',
    user_skills: {},
    current_salary: 75000
  });
  const [skillInput, setSkillInput] = useState({ skill: '', level: 1 });
  const [activeTab, setActiveTab] = useState('prediction');

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Add current skill
  const addCurrentSkill = () => {
    if (skillInput.skill.trim()) {
      setFormData(prev => ({
        ...prev,
        user_skills: {
          ...prev.user_skills,
          [skillInput.skill]: skillInput.level
        }
      }));
      setSkillInput({ skill: '', level: 1 });
    }
  };

  // Remove current skill
  const removeCurrentSkill = (skill) => {
    setFormData(prev => {
      const newSkills = { ...prev.user_skills };
      delete newSkills[skill];
      return {
        ...prev,
        user_skills: newSkills
      };
    });
  };

  // Predict career trajectory
  const predictCareerTrajectory = async (e) => {
    e.preventDefault();
    
    if (!formData.current_role || !formData.target_role) {
      alert('Please fill in both current and target roles');
      return;
    }

    setLoading(true);
    try {
      const response = await careerTrajectoryService.predictCareerTrajectory(formData);
      if (response.success) {
        setCareerPath(response.career_path);
      } else {
        alert('Error predicting career trajectory: ' + response.message);
      }
    } catch (error) {
      console.error('Error predicting career trajectory:', error);
      alert('Failed to predict career trajectory. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Predict next roles
  const predictNextRoles = async (e) => {
    e.preventDefault();
    
    if (!formData.current_role) {
      alert('Please fill in your current role');
      return;
    }

    setLoading(true);
    try {
      const response = await careerTrajectoryService.predictNextRoles({
        current_role: formData.current_role,
        user_skills: formData.user_skills,
        top_k: 5
      });
      if (response.success) {
        setNextRoles(response.next_roles);
      } else {
        alert('Error predicting next roles: ' + response.message);
      }
    } catch (error) {
      console.error('Error predicting next roles:', error);
      alert('Failed to predict next roles. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="career-trajectory">
      <div className="container">
        <h1>Career Trajectory Prediction</h1>
        <p className="subtitle">
          Plan your career progression with AI-powered insights and predictions
        </p>

        <div className="form-container">
          <div className="tabs">
            <button 
              className={`tab ${activeTab === 'prediction' ? 'active' : ''}`}
              onClick={() => setActiveTab('prediction')}
            >
              Career Path Prediction
            </button>
            <button 
              className={`tab ${activeTab === 'next-roles' ? 'active' : ''}`}
              onClick={() => setActiveTab('next-roles')}
            >
              Next Best Roles
            </button>
          </div>

          {activeTab === 'prediction' && (
            <form onSubmit={predictCareerTrajectory}>
              {/* Current Role */}
              <div className="form-section">
                <h3>Current Position</h3>
                <div className="input-group">
                  <input
                    type="text"
                    name="current_role"
                    value={formData.current_role}
                    onChange={handleInputChange}
                    placeholder="e.g., Junior Data Analyst"
                    required
                  />
                  <input
                    type="number"
                    name="current_salary"
                    value={formData.current_salary}
                    onChange={handleInputChange}
                    placeholder="Current Salary ($)"
                    min="0"
                  />
                </div>
              </div>

              {/* Target Role */}
              <div className="form-section">
                <h3>Career Goal</h3>
                <div className="input-group">
                  <input
                    type="text"
                    name="target_role"
                    value={formData.target_role}
                    onChange={handleInputChange}
                    placeholder="e.g., Senior Data Scientist"
                    required
                  />
                </div>
              </div>

              {/* Current Skills */}
              <div className="form-section">
                <h3>Current Skills</h3>
                <div className="input-group">
                  <input
                    type="text"
                    value={skillInput.skill}
                    onChange={(e) => setSkillInput(prev => ({ ...prev, skill: e.target.value }))}
                    placeholder="Skill name"
                  />
                  <select
                    value={skillInput.level}
                    onChange={(e) => setSkillInput(prev => ({ ...prev, level: parseInt(e.target.value) }))}
                  >
                    <option value={1}>Beginner</option>
                    <option value={2}>Intermediate</option>
                    <option value={3}>Advanced</option>
                    <option value={4}>Expert</option>
                    <option value={5}>Master</option>
                  </select>
                  <button type="button" onClick={addCurrentSkill}>Add Skill</button>
                </div>
                <div className="tags-container">
                  {Object.entries(formData.user_skills).map(([skill, level]) => (
                    <span key={skill} className="tag">
                      {skill} (Level {level})
                      <button type="button" onClick={() => removeCurrentSkill(skill)}>×</button>
                    </span>
                  ))}
                </div>
              </div>

              <button type="submit" className="predict-btn" disabled={loading}>
                {loading ? 'Predicting...' : 'Predict Career Path'}
              </button>
            </form>
          )}

          {activeTab === 'next-roles' && (
            <form onSubmit={predictNextRoles}>
              {/* Current Role */}
              <div className="form-section">
                <h3>Current Position</h3>
                <div className="input-group">
                  <input
                    type="text"
                    name="current_role"
                    value={formData.current_role}
                    onChange={handleInputChange}
                    placeholder="e.g., Junior Data Analyst"
                    required
                  />
                </div>
              </div>

              {/* Current Skills */}
              <div className="form-section">
                <h3>Current Skills</h3>
                <div className="input-group">
                  <input
                    type="text"
                    value={skillInput.skill}
                    onChange={(e) => setSkillInput(prev => ({ ...prev, skill: e.target.value }))}
                    placeholder="Skill name"
                  />
                  <select
                    value={skillInput.level}
                    onChange={(e) => setSkillInput(prev => ({ ...prev, level: parseInt(e.target.value) }))}
                  >
                    <option value={1}>Beginner</option>
                    <option value={2}>Intermediate</option>
                    <option value={3}>Advanced</option>
                    <option value={4}>Expert</option>
                    <option value={5}>Master</option>
                  </select>
                  <button type="button" onClick={addCurrentSkill}>Add Skill</button>
                </div>
                <div className="tags-container">
                  {Object.entries(formData.user_skills).map(([skill, level]) => (
                    <span key={skill} className="tag">
                      {skill} (Level {level})
                      <button type="button" onClick={() => removeCurrentSkill(skill)}>×</button>
                    </span>
                  ))}
                </div>
              </div>

              <button type="submit" className="predict-btn" disabled={loading}>
                {loading ? 'Analyzing...' : 'Find Next Roles'}
              </button>
            </form>
          )}
        </div>

        {/* Career Path Results */}
        {careerPath && activeTab === 'prediction' && (
          <div className="results-container">
            <h2>Your Career Trajectory</h2>
            
            <div className="path-overview">
              <div className="overview-card">
                <h3>Career Path Overview</h3>
                <div className="path-steps">
                  {careerPath.steps && careerPath.steps.length > 0 && (
                    <div className="steps-container">
                      {careerPath.steps.map((step, index) => (
                        <div key={index} className="step-item">
                          <div className="step-number">{index + 1}</div>
                          <div className="step-content">
                            <h4>{step}</h4>
                            {index === 0 && <span className="current-badge">Current</span>}
                            {index === careerPath.steps.length - 1 && <span className="target-badge">Target</span>}
                          </div>
                          {index < careerPath.steps.length - 1 && <div className="step-arrow">→</div>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                
                <div className="path-metrics">
                  <div className="metric">
                    <h4>Estimated Timeline</h4>
                    <p>{careerPath.estimated_timeline} months</p>
                  </div>
                  <div className="metric">
                    <h4>Confidence Score</h4>
                    <p>{(careerPath.confidence_score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="metric">
                    <h4>Skill Gaps</h4>
                    <p>{Object.keys(careerPath.required_skills || {}).length} skills to develop</p>
                  </div>
                </div>
              </div>
            </div>

            {careerPath.required_skills && Object.keys(careerPath.required_skills).length > 0 && (
              <div className="skill-gaps">
                <h3>Required Skill Development</h3>
                <div className="gaps-grid">
                  {Object.entries(careerPath.required_skills).map(([skill, gap]) => (
                    <div key={skill} className="gap-card">
                      <h4>{skill}</h4>
                      <p><strong>Gap Level:</strong> {gap}</p>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ width: `${Math.max(0, 100 - gap * 20)}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Next Roles Results */}
        {nextRoles.length > 0 && activeTab === 'next-roles' && (
          <div className="results-container">
            <h2>Recommended Next Roles</h2>
            <div className="roles-grid">
              {nextRoles.map((role, index) => (
                <div key={index} className="role-card">
                  <div className="role-header">
                    <h3>{role[0]}</h3>
                    <div className="confidence-score">
                      {(role[1] * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill" 
                      style={{ width: `${role[1] * 100}%` }}
                    ></div>
                  </div>
                  <p className="match-description">
                    This role matches your profile and skills with high confidence
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CareerTrajectory;
