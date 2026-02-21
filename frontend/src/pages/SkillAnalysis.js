import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaCode, FaBriefcase, FaUsers, FaLightbulb, FaWordpress, FaMobile, FaGamepad, FaDatabase, FaServer, FaFlask, FaShieldAlt, FaPalette, FaQuestion, FaTimesCircle, FaExpand, FaExclamationTriangle } from 'react-icons/fa';
import { API_ENDPOINTS } from '../config/api';
import { formatRoleToKebab } from '../utils/datasetMapping';
import '../styles/SkillAnalysis.css';
import '../styles/RoleApproach.css';
import CameraMonitor from '../components/CameraMonitor';

// Map to local convenience names used throughout this component
const ENDPOINTS = {
  GENERATE_ROLE_QUESTIONS: API_ENDPOINTS.GENERATE_ROLE_QUESTIONS,
  ANALYZE_ROLE_RESULTS: API_ENDPOINTS.ANALYZE_ROLE_RESULTS,
  PROCTOR_START: API_ENDPOINTS.START_CAMERA,
  PROCTOR_ANALYZE_FRAME: API_ENDPOINTS.ANALYZE_FRAME,
  PROCTOR_CHECK_FULLSCREEN: `${API_ENDPOINTS.START_CAMERA.replace('/camera/start', '/check-fullscreen')}`,
  PROCTOR_TERMINATE: `${API_ENDPOINTS.START_CAMERA.replace('/camera/start', '/terminate')}`,
  QUESTIONS: API_ENDPOINTS.QUESTIONS
};

