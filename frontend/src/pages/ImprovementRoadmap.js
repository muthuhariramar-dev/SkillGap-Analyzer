import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaRoad, FaArrowLeft, FaCheckCircle, FaClock, FaBook, FaCode, FaUsers, FaChartLine } from 'react-icons/fa';
import '../styles/ImprovementRoadmap.css';

const ImprovementRoadmap = () => {
  const navigate = useNavigate();
  const [roadmap, setRoadmap] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedFocus, setSelectedFocus] = useState('');

  const focusAreas = [
    { id: 'technical', name: 'Technical Skills', icon: <FaCode /> },
    { id: 'soft', name: 'Soft Skills', icon: <FaUsers /> },
    { id: 'career', name: 'Career Growth', icon: <FaChartLine /> }
  ];

  const generateRoadmap = (focusArea) => {
    setSelectedFocus(focusArea);
    setIsGenerating(true);
    
    setTimeout(() => {
      const mockRoadmap = generateMockRoadmap(focusArea);
      setRoadmap(mockRoadmap);
      setIsGenerating(false);
    }, 2000);
  };

  const generateMockRoadmap = (focus) => {
    const roadmaps = {
      technical: {
        title: 'Technical Skills Enhancement Roadmap',
        duration: '6-12 months',
        phases: [
          {
            phase: 'Foundation Building',
            duration: '1-3 months',
            status: 'current',
            tasks: [
              'Master core programming concepts',
              'Complete online courses (Coursera, Udemy)',
              'Build 3-4 fundamental projects',
              'Join coding communities'
            ],
            resources: [
              'FreeCodeCamp',
              'Codecademy',
              'LeetCode for practice',
              'GitHub for portfolio'
            ]
          },
          {
            phase: 'Skill Specialization',
            duration: '3-6 months',
            status: 'upcoming',
            tasks: [
              'Choose specialization (Frontend/Backend/Full-stack)',
              'Advanced framework learning',
              'Real-world project development',
              'Contribute to open source'
            ],
            resources: [
              'Advanced React/Vue courses',
              'Node.js/Python backend',
              'Database design courses',
              'Cloud platforms (AWS/Azure)'
            ]
          },
          {
            phase: 'Expert Level',
            duration: '6-12 months',
            status: 'future',
            tasks: [
              'System design mastery',
              'Architecture patterns',
              'Team leadership skills',
              'Mentoring others'
            ],
            resources: [
              'System design interviews',
              'Architecture patterns books',
              'Leadership courses',
              'Conference speaking'
            ]
          }
        ]
      },
      soft: {
        title: 'Soft Skills Development Roadmap',
        duration: '3-6 months',
        phases: [
          {
            phase: 'Communication Foundation',
            duration: '1-2 months',
            status: 'current',
            tasks: [
              'Public speaking practice',
              'Active listening exercises',
              'Written communication improvement',
              'Networking events attendance'
            ],
            resources: [
              'Toastmasters International',
              'Dale Carnegie courses',
              'Business writing workshops',
              'LinkedIn networking'
            ]
          },
          {
            phase: 'Leadership Development',
            duration: '2-4 months',
            status: 'upcoming',
            tasks: [
              'Team project leadership',
              'Conflict resolution practice',
              'Decision-making frameworks',
              'Mentoring junior members'
            ],
            resources: [
              'Leadership books',
              'Management courses',
              'Team building activities',
              'Executive coaching'
            ]
          },
          {
            phase: 'Executive Presence',
            duration: '4-6 months',
            status: 'future',
            tasks: [
              'Strategic thinking development',
              'Executive communication',
              'Stakeholder management',
              'Industry thought leadership'
            ],
            resources: [
              'Executive MBA programs',
              'Strategic management courses',
              'Industry conferences',
              'Thought leadership platforms'
            ]
          }
        ]
      },
      career: {
        title: 'Career Growth Roadmap',
        duration: '12-18 months',
        phases: [
          {
            phase: 'Career Assessment',
            duration: '1-2 months',
            status: 'current',
            tasks: [
              'Skills gap analysis',
              'Career goal setting',
              'Industry research',
              'Professional brand building'
            ],
            resources: [
              'LinkedIn Learning',
              'Industry reports',
              'Career counseling',
              'Personal branding workshops'
            ]
          },
          {
            phase: 'Skill Enhancement',
            duration: '3-8 months',
            status: 'upcoming',
            tasks: [
              'Targeted skill development',
              'Certification programs',
              'Industry networking',
              'Portfolio expansion'
            ],
            resources: [
              'Professional certifications',
              'Industry associations',
              'Networking events',
              'Portfolio platforms'
            ]
          },
          {
            phase: 'Career Advancement',
            duration: '8-18 months',
            status: 'future',
            tasks: [
              'Job search strategy',
              'Interview preparation',
              'Negotiation skills',
              'Career transition planning'
            ],
            resources: [
              'Job search platforms',
              'Interview coaching',
              'Salary negotiation courses',
              'Career transition services'
            ]
          }
        ]
      }
    };

    return roadmaps[focus] || roadmaps.technical;
  };

  const resetRoadmap = () => {
    setRoadmap(null);
    setSelectedFocus('');
    setIsGenerating(false);
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'current':
        return <FaClock className="status-icon current" />;
      case 'upcoming':
        return <FaCheckCircle className="status-icon upcoming" />;
      case 'future':
        return <FaRoad className="status-icon future" />;
      default:
        return <FaClock />;
    }
  };

  return (
    <div className="roadmap-container">
      <div className="roadmap-header">
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1><FaRoad /> Personalized Improvement Roadmap</h1>
        <p>Receive customized recommendations to enhance your skills and improve placement prospects</p>
      </div>

      {!roadmap ? (
        <div className="roadmap-intro">
          <div className="intro-card">
            <h2>Create Your Personalized Roadmap</h2>
            <p>
              Our AI-powered roadmap generator creates a customized development plan based on your 
              current skills, career goals, and industry requirements. Get step-by-step guidance 
              with timelines, resources, and milestones.
            </p>

            <div className="roadmap-features">
              <h3>What Your Roadmap Includes</h3>
              <div className="features-grid">
                <div className="feature-item">
                  <FaCheckCircle className="feature-icon" />
                  <h4>Phased Learning</h4>
                  <p>Structured phases with clear timelines</p>
                </div>
                <div className="feature-item">
                  <FaBook className="feature-icon" />
                  <h4>Curated Resources</h4>
                  <p>Best courses, books, and tools</p>
                </div>
                <div className="feature-item">
                  <FaClock className="feature-icon" />
                  <h4>Time Estimates</h4>
                  <p>Realistic duration for each phase</p>
                </div>
                <div className="feature-item">
                  <FaCode className="feature-icon" />
                  <h4>Practical Tasks</h4>
                  <p>Hands-on projects and exercises</p>
                </div>
              </div>
            </div>

            <div className="focus-selection">
              <h3>Select Your Focus Area</h3>
              <div className="focus-grid">
                {focusAreas.map((area) => (
                  <div
                    key={area.id}
                    className={`focus-card ${selectedFocus === area.id ? 'selected' : ''}`}
                    onClick={() => generateRoadmap(area.id)}
                  >
                    <div className="focus-icon">{area.icon}</div>
                    <h4>{area.name}</h4>
                    <button className="generate-btn" disabled={isGenerating}>
                      {isGenerating && selectedFocus === area.id ? 'Generating...' : 'Generate Roadmap'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="roadmap-results">
          <div className="results-header">
            <h2>Your Personalized Roadmap</h2>
            <p>{roadmap.title}</p>
            <div className="roadmap-duration">
              <strong>Estimated Duration:</strong> {roadmap.duration}
            </div>
          </div>

          <div className="roadmap-timeline">
            <h3>Development Phases</h3>
            <div className="timeline-container">
              {roadmap.phases.map((phase, index) => (
                <div key={index} className={`phase-card ${phase.status}`}>
                  <div className="phase-header">
                    <div className="phase-info">
                      <div className="phase-number">Phase {index + 1}</div>
                      <h4>{phase.phase}</h4>
                      <span className="phase-duration">{phase.duration}</span>
                    </div>
                    <div className="phase-status">
                      {getStatusIcon(phase.status)}
                      <span className="status-text">{phase.status}</span>
                    </div>
                  </div>

                  <div className="phase-content">
                    <div className="tasks-section">
                      <h5>Key Tasks</h5>
                      <ul>
                        {phase.tasks.map((task, taskIndex) => (
                          <li key={taskIndex}>{task}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="resources-section">
                      <h5>Recommended Resources</h5>
                      <div className="resources-grid">
                        {phase.resources.map((resource, resourceIndex) => (
                          <div key={resourceIndex} className="resource-item">
                            <FaBook className="resource-icon" />
                            <span>{resource}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="roadmap-tips">
            <h3>Success Tips</h3>
            <div className="tips-grid">
              <div className="tip-card">
                <h4>Stay Consistent</h4>
                <p>Dedicate regular time each week to follow your roadmap</p>
              </div>
              <div className="tip-card">
                <h4>Track Progress</h4>
                <p>Maintain a log of completed tasks and achievements</p>
              </div>
              <div className="tip-card">
                <h4>Seek Feedback</h4>
                <p>Get regular feedback from mentors and peers</p>
              </div>
              <div className="tip-card">
                <h4>Adapt as Needed</h4>
                <p>Adjust your roadmap based on learning and opportunities</p>
              </div>
            </div>
          </div>

          <div className="next-actions">
            <h3>Recommended Next Actions</h3>
            <div className="actions-list">
              <div className="action-item">
                <span className="action-number">1</span>
                <div className="action-content">
                  <h4>Start Phase 1 Today</h4>
                  <p>Begin with the foundation building tasks</p>
                </div>
              </div>
              <div className="action-item">
                <span className="action-number">2</span>
                <div className="action-content">
                  <h4>Set Up Learning Schedule</h4>
                  <p>Create a weekly calendar for consistent progress</p>
                </div>
              </div>
              <div className="action-item">
                <span className="action-number">3</span>
                <div className="action-content">
                  <h4>Join Learning Community</h4>
                  <p>Connect with others on similar learning paths</p>
                </div>
              </div>
            </div>
          </div>

          <div className="results-actions">
            <button className="action-btn primary" onClick={resetRoadmap}>
              Generate New Roadmap
            </button>
            <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImprovementRoadmap;
