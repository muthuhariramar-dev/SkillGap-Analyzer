import React, { useState } from 'react';
import { learningPathGenerationService } from '../services/apiService';
import './LearningPathGeneration.css';

const LearningPathGeneration = () => {
  const [loading, setLoading] = useState(false);
  const [learningPath, setLearningPath] = useState(null);
  const [formData, setFormData] = useState({
    target_skills: [],
    current_skills: {},
    learning_goals: [],
    time_availability: 5
  });
  const [skillInput, setSkillInput] = useState('');
  const [goalInput, setGoalInput] = useState('');
  const [currentSkillInput, setCurrentSkillInput] = useState({ skill: '', level: 1 });

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Add target skill
  const addTargetSkill = () => {
    if (skillInput.trim()) {
      setFormData(prev => ({
        ...prev,
        target_skills: [...prev.target_skills, skillInput.trim()]
      }));
      setSkillInput('');
    }
  };

  // Add learning goal
  const addLearningGoal = () => {
    if (goalInput.trim()) {
      setFormData(prev => ({
        ...prev,
        learning_goals: [...prev.learning_goals, goalInput.trim()]
      }));
      setGoalInput('');
    }
  };

  // Add current skill
  const addCurrentSkill = () => {
    if (currentSkillInput.skill.trim()) {
      setFormData(prev => ({
        ...prev,
        current_skills: {
          ...prev.current_skills,
          [currentSkillInput.skill]: currentSkillInput.level
        }
      }));
      setCurrentSkillInput({ skill: '', level: 1 });
    }
  };

  // Remove target skill
  const removeTargetSkill = (index) => {
    setFormData(prev => ({
      ...prev,
      target_skills: prev.target_skills.filter((_, i) => i !== index)
    }));
  };

  // Remove learning goal
  const removeLearningGoal = (index) => {
    setFormData(prev => ({
      ...prev,
      learning_goals: prev.learning_goals.filter((_, i) => i !== index)
    }));
  };

  // Remove current skill
  const removeCurrentSkill = (skill) => {
    setFormData(prev => {
      const newCurrentSkills = { ...prev.current_skills };
      delete newCurrentSkills[skill];
      return {
        ...prev,
        current_skills: newCurrentSkills
      };
    });
  };

  // Generate learning path
  const generateLearningPath = async (e) => {
    e.preventDefault();
    
    if (formData.target_skills.length === 0) {
      alert('Please add at least one target skill');
      return;
    }

    setLoading(true);
    try {
      const response = await learningPathGenerationService.generateLearningPath(formData);
      if (response.success) {
        setLearningPath(response.learning_path);
      } else {
        alert('Error generating learning path: ' + response.message);
      }
    } catch (error) {
      console.error('Error generating learning path:', error);
      alert('Failed to generate learning path. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="learning-path-generation">
      <div className="container">
        <h1>Personalized Learning Path Generation</h1>
        <p className="subtitle">
          Generate a customized learning path based on your current skills and career goals
        </p>

        <div className="form-container">
          <form onSubmit={generateLearningPath}>
            {/* Target Skills Section */}
            <div className="form-section">
              <h3>Target Skills</h3>
              <div className="input-group">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  placeholder="Enter a skill you want to learn (e.g., Python, Data Science)"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTargetSkill())}
                />
                <button type="button" onClick={addTargetSkill}>Add Skill</button>
              </div>
              <div className="tags-container">
                {formData.target_skills.map((skill, index) => (
                  <span key={index} className="tag">
                    {skill}
                    <button type="button" onClick={() => removeTargetSkill(index)}>×</button>
                  </span>
                ))}
              </div>
            </div>

            {/* Current Skills Section */}
            <div className="form-section">
              <h3>Current Skills</h3>
              <div className="input-group">
                <input
                  type="text"
                  value={currentSkillInput.skill}
                  onChange={(e) => setCurrentSkillInput(prev => ({ ...prev, skill: e.target.value }))}
                  placeholder="Skill name"
                />
                <select
                  value={currentSkillInput.level}
                  onChange={(e) => setCurrentSkillInput(prev => ({ ...prev, level: parseInt(e.target.value) }))}
                >
                  <option value={1}>Beginner</option>
                  <option value={2}>Intermediate</option>
                  <option value={3}>Advanced</option>
                  <option value={4}>Expert</option>
                </select>
                <button type="button" onClick={addCurrentSkill}>Add Current Skill</button>
              </div>
              <div className="tags-container">
                {Object.entries(formData.current_skills).map(([skill, level]) => (
                  <span key={skill} className="tag">
                    {skill} (Level {level})
                    <button type="button" onClick={() => removeCurrentSkill(skill)}>×</button>
                  </span>
                ))}
              </div>
            </div>

            {/* Learning Goals Section */}
            <div className="form-section">
              <h3>Learning Goals</h3>
              <div className="input-group">
                <input
                  type="text"
                  value={goalInput}
                  onChange={(e) => setGoalInput(e.target.value)}
                  placeholder="Enter your learning goal (e.g., Get a job in Data Science)"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addLearningGoal())}
                />
                <button type="button" onClick={addLearningGoal}>Add Goal</button>
              </div>
              <div className="tags-container">
                {formData.learning_goals.map((goal, index) => (
                  <span key={index} className="tag">
                    {goal}
                    <button type="button" onClick={() => removeLearningGoal(index)}>×</button>
                  </span>
                ))}
              </div>
            </div>

            {/* Time Availability Section */}
            <div className="form-section">
              <h3>Time Availability</h3>
              <div className="input-group">
                <label>Hours per week:</label>
                <input
                  type="number"
                  name="time_availability"
                  value={formData.time_availability}
                  onChange={handleInputChange}
                  min="1"
                  max="40"
                />
              </div>
            </div>

            <button type="submit" className="generate-btn" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Learning Path'}
            </button>
          </form>
        </div>

        {/* Learning Path Results */}
        {learningPath && (
          <div className="results-container">
            <h2>Your Personalized Learning Path</h2>
            <div className="path-summary">
              <div className="summary-card">
                <h4>Path Overview</h4>
                <p><strong>Path ID:</strong> {learningPath.path_id}</p>
                <p><strong>Estimated Duration:</strong> {learningPath.estimated_duration} weeks</p>
                <p><strong>Total Skills:</strong> {learningPath.learning_path?.length || 0}</p>
                <p><strong>Difficulty:</strong> {learningPath.difficulty_level}</p>
              </div>
            </div>

            {learningPath.learning_path && learningPath.learning_path.length > 0 && (
              <div className="learning-modules">
                <h3>Learning Modules</h3>
                {learningPath.learning_path.map((module, index) => (
                  <div key={index} className="module-card">
                    <div className="module-header">
                      <h4>{module.skill}</h4>
                      <span className="difficulty-badge">
                        Level {module.difficulty}
                      </span>
                    </div>
                    <div className="module-content">
                      <p><strong>Category:</strong> {module.category}</p>
                      <p><strong>Estimated Time:</strong> {module.estimated_time} minutes</p>
                      
                      {module.learning_objectives && (
                        <div className="objectives">
                          <strong>Learning Objectives:</strong>
                          <ul>
                            {module.learning_objectives.map((objective, i) => (
                              <li key={i}>{objective}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {module.recommended_content && module.recommended_content.length > 0 && (
                        <div className="resources">
                          <strong>Recommended Resources:</strong>
                          <ul>
                            {module.recommended_content.map((resource, i) => (
                              <li key={i}>
                                <a href={resource.url} target="_blank" rel="noopener noreferrer">
                                  {resource.title}
                                </a>
                                <span className="resource-type">({resource.type})</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {module.assessments && module.assessments.length > 0 && (
                        <div className="assessments">
                          <strong>Assessments:</strong>
                          <ul>
                            {module.assessments.map((assessment, i) => (
                              <li key={i}>
                                {assessment.title} - {assessment.duration} minutes
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {learningPath.milestones && learningPath.milestones.length > 0 && (
              <div className="milestones">
                <h3>Learning Milestones</h3>
                {learningPath.milestones.map((milestone, index) => (
                  <div key={index} className="milestone-card">
                    <h4>Week {milestone.week}: {milestone.title}</h4>
                    <p><strong>Skills:</strong> {milestone.modules?.join(', ') || 'N/A'}</p>
                    <p><strong>Estimated Time:</strong> {milestone.estimated_time} minutes</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LearningPathGeneration;