const SkillAnalysis = () => {
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState('');
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [proctorMode, setProctorMode] = useState(false);
  const [cameraEnabled, setCameraEnabled] = useState(false);
  const [error, setError] = useState(null);
  const [terminationReason, setTerminationReason] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // Security Event Listeners
  useEffect(() => {
    if (proctorMode) {
      const handleContextMenu = (e) => e.preventDefault();
      const handleCopy = (e) => e.preventDefault();
      const handlePaste = (e) => e.preventDefault();
      const handleKeyDown = (e) => {
        // block typical shortcuts
        if ((e.ctrlKey && ['r', 'c', 'v', 'p', 'f'].includes(e.key)) || e.code === 'F5' || (e.altKey && e.code === 'Tab')) {
          e.preventDefault();
          alert("This action is disabled during the assessment.");
        }
      };

      document.addEventListener('contextmenu', handleContextMenu);
      document.addEventListener('copy', handleCopy);
      document.addEventListener('paste', handlePaste);
      window.addEventListener('keydown', handleKeyDown);

      // Disable back button
      window.history.pushState(null, document.title, window.location.href);
      const handlePopState = () => {
        window.history.pushState(null, document.title, window.location.href);
        alert("Navigation is disabled during the assessment.");
      };
      window.addEventListener('popstate', handlePopState);

      return () => {
        document.removeEventListener('contextmenu', handleContextMenu);
        document.removeEventListener('copy', handleCopy);
        document.removeEventListener('paste', handlePaste);
        window.removeEventListener('keydown', handleKeyDown);
        window.removeEventListener('popstate', handlePopState);
      };
    }
  }, [proctorMode]);

  const jobRoles = useMemo(() => [
    {
      id: 'frontend-developer',
      title: 'Frontend Developer',
      icon: <FaCode />,
      requiredSkills: ['HTML/CSS', 'JavaScript', 'React/Vue', 'Responsive Design', 'UI/UX'],
      description: 'Build user interfaces and web applications',
      approachMethod: {
        steps: [
          'Master Semantic HTML and CSS Layouts (Flexbox/Grid)',
          'Deep dive into ES6+ JavaScript and DOM manipulation',
          'Learn a modern framework like React, Vue, or Angular',
          'Practice building responsive UI components with clean code',
          'Understand performance optimization and accessibility'
        ],
        prepGuide: 'Focus on core JavaScript concepts and React hooks. Practice building a small project like a task manager or weather app.'
      }
    },
    {
      id: 'backend-developer',
      title: 'Backend Developer',
      icon: <FaCode />,
      requiredSkills: ['Node.js/Python', 'Databases', 'APIs', 'Security', 'Cloud Services'],
      description: 'Develop server-side applications and APIs',
      approachMethod: {
        steps: [
          'Choose a backend language (Node.js, Python, or Java)',
          'Learn to design and query SQL and NoSQL databases',
          'Understand RESTful API design and authentication',
          'Learn server management and cloud deployment (AWS/Azure)',
          'Master security best practices and data protection'
        ],
        prepGuide: 'Build a secure REST API with authentication. Practice database schema design and optimization.'
      }
    },
    {
      id: 'fullstack-developer',
      title: 'Full Stack Developer',
      icon: <FaCode />,
      requiredSkills: ['Frontend', 'Backend', 'Databases', 'DevOps', 'System Design'],
      description: 'Work on both frontend and backend development',
      approachMethod: {
        steps: [
          'Integrate frontend applications with backend services',
          'Manage end-to-end development lifecycle',
          'Deploy applications using CI/CD pipelines',
          'Optimize full-stack performance and scalability',
          'Master cross-functional communication and system design'
        ],
        prepGuide: 'Create a complete web application from scratch. Focus on integrating the frontend and backend efficiently.'
      }
    },
    {
      id: 'data-scientist',
      title: 'Data Scientist',
      icon: <FaFlask />,
      requiredSkills: ['Machine Learning', 'Python/R', 'Statistics', 'Data Visualization', 'Deep Learning'],
      description: 'Analyze data and build predictive models',
      approachMethod: {
        steps: [
          'Master statistical analysis and probability',
          'Learn data manipulation with Python (Pandas/NumPy)',
          'Study machine learning algorithms and evaluation',
          'Practice data visualization with Matplotlib or Seaborn',
          'Work on real-world datasets and Kaggle competitions'
        ],
        prepGuide: 'Work through a complete data analysis project. Focus on model selection and feature engineering.'
      }
    },
    {
      id: 'product-manager',
      title: 'Product Manager',
      icon: <FaBriefcase />,
      requiredSkills: ['Strategy', 'Communication', 'Analytics', 'User Research', 'Leadership'],
      description: 'Guide product development and strategy'
    },
    {
      id: 'team-lead',
      title: 'Team Lead',
      icon: <FaUsers />,
      requiredSkills: ['Leadership', 'Communication', 'Project Management', 'Technical Skills', 'Mentoring'],
      description: 'Lead development teams and projects'
    },
    {
      id: 'ui-ux-designer',
      title: 'UI/UX Designer',
      icon: <FaLightbulb />,
      requiredSkills: ['Design Tools', 'User Research', 'Prototyping', 'Visual Design', 'Accessibility'],
      description: 'Create user-centered designs and experiences'
    },
    {
      id: 'wordpress-developer',
      title: 'WordPress Developer',
      icon: <FaWordpress />,
      requiredSkills: ['WordPress', 'PHP', 'MySQL', 'Plugin Development', 'Theme Development'],
      description: 'Build and customize WordPress websites and applications'
    },
    {
      id: 'software-engineer-agile',
      title: 'Software Engineer[AGILE]',
      icon: <FaCode />,
      requiredSkills: ['Agile Methodologies', 'Scrum', 'Software Development', 'Testing', 'Team Collaboration'],
    },
    {
      id: 'mobile-developer',
      title: 'Mobile Developer',
      icon: <FaMobile />,
      requiredSkills: ['React Native/Flutter', 'iOS/Android', 'Mobile UI/UX', 'App Store Deployment', 'Performance Optimization'],
      description: 'Create mobile applications for iOS and Android platforms'
    },
    {
      id: 'game-developer',
      title: 'Game Developer',
      icon: <FaGamepad />,
      requiredSkills: ['Unity/Unreal Engine', 'C#/C++', 'Game Design', '3D Modeling', 'Physics Simulation'],
      description: 'Develop interactive games and gaming experiences'
    },
    {
      id: 'big-data-developer',
      title: 'Big Data Developer',
      icon: <FaDatabase />,
      requiredSkills: ['Hadoop/Spark', 'Data Processing', 'Python/R', 'SQL/NoSQL', 'Data Warehousing'],
      description: 'Work with large-scale data processing and analytics'
    },
    {
      id: 'devops-engineer',
      title: 'Developmental Operations Engineer',
      icon: <FaServer />,
      requiredSkills: ['CI/CD', 'Docker/Kubernetes', 'Cloud Platforms', 'Monitoring', 'Infrastructure as Code'],
      description: 'Manage deployment pipelines and infrastructure'
    },
    {
      id: 'security-developer',
      title: 'Security Developer',
      icon: <FaShieldAlt />,
      requiredSkills: ['Cybersecurity', 'Penetration Testing', 'Secure Coding', 'Cryptography', 'Risk Assessment'],
      description: 'Develop secure applications and security systems'
    },
    {
      id: 'graphics-developer',
      title: 'Graphics Developer',
      icon: <FaPalette />,
      requiredSkills: ['OpenGL/WebGL', '3D Graphics', 'Shader Programming', 'Rendering', 'Mathematics'],
      description: 'Create graphics engines and visual effects'
    }
  ], []);

  const handleStartAssessment = useCallback(async (roleIdOverride) => {
    setIsLoading(true);
    setError(null);

    const roleId = roleIdOverride || selectedRole;
    if (!roleId) {
      setIsLoading(false);
      return;
    }

    try {
      // Enable proctor mode and request camera access
      setProctorMode(true);

      // Auto enter fullscreen
      try {
        if (document.documentElement.requestFullscreen) {
          await document.documentElement.requestFullscreen();
        }
      } catch (fsErr) {
        console.warn('Could not enter fullscreen automatically', fsErr);
      }

      // Camera logic handled by CameraMonitor
      setCameraEnabled(true);

      // Start proctoring session when role is selected
      // Start proctoring session when role is selected
      if (roleId) {
        try {
          // Start proctoring session
          const proctorResponse = await fetch(ENDPOINTS.PROCTOR_START, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              sessionId: `session_${Date.now()}_${roleId}`,
              userId: localStorage.getItem('userId') || 'anonymous',
              role: roleId
            })
          });

          const proctorResult = await proctorResponse.json();

          if (proctorResult.success) {
            console.log('Proctoring session started:', proctorResult.sessionId);
          }
        } catch (proctorErr) {
          console.warn('Proctoring session start failed:', proctorErr);
        }
      }

      const role = jobRoles.find(r => r.id === roleId);

      // Convert role title to dataset slug (e.g., "Frontend Developer" -> "frontend-developer")
      const roleSlug = formatRoleToKebab(role.title);

      const response = await axios.get(`${ENDPOINTS.QUESTIONS}/${roleSlug}`, {
        headers: {
          'Content-Type': 'application/json'
        },
        params: {
          limit: 10 // Only fetch 10 questions for the assessment
        }
      });

      if (response.data.success) {
        setQuestions(response.data.questions);
        setCurrentQuestionIndex(1); // Start with first question (index 1, not 0)
        setAnswers([]);
        setShowResults(false);
        setError(null);
        setProctorMode(true);
      } else {
        throw new Error('Failed to generate questions');
      }

    } catch (err) {
      const errorMsg = `Error: ${err.response?.data?.message || err.message || 'Failed to load assessment'}`;
      console.error('Error generating questions:', err);
      // Fallback logic kept for safety
      setError(errorMsg + ". Using local fallback.");

      const role = jobRoles.find(r => r.id === roleId) || { title: roleId, requiredSkills: ['General'] };
      const fallback = Array.from({ length: 10 }).map((_, i) => ({
        id: `fallback-${selectedRole}-q${i + 1}`,
        question: `${role.title} - Sample question ${i + 1}`,
        options: ['Option A', 'Option B', 'Option C', 'Option D'],
        correct: 0,
        skill: role.requiredSkills[i % role.requiredSkills.length]
      }));
      setQuestions(fallback);
      setCurrentQuestionIndex(1);
      setAnswers([]);
      setShowResults(false);
      setProctorMode(true);

    } finally {
      setIsLoading(false);
    }
  }, [selectedRole, jobRoles]);

  // Stream handling moved to CameraMonitor

  const handleAssessmentTermination = useCallback(async (reason) => {
    try {
      // Exit fullscreen if active
      if (document.fullscreenElement) {
        try { await document.exitFullscreen(); } catch (e) { }
      }

      // Turn off cameras
      setProctorMode(false);
      setCameraEnabled(false);

      const token = localStorage.getItem('token');
      try {
        await fetch(ENDPOINTS.PROCTOR_TERMINATE, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            sessionId: `session_${Date.now()}_${selectedRole}`,
            reason: reason
          })
        });
      } catch (err) {
        console.warn('Backend termination notify failed', err);
      }

      // Set termination reason and show results view (which now handles violations)
      setTerminationReason(reason);
      setShowResults(true);
    } catch (error) {
      console.error('Error terminating assessment:', error);
    }
  }, [selectedRole]);

  // Check fullscreen violations
  const checkFullscreenViolation = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(ENDPOINTS.PROCTOR_CHECK_FULLSCREEN, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sessionId: `session_${Date.now()}_${selectedRole}`
        })
      });

      const result = await response.json();

      if (result.success && result.fullscreenStatus.violations >= 3) {
        // Terminate assessment due to excessive fullscreen violations
        handleAssessmentTermination('EXCESSIVE_FULLSCREEN_VIOLATIONS');
      }
    } catch (error) {
      console.error('Error checking fullscreen violation:', error);
    }
  }, [selectedRole, handleAssessmentTermination]);

  // Fullscreen change listener
  useEffect(() => {
    const onFsChange = () => {
      // Check fullscreen violations with backend
      if (proctorMode && selectedRole) {
        checkFullscreenViolation();
      }
    };
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, [proctorMode, selectedRole, checkFullscreenViolation]);

  // (Duplicate handleAssessmentTermination removed - using useCallback version above)

  const toggleFullscreen = async () => {
    if (!videoRef.current) return;
    try {
      if (!document.fullscreenElement) {
        await videoRef.current.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    } catch (e) {
      console.warn('Fullscreen toggle failed', e);
    }
  };

  // Ensure stream is stopped on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        try { streamRef.current.getTracks().forEach(t => t.stop()); } catch (e) { }
        streamRef.current = null;
      }
    };
  }, []);


  const handleAnswerSelect = (questionId, selectedOptionIndex) => {
    const newAnswers = answers.filter(a => a.questionId !== questionId);
    newAnswers.push({ questionId, selectedOptionIndex });
    setAnswers(newAnswers);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      handleSubmitAnswers();
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 1) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  // Fallback analysis generator when backend is unavailable
  const generateFallbackAnalysis = () => {
    const role = jobRoles.find(r => r.id === selectedRole);

    // Calculate correct answers
    let correctCount = 0;
    const skillCorrects = {};
    const skillTotals = {};

    questions.forEach((q) => {
      const userAnswer = answers.find(a => a.questionId === q.id);
      const skillName = q.skill;

      if (!skillTotals[skillName]) {
        skillTotals[skillName] = 0;
        skillCorrects[skillName] = 0;
      }

      skillTotals[skillName]++;

      if (userAnswer && userAnswer.selectedOptionIndex === q.correct) {
        correctCount++;
        skillCorrects[skillName]++;
      }
    });

    const totalCount = questions.length;
    const score = totalCount > 0 ? Math.round((correctCount / totalCount) * 100) : 0;

    // Build skill scores
    const skillScores = role.requiredSkills.map((skillName) => {
      const correct = skillCorrects[skillName] || 0;
      const total = skillTotals[skillName] || 1;
      const skillScore = total > 0 ? Math.round((correct / total) * 100) : 0;

      return {
        skill: skillName,
        level: skillScore >= 80 ? 'Advanced' : skillScore >= 60 ? 'Intermediate' : 'Beginner',
        score: skillScore,
        correct,
        total
      };
    });

    const readiness = score >= 75 ? 'High' : score >= 50 ? 'Medium' : 'Low';

    return {
      success: true,
      analysis: {
        overallScore: score,
        readiness,
        skillScores,
        recommendations: [
          `Focus on strengthening ${role.requiredSkills[0]} – a key requirement for ${role.title}`,
          `Take targeted courses to improve knowledge in ${role.requiredSkills[1]}`,
          `Practice real-world projects to gain hands-on experience`,
          `Review ${role.requiredSkills[2] || role.requiredSkills[0]} concepts and best practices`,
          `Engage with the developer community and participate in code reviews`
        ],
        nextSteps: [
          `Complete an online course in ${role.requiredSkills[0]}`,
          `Build 2-3 portfolio projects demonstrating ${role.requiredSkills[1]} skills`,
          `Contribute to open-source projects related to this role`,
          `Schedule mentoring sessions with experienced ${role.title}s`,
          `Retake this assessment in 3 months to track progress`
        ]
      }
    };
  };

  const handleSubmitAnswers = async () => {
    setIsLoading(true);

    try {
      // Exit fullscreen if active
      if (document.fullscreenElement) {
        try { await document.exitFullscreen(); } catch (e) { }
      }

      // Turn off cameras
      setProctorMode(false);
      setCameraEnabled(false);

      const role = jobRoles.find(r => r.id === selectedRole);

      try {
        // Try backend API first
        // Map answers to the format backend expects: selectedOption instead of selectedOptionIndex
        const mappedAnswers = answers.map(a => ({
          questionId: a.questionId,
          selectedOption: a.selectedOptionIndex
        }));

        const response = await axios.post(ENDPOINTS.ANALYZE_ROLE_RESULTS, {
          roleId: selectedRole,
          roleTitle: role.title,
          questions: questions,
          answers: mappedAnswers
        }, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 5000
        });

        if (response.data.success) {
          setAnalysisResults(response.data.analysis);
          setShowResults(true);
        } else {
          throw new Error('Backend analysis failed');
        }
      } catch (backendErr) {
        // Fallback to local analysis if backend unavailable
        console.warn('Backend analysis unavailable, using local fallback', backendErr);
        const fallbackData = generateFallbackAnalysis();
        setAnalysisResults(fallbackData.analysis);
        setShowResults(true);
      }
    } catch (err) {
      console.error('Error analyzing results:', err);
      // Final fallback: generate local analysis
      const fallbackData = generateFallbackAnalysis();
      setAnalysisResults(fallbackData.analysis);
      setShowResults(true);
    } finally {
      setIsLoading(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedRole('');
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setShowResults(false);
    setAnalysisResults(null);
    setTerminationReason(null);
    setIsLoading(false);
    setProctorMode(false);
    setCameraEnabled(false);
    setError(null);
    // stop and release camera stream if present
    if (streamRef.current) {
      try {
        streamRef.current.getTracks().forEach(t => t.stop());
      } catch (e) { }
      streamRef.current = null;
    }
  };

  const getCurrentAnswer = () => {
    if (currentQuestionIndex === 0 || questions.length === 0) return undefined;
    const currentQuestion = questions[currentQuestionIndex - 1];
    const answer = answers.find(a => a.questionId === currentQuestion?.id);
    return answer?.selectedOptionIndex;
  };

  const getProgressPercentage = () => {
    return Math.round((currentQuestionIndex / questions.length) * 100);
  };

  return (
    <div className="skill-analysis-container">
      {!selectedRole && !showResults && (
        <div className="role-selection">
          <div className="skill-analysis-header">
            <h1>Select Your Target Role</h1>
            <p>Choose a role to get skill assessment questions tailored for that position</p>
          </div>
          <div className="roles-grid">
            {jobRoles.map((role) => (
              <div
                key={role.id}
                className="role-card enhanced-card"
                onClick={() => {
                  setSelectedRole(role.id);
                  handleStartAssessment(role.id);
                }}
              >
                <div className="role-icon">{role.icon}</div>
                <h3>{role.title}</h3>
                <p>{role.description}</p>
                <div className="required-skills">
                  {role.requiredSkills.slice(0, 3).map((skill, idx) => (
                    <span key={idx} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {selectedRole && isLoading && questions.length === 0 && (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <h2>Initializing Proctored Assessment...</h2>
              <p>Generating 10 AI-powered questions for {jobRoles.find(r => r.id === selectedRole)?.title}</p>
              <div className="loading-steps">
                <div className="loading-step active">
                  <span>📹 Activating AI Proctoring</span>
                </div>
                <div className="loading-step">
                  <span>❓ Generating Questions</span>
                </div>
                <div className="loading-step">
                  <span>✓ Ready for Assessment</span>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="error-container">
              <div className="error-content">
                <FaTimesCircle className="error-icon" />
                <h3>Assessment Error</h3>
                <p>{error}</p>
                <button
                  className="error-retry-btn"
                  onClick={() => {
                    setError(null);
                    setSelectedRole('');
                  }}
                >
                  Try Another Role
                </button>
              </div>
            </div>
          )}
        </div>
      )}


      {selectedRole && !showResults && questions.length > 0 && currentQuestionIndex > 0 && (
        <div className="assessment-arena split-layout">
          {/* Left Column: Question Container */}
          <div className="question-column">
            <div className="question-container enhanced-card">
              <div className="question-header">
                <div className="header-info">
                  <h2><FaQuestion /> Assessment</h2>
                  <span className="role-badge">{jobRoles.find(r => r.id === selectedRole)?.title}</span>
                </div>
                <div className="progress-container">
                  <div className="progress-info">
                    <span>Question {currentQuestionIndex} of {questions.length}</span>
                    <span>{getProgressPercentage()}% Completed</span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${getProgressPercentage()}%` }}></div>
                  </div>
                </div>
              </div>

              <div className="question-content">
                <h3 className="question-text">{questions[currentQuestionIndex - 1].question}</h3>
                <div className="options-list">
                  {questions[currentQuestionIndex - 1].options.map((option, index) => (
                    <div
                      key={index}
                      className={`option-item ${getCurrentAnswer() === index ? 'selected' : ''}`}
                      onClick={() => handleAnswerSelect(questions[currentQuestionIndex - 1].id, index)}
                    >
                      <div className="option-marker">
                        {getCurrentAnswer() === index ? <div className="marker-dot"></div> : <span className="marker-letter">{String.fromCharCode(65 + index)}</span>}
                      </div>
                      <span className="option-text">{option}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="question-navigation">
                <button
                  className="nav-btn secondary"
                  onClick={handlePreviousQuestion}
                  disabled={currentQuestionIndex === 1}
                >
                  Previous
                </button>
                <button
                  className="nav-btn primary"
                  onClick={handleNextQuestion}
                  disabled={getCurrentAnswer() === undefined}
                >
                  {currentQuestionIndex === questions.length ? 'Submit Analysis' : 'Next Question'}
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: AI Proctor Monitor & Info */}
          <div className="proctor-column">
            {proctorMode && (
              <div className="proctor-card enhanced-card">
                <div className="card-header">
                  <h3><FaShieldAlt /> AI Proctoring Active</h3>
                  <div className="live-indicator">
                    <span className="blink-dot"></span> Live
                  </div>
                </div>

                <div className="camera-feed-container">
                  <div className="proctor-media-wrapper" ref={videoRef}>
                    <CameraMonitor
                      isActive={proctorMode}
                      onViolation={(reason) => handleAssessmentTermination(reason)}
                    />
                    <div className="camera-overlay">
                      <FaExpand className="expand-icon" onClick={toggleFullscreen} />
                    </div>
                  </div>
                  <p className="camera-status-text">
                    {cameraEnabled ? "Camera is monitoring your environment." : "Camera access required for proctoring."}
                  </p>
                </div>

                <div className="proctor-rules">
                  <h4>Assessment Rules</h4>
                  <ul>
                    <li><FaExclamationTriangle className="rule-icon" /> No tab switching allowed</li>
                    <li><FaExclamationTriangle className="rule-icon" /> Face must be visible at all times</li>
                    <li><FaExclamationTriangle className="rule-icon" /> No multiple faces detected</li>
                  </ul>
                </div>
              </div>
            )}

            <div className="info-card enhanced-card">
              <h3>Assessment Session</h3>
              <div className="session-info">
                <p><strong>Role:</strong> {jobRoles.find(r => r.id === selectedRole)?.title}</p>
                <p><strong>Status:</strong> In Progress</p>
                <p>Time Remaining: <span>45:00</span></p> {/* Mock timer */}
              </div>
            </div>
          </div>
        </div>
      )}

      {showResults && (
        <div className="analysis-results">
          {terminationReason ? (
            <div className="violation-alert enhanced-card">
              <div className="violation-header">
                <FaExclamationTriangle className="violation-icon" />
                <h2>Assessment Terminated</h2>
              </div>
              <div className="violation-content">
                <p>An AI proctoring violation was detected:</p>
                <div className="reason-box">
                  <strong>{terminationReason.replace(/_/g, ' ')}</strong>
                </div>
                <p className="violation-warning">
                  Your assessment has been stopped to maintain academic integrity.
                  Multiple violations of the assessment rules (tab switching, face visibility, etc.)
                  result in immediate termination.
                </p>
              </div>
              <div className="results-actions">
                <button className="action-btn primary" onClick={resetAnalysis}>
                  Try Again
                </button>
                <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
                  Return to Dashboard
                </button>
              </div>
            </div>
          ) : analysisResults && (
            <>
              <div className="results-header">
                <h2>Skill Analysis Results</h2>
                <p>Analysis for <strong>{jobRoles.find(r => r.id === selectedRole)?.title}</strong></p>
              </div>

              <div className="overall-score">
                <div className="score-circle" style={{ '--p': `${analysisResults.overallScore}%` }}>
                  <span className="score-percentage">{analysisResults.overallScore}%</span>
                  <span className="score-label">Overall Match</span>
                </div>
                <div className="readiness-indicator">
                  <span className={`readiness-badge ${analysisResults.readiness.toLowerCase()}`}>
                    {analysisResults.readiness} Readiness
                  </span>
                </div>
              </div>

              <div className="skill-breakdown">
                <h3>Skill Breakdown</h3>
                <div className="skills-list">
                  {analysisResults.skillScores.map((skill, index) => (
                    <div key={index} className="skill-item">
                      <div className="skill-info">
                        <span className="skill-name">{skill.skill}</span>
                        <span className="skill-level">{skill.level}</span>
                        <span className="skill-ratio">{skill.correct}/{skill.total}</span>
                      </div>
                      <div className="skill-progress">
                        <div
                          className="progress-fill"
                          style={{ width: `${skill.score}%` }}
                        ></div>
                        <span className="skill-score">{skill.score}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="recommendations">
                <h3>Recommendations</h3>
                <div className="recommendation-list">
                  {analysisResults.recommendations.map((rec, index) => (
                    <div key={index} className="recommendation-item">
                      <span className="rec-number">{index + 1}</span>
                      <p>{rec}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="next-steps">
                <h3>Next Steps</h3>
                <div className="steps-list">
                  {analysisResults.nextSteps.map((step, index) => (
                    <div key={index} className="step-item">
                      <span className="step-number">{index + 1}</span>
                      <p>{step}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="results-actions">
                <button className="action-btn primary" onClick={resetAnalysis}>
                  Analyze Another Role
                </button>
                <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
                  Back to Dashboard
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {isLoading && !selectedRole && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Generating role-specific questions...</p>
        </div>
      )}
    </div>
  );
};

export default SkillAnalysis;