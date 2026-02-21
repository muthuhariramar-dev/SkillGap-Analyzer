// src/pages/Preparation.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaArrowLeft, FaBook, FaBrain, FaChartLine, FaClock, FaCheckCircle, FaLightbulb, FaRocket, FaShieldAlt } from 'react-icons/fa';
import AssessmentEngine from '../components/SkillEvaluation/AssessmentEngine';
import '../styles/PlacementsPage.css';

const Preparation = () => {
  const [activeTab, setActiveTab] = useState('technical');
  const [aiContent, setAiContent] = useState({});
  const [loading, setLoading] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [showAssessment, setShowAssessment] = useState(false);

  const technicalTopics = [
    'Data Structures & Algorithms',
    'Web Development',
    'Machine Learning',
    'Database Management',
    'Cloud Computing',
    'Cybersecurity',
    'Mobile Development',
    'DevOps'
  ];

  const aptitudeTopics = [
    'Quantitative Aptitude',
    'Logical Reasoning',
    'Verbal Ability',
    'Data Interpretation',
    'Problem Solving',
    'Critical Thinking',
    'Pattern Recognition',
    'Mathematical Skills'
  ];

  const mockInterviewCategories = [
    'Technical Interview',
    'HR Interview',
    'Behavioral Questions',
    'Case Study Interview',
    'System Design',
    'Problem Solving',
    'Cultural Fit',
    'Salary Negotiation'
  ];

  const resumeTopics = [
    'Resume Writing Tips',
    'Cover Letter Writing',
    'LinkedIn Profile Optimization',
    'Portfolio Building',
    'Personal Branding',
    'Achievement Highlighting',
    'Skills Section',
    'Experience Description'
  ];

  const communicationTopics = [
    'Public Speaking',
    'Verbal Communication',
    'Written Communication',
    'Body Language',
    'Active Listening',
    'Presentation Skills',
    'Interpersonal Skills',
    'Negotiation Skills'
  ];

  const problemSolvingTopics = [
    'Root Cause Analysis',
    'Creative Thinking',
    'Decision Making',
    'Troubleshooting',
    'Risk Management',
    'Strategic Planning',
    'Information Processing',
    'Innovation Skills'
  ];

  const logicalThinkingTopics = [
    'Deductive Reasoning',
    'Inductive Reasoning',
    'Syllogisms',
    'Data Logic',
    'Critical Analysis',
    'Pattern Recognition',
    'Cognitive Flexibility',
    'Analytical Reasoning'
  ];

  const behavioralHRTopics = [
    'Self Awareness',
    'Emotional Intelligence',
    'Conflict Resolution',
    'Adaptability',
    'Leadership Qualities',
    'Teamwork & Collaboration',
    'Work Ethics',
    'Stress Management'
  ];

  const timeManagementTopics = [
    'Prioritization',
    'Goal Setting',
    'Scheduling',
    'Task Delegation',
    'Focus & Concentration',
    'Deadlines & Milestones',
    'Efficiency Optimization',
    'Work-Life Balance'
  ];

  const generateAIContent = async (topic, category) => {
    setLoading(true);
    setSelectedTopic(topic);

    // Simulate AI content generation with realistic data
    setTimeout(() => {
      const contentMap = {
        'Data Structures & Algorithms': {
          title: 'Data Structures & Algorithms Mastery',
          description: 'Master the fundamental concepts of data structures and algorithms for technical interviews',
          content: [
            {
              type: 'concept',
              title: 'Time Complexity Analysis',
              details: 'Understanding Big O notation is crucial for optimizing code performance. Learn to analyze algorithms based on time and space complexity.',
              examples: ['O(1) - Constant Time', 'O(log n) - Logarithmic Time', 'O(n) - Linear Time', 'O(n log n) - Linearithmic Time', 'O(n²) - Quadratic Time']
            },
            {
              type: 'practice',
              title: 'Common Problem Patterns',
              details: 'Recognize patterns in coding problems to solve them efficiently',
              examples: ['Two Pointer Technique', 'Sliding Window', 'Binary Search', 'Depth-First Search', 'Breadth-First Search', 'Dynamic Programming']
            },
            {
              type: 'implementation',
              title: 'Implementation Best Practices',
              details: 'Write clean, efficient, and bug-free code during interviews',
              examples: ['Edge Case Handling', 'Input Validation', 'Error Handling', 'Code Documentation', 'Testing Approach']
            }
          ],
          tips: [
            'Practice coding problems daily on platforms like LeetCode and HackerRank',
            'Focus on understanding the problem before jumping to solution',
            'Explain your thought process clearly during the interview',
            'Start with a brute force solution and then optimize'
          ]
        },
        'Quantitative Aptitude': {
          title: 'Quantitative Aptitude Excellence',
          description: 'Develop strong mathematical skills for placement tests and competitive exams',
          content: [
            {
              type: 'concept',
              title: 'Number Systems',
              details: 'Master concepts of integers, fractions, decimals, and number properties',
              examples: ['Prime Numbers', 'LCM & HCF', 'Factorials', 'Number Series', 'Divisibility Rules']
            },
            {
              type: 'formula',
              title: 'Essential Formulas',
              details: 'Key mathematical formulas for quick problem solving',
              examples: ['Percentage Calculations', 'Profit and Loss', 'Simple and Compound Interest', 'Ratio and Proportion', 'Time and Work']
            },
            {
              type: 'technique',
              title: 'Problem-Solving Techniques',
              details: 'Strategic approaches to tackle quantitative problems',
              examples: ['Back Calculation', 'Option Elimination', 'Approximation Methods', 'Unitary Method', 'Allegation Method']
            }
          ],
          tips: [
            'Memorize important formulas and shortcuts',
            'Practice mental calculations to improve speed',
            'Understand the logic behind each formula',
            'Solve previous year question papers'
          ]
        },
        'Technical Interview': {
          title: 'Technical Interview Preparation',
          description: 'Excel in technical interviews with comprehensive preparation strategies',
          content: [
            {
              type: 'preparation',
              title: 'Before the Interview',
              details: 'Essential preparation steps for technical interviews',
              examples: ['Research the Company', 'Review Job Description', 'Prepare STAR Examples', 'Practice Coding Problems', 'Prepare Questions to Ask']
            },
            {
              type: 'during',
              title: 'During the Interview',
              details: 'How to perform well during the technical interview',
              examples: ['Clear Communication', 'Think Aloud', 'Ask Clarifying Questions', 'Write Clean Code', 'Explain Trade-offs']
            },
            {
              type: 'common',
              title: 'Common Questions',
              details: 'Frequently asked technical interview questions',
              examples: ['Tell me about yourself', 'Why do you want to work here?', 'What are your strengths?', 'Describe a challenging project', 'How do you handle pressure?']
            }
          ],
          tips: [
            'Practice mock interviews with friends or mentors',
            'Record yourself to improve communication skills',
            'Research the company\'s tech stack and projects',
            'Prepare examples from your past experience'
          ]
        },
        'Resume Writing Tips': {
          title: 'Professional Resume Writing',
          description: 'Create a compelling resume that stands out to recruiters',
          content: [
            {
              type: 'structure',
              title: 'Resume Structure',
              details: 'Organize your resume for maximum impact',
              examples: ['Contact Information', 'Professional Summary', 'Work Experience', 'Education', 'Skills', 'Projects', 'Achievements']
            },
            {
              type: 'content',
              title: 'Content Best Practices',
              details: 'Write effective resume content that highlights your value',
              examples: ['Action Verbs', 'Quantifiable Results', 'Keywords', 'Tailored Content', 'Concise Language']
            },
            {
              type: 'formatting',
              title: 'Professional Formatting',
              details: 'Ensure your resume looks professional and is easy to read',
              examples: ['Consistent Font', 'Proper Margins', 'Bullet Points', 'White Space', 'PDF Format']
            }
          ],
          tips: [
            'Keep your resume to one page if you have less than 10 years of experience',
            'Use industry-specific keywords to pass ATS systems',
            'Quantify your achievements with numbers and percentages',
            'Proofread multiple times to avoid errors'
          ]
        }
      };

      // Generate dynamic content for other topics
      const defaultContent = {
        title: topic,
        description: `Comprehensive guide to ${topic.toLowerCase()} for placement success`,
        content: [
          {
            type: 'concept',
            title: 'Fundamental Concepts',
            details: `Understanding the core concepts of ${topic.toLowerCase()} is essential for success`,
            examples: ['Core Principles', 'Best Practices', 'Common Patterns', 'Industry Standards', 'Advanced Techniques']
          },
          {
            type: 'application',
            title: 'Practical Applications',
            details: `Real-world applications of ${topic.toLowerCase()} in professional settings`,
            examples: ['Case Studies', 'Industry Examples', 'Practical Scenarios', 'Implementation Strategies', 'Problem-Solving Approaches']
          },
          {
            type: 'advanced',
            title: 'Advanced Topics',
            details: `Deep dive into advanced ${topic.toLowerCase()} concepts and techniques`,
            examples: ['Expert Level Content', 'Specialized Knowledge', 'Cutting-edge Trends', 'Research Findings', 'Future Developments']
          }
        ],
        tips: [
          `Practice ${topic.toLowerCase()} regularly to build expertise`,
          `Stay updated with the latest trends in ${topic.toLowerCase()}`,
          `Apply theoretical knowledge to practical problems`,
          `Seek feedback from industry professionals`
        ]
      };

      setAiContent(contentMap[topic] || defaultContent);
      setLoading(false);
    }, 400);
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="ai-loading">
          <div className="loading-spinner"></div>
          <h3>Generating AI Content...</h3>
          <p>Creating personalized learning material for {selectedTopic}</p>
        </div>
      );
    }

    if (!aiContent.title) {
      return (
        <div className="welcome-section">
          <div className="welcome-icon">
            <FaBrain />
          </div>
          <h3>Welcome to AI-Powered Preparation</h3>
          <div className="welcome-info">
            <div className="info-item">
              <h4>Instructions</h4>
              <p>Select a preparation area from the left menu, then choose a specific topic from the center panel to begin.</p>
            </div>
            <div className="info-item">
              <h4>Assessment Guidance</h4>
              <p>Follow the AI-generated study material before attempting the practice tests for better results.</p>
            </div>
            <div className="info-item">
              <h4>AI Suggestions</h4>
              <p>Our AI will personalize your learning path based on your selected topics and performance.</p>
            </div>
            <div className="info-item">
              <h4>Performance Hints</h4>
              <p>Focus on foundational concepts first. Use the "Pro Tips" generated for each topic.</p>
            </div>
          </div>
          <div className="quick-stats">
            <div className="stat">
              <span className="stat-number">1000+</span>
              <span className="stat-label">Topics Available</span>
            </div>
            <div className="stat">
              <span className="stat-number">24/7</span>
              <span className="stat-label">AI Support</span>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="ai-content">
        <div className="content-header">
          <h2>{aiContent.title}</h2>
          <p>{aiContent.description}</p>
          <div className="content-meta">
            <span className="ai-badge">
              <FaBrain /> AI-Generated
            </span>
            <span className="update-time">
              <FaClock /> Updated just now
            </span>
          </div>
        </div>

        <div className="content-sections">
          {aiContent.content.map((section, index) => (
            <div key={index} className="content-section">
              <h3>
                <FaLightbulb /> {section.title}
              </h3>
              <p>{section.details}</p>
              <div className="examples-grid">
                {section.examples.map((example, idx) => (
                  <div key={idx} className="example-card">
                    <FaCheckCircle className="example-icon" />
                    <span>{example}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="tips-section">
          <h3>
            <FaRocket /> Pro Tips for Success
          </h3>
          <div className="tips-list">
            {aiContent.tips.map((tip, index) => (
              <div key={index} className="tip-item">
                <FaCheckCircle className="tip-icon" />
                <span>{tip}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="action-buttons">
          <button
            className="primary-button"
            onClick={() => {
              // Trigger the unified skill assessment directly in this view
              setShowAssessment(true);
            }}
          >
            <FaChartLine /> Start Practice Test
          </button>
        </div>
      </div>
    );
  };

  const renderTopicList = (topics, category) => (
    <div className="topics-grid">
      {topics.map((topic, index) => (
        <div key={index} className="topic-card-wrapper">
          <button
            className={`topic-card ${selectedTopic === topic ? 'active' : ''}`}
            onClick={() => generateAIContent(topic, category)}
          >
            <h4>{topic}</h4>
            <p>Click to generate AI content</p>
            <FaArrowLeft className="card-arrow" />
          </button>
          <button
            className="quick-assess-btn"
            onClick={(e) => {
              e.stopPropagation();
              setSelectedTopic(topic);
              setShowAssessment(true);
            }}
          >
            <FaChartLine /> Take Assessment
          </button>
        </div>
      ))}
    </div>
  );

  if (showAssessment) {
    return (
      <AssessmentEngine
        role={selectedTopic || activeTab}
        mcqCount={20}
        codingCount={0}
        onExit={() => setShowAssessment(false)}
      />
    );
  }

  return (
    <div className="preparation-layout">
      {/* LEFT SIDE — VERTICAL MENU (PRIMARY NAVIGATION) */}
      <aside className="sidebar-nav">
        <div className="sidebar-header">
          <Link to="/placements" className="back-button">
            <FaArrowLeft /> Back
          </Link>
          <h1 className="sidebar-title">Preparation Center</h1>
        </div>
        <div className="sidebar-menu">
          <button
            className={`menu-item ${activeTab === 'technical' ? 'active' : ''}`}
            onClick={() => setActiveTab('technical')}
          >
            <FaBook /> <span>Technical Interview</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'aptitude' ? 'active' : ''}`}
            onClick={() => setActiveTab('aptitude')}
          >
            <FaChartLine /> <span>Aptitude Test</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'mock' ? 'active' : ''}`}
            onClick={() => setActiveTab('mock')}
          >
            <FaBrain /> <span>Mock Interviews</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'resume' ? 'active' : ''}`}
            onClick={() => setActiveTab('resume')}
          >
            <FaLightbulb /> <span>Resume Building</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'communication' ? 'active' : ''}`}
            onClick={() => setActiveTab('communication')}
          >
            <FaRocket /> <span>Communication Skills</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'problemSolving' ? 'active' : ''}`}
            onClick={() => setActiveTab('problemSolving')}
          >
            <FaBrain /> <span>Problem Solving</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'logicalThinking' ? 'active' : ''}`}
            onClick={() => setActiveTab('logicalThinking')}
          >
            <FaLightbulb /> <span>Logical Thinking</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'behavioral' ? 'active' : ''}`}
            onClick={() => setActiveTab('behavioral')}
          >
            <FaShieldAlt /> <span>Behavioral / HR Readiness</span>
          </button>
          <button
            className={`menu-item ${activeTab === 'timeManagement' ? 'active' : ''}`}
            onClick={() => setActiveTab('timeManagement')}
          >
            <FaClock /> <span>Time Management</span>
          </button>
        </div>
      </aside>

      {/* CENTER AREA — CONTENT DISPLAY */}
      <main className="content-display">
        <div className="topics-scroll-area">
          {activeTab === 'technical' && renderTopicList(technicalTopics, 'technical')}
          {activeTab === 'aptitude' && renderTopicList(aptitudeTopics, 'aptitude')}
          {activeTab === 'mock' && renderTopicList(mockInterviewCategories, 'mock')}
          {activeTab === 'resume' && renderTopicList(resumeTopics, 'resume')}
          {activeTab === 'communication' && renderTopicList(communicationTopics, 'communication')}
          {activeTab === 'problemSolving' && renderTopicList(problemSolvingTopics, 'problemSolving')}
          {activeTab === 'logicalThinking' && renderTopicList(logicalThinkingTopics, 'logicalThinking')}
          {activeTab === 'behavioral' && renderTopicList(behavioralHRTopics, 'behavioral')}
          {activeTab === 'timeManagement' && renderTopicList(timeManagementTopics, 'timeManagement')}
        </div>
      </main>

      {/* RIGHT SIDE — PREPARATION PANEL */}
      <section className="preparation-panel">
        <div className="panel-inner">
          {renderContent()}
        </div>
      </section>
    </div>
  );
};

export default Preparation;
