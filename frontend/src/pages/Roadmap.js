import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaMap, FaArrowLeft, FaCheckCircle, FaClock, FaPlay, FaTrophy, FaBook, FaCode, FaUsers, FaCertificate, FaWordpress, FaMobile, FaGamepad, FaDatabase, FaServer, FaShieldAlt, FaPalette } from 'react-icons/fa';
import '../styles/Roadmap.css';

const Roadmap = () => {
  const navigate = useNavigate();
  const [selectedCareer, setSelectedCareer] = useState('');
  const [roadmap, setRoadmap] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const careerPaths = [
    {
      id: 'frontend-developer',
      title: 'Frontend Developer',
      icon: <FaCode />,
      duration: '6-12 months',
      difficulty: 'Intermediate',
      description: 'Build modern web applications and user interfaces'
    },
    {
      id: 'backend-developer',
      title: 'Backend Developer',
      icon: <FaCode />,
      duration: '8-14 months',
      difficulty: 'Intermediate',
      description: 'Develop server-side applications and APIs'
    },
    {
      id: 'fullstack-developer',
      title: 'Full Stack Developer',
      icon: <FaCode />,
      duration: '12-18 months',
      difficulty: 'Advanced',
      description: 'Master both frontend and backend development'
    },
    {
      id: 'product-manager',
      title: 'Product Manager',
      icon: <FaUsers />,
      duration: '6-10 months',
      difficulty: 'Intermediate',
      description: 'Lead product strategy and development'
    },
    {
      id: 'team-lead',
      title: 'Team Lead',
      icon: <FaUsers />,
      duration: '8-12 months',
      difficulty: 'Intermediate',
      description: 'Lead development teams and projects'
    },
    {
      id: 'ui-ux-designer',
      title: 'UI/UX Designer',
      icon: <FaBook />,
      duration: '4-8 months',
      difficulty: 'Beginner',
      description: 'Create user-centered designs and experiences'
    },
    {
      id: 'data-scientist',
      title: 'Data Scientist',
      icon: <FaCertificate />,
      duration: '10-16 months',
      difficulty: 'Advanced',
      description: 'Analyze data and build machine learning models'
    },
    {
      id: 'wordpress-developer',
      title: 'WordPress Developer',
      icon: <FaWordpress />,
      duration: '4-8 months',
      difficulty: 'Beginner',
      description: 'Build and customize WordPress websites and applications'
    },
    {
      id: 'software-engineer-agile',
      title: 'Software Engineer[AGILE]',
      icon: <FaCode />,
      duration: '8-12 months',
      difficulty: 'Intermediate',
      description: 'Develop software using Agile methodologies and practices'
    },
    {
      id: 'mobile-developer',
      title: 'Mobile Developer',
      icon: <FaMobile />,
      duration: '8-14 months',
      difficulty: 'Intermediate',
      description: 'Create mobile applications for iOS and Android platforms'
    },
    {
      id: 'game-developer',
      title: 'Game Developer',
      icon: <FaGamepad />,
      duration: '12-20 months',
      difficulty: 'Advanced',
      description: 'Develop interactive games and gaming experiences'
    },
    {
      id: 'big-data-developer',
      title: 'Big Data Developer',
      icon: <FaDatabase />,
      duration: '10-16 months',
      difficulty: 'Advanced',
      description: 'Work with large-scale data processing and analytics'
    },
    {
      id: 'devops-engineer',
      title: 'Developmental Operations Engineer',
      icon: <FaServer />,
      duration: '6-10 months',
      difficulty: 'Intermediate',
      description: 'Manage deployment pipelines and infrastructure'
    },
    {
      id: 'security-developer',
      title: 'Security Developer',
      icon: <FaShieldAlt />,
      duration: '8-14 months',
      difficulty: 'Advanced',
      description: 'Develop secure applications and security systems'
    },
    {
      id: 'graphics-developer',
      title: 'Graphics Developer',
      icon: <FaPalette />,
      duration: '10-18 months',
      difficulty: 'Advanced',
      description: 'Create graphics engines and visual effects'
    }
  ];

  const generateRoadmap = (career) => {
    setSelectedCareer(career.id);
    setIsGenerating(true);
    
    setTimeout(() => {
      const mockRoadmap = generateMockRoadmap(career);
      setRoadmap(mockRoadmap);
      setIsGenerating(false);
    }, 2000);
  };

  const generateMockRoadmap = (career) => {
    const phases = getCareerPhases(career.id);
    const milestones = getCareerMilestones(career.id);
    const resources = getCareerResources(career.id);
    
    return {
      career: career.title,
      totalDuration: career.duration,
      difficulty: career.difficulty,
      phases: phases,
      milestones: milestones,
      resources: resources,
      currentPhase: 1,
      completedPhases: 0,
      totalPhases: phases.length
    };
  };

  const getCareerPhases = (careerId) => {
    const phaseTemplates = {
      'frontend-developer': [
        {
          title: 'Foundation Basics',
          duration: '2-3 months',
          description: 'Learn HTML, CSS, and JavaScript fundamentals',
          topics: ['HTML5 & Semantic Markup', 'CSS3 & Responsive Design', 'JavaScript ES6+', 'DOM Manipulation', 'Version Control with Git'],
          projects: ['Personal Portfolio', 'Landing Page', 'Interactive Calculator'],
          status: 'completed'
        },
        {
          title: 'Modern Frameworks',
          duration: '3-4 months',
          description: 'Master React.js and modern frontend tools',
          topics: ['React Components & State', 'React Hooks', 'React Router', 'State Management (Redux/Context)', 'Build Tools (Webpack/Vite)'],
          projects: ['Todo App', 'Weather Dashboard', 'E-commerce Frontend'],
          status: 'current'
        },
        {
          title: 'Advanced Concepts',
          duration: '2-3 months',
          description: 'Learn advanced frontend concepts and optimization',
          topics: ['Performance Optimization', 'Testing (Jest/React Testing)', 'TypeScript', 'Progressive Web Apps', 'Deployment & CI/CD'],
          projects: ['Full-stack Application', 'PWA Project', 'Component Library'],
          status: 'upcoming'
        },
        {
          title: 'Specialization',
          duration: '1-2 months',
          description: 'Choose a specialization and build portfolio',
          topics: ['Mobile Development (React Native)', 'WebGL/Three.js', 'Node.js Basics', 'GraphQL', 'Advanced State Patterns'],
          projects: ['Mobile App', '3D Visualization', 'Capstone Project'],
          status: 'upcoming'
        }
      ],
      'backend-developer': [
        {
          title: 'Programming Fundamentals',
          duration: '2-3 months',
          description: 'Master programming language and computer science basics',
          topics: ['Python/Node.js Fundamentals', 'Data Structures & Algorithms', 'Database Design', 'API Concepts', 'Security Basics'],
          projects: ['REST API', 'Database Schema', 'CLI Application'],
          status: 'completed'
        },
        {
          title: 'Backend Frameworks',
          duration: '3-4 months',
          description: 'Learn backend frameworks and architecture',
          topics: ['Django/Express.js', 'ORM/Database Integration', 'Authentication & Authorization', 'Middleware', 'Error Handling'],
          projects: ['Blog API', 'User Management System', 'File Upload Service'],
          status: 'current'
        },
        {
          title: 'Advanced Backend',
          duration: '2-3 months',
          description: 'Master advanced backend concepts',
          topics: ['Microservices', 'Message Queues', 'Caching Strategies', 'Load Balancing', 'Containerization (Docker)'],
          projects: ['Microservices Architecture', 'Real-time Chat', 'E-commerce Backend'],
          status: 'upcoming'
        },
        {
          title: 'DevOps & Deployment',
          duration: '1-2 months',
          description: 'Learn deployment and operations',
          topics: ['Cloud Services (AWS/Azure)', 'CI/CD Pipelines', 'Monitoring & Logging', 'Scaling Strategies', 'Infrastructure as Code'],
          projects: ['Deployed Application', 'Automated Pipeline', 'Monitoring Dashboard'],
          status: 'upcoming'
        }
      ],
      'wordpress-developer': [
        {
          title: 'WordPress Fundamentals',
          duration: '1-2 months',
          description: 'Learn WordPress basics and setup',
          topics: ['WordPress Installation', 'Dashboard Navigation', 'Posts & Pages', 'Media Management', 'Basic SEO'],
          projects: ['Personal Blog', 'Business Website', 'Portfolio Site'],
          status: 'completed'
        },
        {
          title: 'Theme Development',
          duration: '2-3 months',
          description: 'Create custom WordPress themes',
          topics: ['PHP Basics', 'WordPress Theme Hierarchy', 'Custom Templates', 'CSS/JavaScript Integration', 'Responsive Design'],
          projects: ['Custom Theme', 'Child Theme', 'Multipurpose Theme'],
          status: 'current'
        },
        {
          title: 'Plugin Development',
          duration: '2-3 months',
          description: 'Develop WordPress plugins',
          topics: ['Plugin Architecture', 'Hooks & Filters', 'Custom Post Types', 'Shortcodes', 'Database Integration'],
          projects: ['Contact Form Plugin', 'Gallery Plugin', 'SEO Plugin'],
          status: 'upcoming'
        },
        {
          title: 'Advanced WordPress',
          duration: '1-2 months',
          description: 'Master advanced WordPress concepts',
          topics: ['WooCommerce Development', 'Multisite Setup', 'Performance Optimization', 'Security Hardening', 'REST API Integration'],
          projects: ['E-commerce Site', 'Multisite Network', 'Performance-Optimized Site'],
          status: 'upcoming'
        }
      ],
      'team-lead': [
        {
          title: 'Leadership Fundamentals',
          duration: '2-3 months',
          description: 'Learn basic leadership and management skills',
          topics: ['Leadership Principles', 'Team Communication', 'Project Management Basics', 'Time Management', 'Conflict Resolution'],
          projects: ['Team Meeting Facilitation', 'Small Project Leadership', 'Communication Plan', 'Process Improvement'],
          status: 'completed'
        },
        {
          title: 'Technical Leadership',
          duration: '3-4 months',
          description: 'Develop technical leadership and mentoring skills',
          topics: ['Code Review Best Practices', 'Technical Decision Making', 'Mentoring Junior Developers', 'Architecture Planning', 'Quality Assurance'],
          projects: ['Code Review Process', 'Mentoring Program', 'Technical Documentation', 'Quality Standards'],
          status: 'current'
        },
        {
          title: 'Advanced Team Management',
          duration: '2-3 months',
          description: 'Master advanced team and project management',
          topics: ['Agile/Scrum Mastery', 'Team Building', 'Performance Management', 'Resource Planning', 'Stakeholder Management'],
          projects: ['Team Building Workshop', 'Performance Review System', 'Resource Allocation Plan', 'Stakeholder Communication'],
          status: 'upcoming'
        },
        {
          title: 'Strategic Leadership',
          duration: '1-2 months',
          description: 'Develop strategic thinking and organizational leadership',
          topics: ['Strategic Planning', 'Organizational Culture', 'Change Management', 'Business Acumen', 'Executive Communication'],
          projects: ['Strategic Plan', 'Change Initiative', 'Leadership Development Program', 'Business Case Study'],
          status: 'upcoming'
        }
      ],
      'software-engineer-agile': [
        {
          title: 'Software Development Basics',
          duration: '2-3 months',
          description: 'Learn fundamental software development skills',
          topics: ['Programming Fundamentals', 'Version Control', 'Testing Basics', 'Code Quality', 'Documentation'],
          projects: ['CLI Tool', 'Unit Tested Library', 'Code Documentation'],
          status: 'completed'
        },
        {
          title: 'Agile Methodologies',
          duration: '2-3 months',
          description: 'Master Agile principles and practices',
          topics: ['Scrum Framework', 'Agile Ceremonies', 'User Stories', 'Sprint Planning', 'Retrospectives'],
          projects: ['Sprint Simulation', 'Agile Board Setup', 'Process Documentation'],
          status: 'current'
        },
        {
          title: 'Advanced Agile Practices',
          duration: '2-3 months',
          description: 'Learn advanced Agile and DevOps practices',
          topics: ['Continuous Integration', 'Test-Driven Development', 'Pair Programming', 'Code Reviews', 'Metrics & Reporting'],
          projects: ['CI Pipeline', 'TDD Project', 'Code Review Process'],
          status: 'upcoming'
        },
        {
          title: 'Agile Leadership',
          duration: '1-2 months',
          description: 'Develop Agile leadership skills',
          topics: ['Team Facilitation', 'Coaching', 'Scaling Agile', 'Organizational Change', 'Agile Transformation'],
          projects: ['Team Coaching', 'Process Improvement', 'Agile Transformation Plan'],
          status: 'upcoming'
        }
      ],
      'mobile-developer': [
        {
          title: 'Mobile Development Basics',
          duration: '2-3 months',
          description: 'Learn mobile development fundamentals',
          topics: ['Mobile UI/UX Principles', 'React Native Basics', 'Flutter Basics', 'Platform Guidelines', 'Mobile Testing'],
          projects: ['Simple Calculator App', 'Weather App', 'Todo Mobile App'],
          status: 'completed'
        },
        {
          title: 'Advanced Mobile Development',
          duration: '3-4 months',
          description: 'Master advanced mobile concepts',
          topics: ['State Management', 'Navigation', 'API Integration', 'Local Storage', 'Push Notifications'],
          projects: ['Social Media App', 'E-commerce App', 'News App'],
          status: 'current'
        },
        {
          title: 'Platform-Specific Features',
          duration: '2-3 months',
          description: 'Learn platform-specific features',
          topics: ['Native Modules', 'Camera Integration', 'GPS & Maps', 'Device APIs', 'Performance Optimization'],
          projects: ['Camera App', 'Location-Based App', 'Performance-Optimized App'],
          status: 'upcoming'
        },
        {
          title: 'Mobile Deployment & Marketing',
          duration: '1-2 months',
          description: 'Deploy and market mobile applications',
          topics: ['App Store Submission', 'Play Store Submission', 'App Marketing', 'Analytics', 'Monetization'],
          projects: ['Published App', 'App Marketing Strategy', 'Analytics Dashboard'],
          status: 'upcoming'
        }
      ],
      'game-developer': [
        {
          title: 'Game Development Basics',
          duration: '2-3 months',
          description: 'Learn game development fundamentals',
          topics: ['Unity Basics', 'Unreal Engine Basics', 'Game Design Principles', '2D Graphics', 'Game Physics'],
          projects: ['Simple 2D Game', 'Platformer', 'Puzzle Game'],
          status: 'completed'
        },
        {
          title: 'Advanced Game Development',
          duration: '4-6 months',
          description: 'Master advanced game development',
          topics: ['3D Modeling', 'Animation', 'Shader Programming', 'AI Programming', 'Multiplayer Networking'],
          projects: ['3D Adventure Game', 'RPG Game', 'Multiplayer Game'],
          status: 'current'
        },
        {
          title: 'Game Specialization',
          duration: '3-4 months',
          description: 'Specialize in specific game types',
          topics: ['Mobile Games', 'VR/AR Development', 'Game Optimization', 'Game Audio', 'Game Marketing'],
          projects: ['Mobile Game', 'VR Experience', 'Optimized Game Engine'],
          status: 'upcoming'
        },
        {
          title: 'Game Industry & Publishing',
          duration: '2-3 months',
          description: 'Learn game business and publishing',
          topics: ['Game Publishing', 'Steam Publishing', 'Mobile Game Stores', 'Game Marketing', 'Community Management'],
          projects: ['Published Game', 'Game Marketing Campaign', 'Community Platform'],
          status: 'upcoming'
        }
      ],
      'big-data-developer': [
        {
          title: 'Big Data Fundamentals',
          duration: '2-3 months',
          description: 'Learn big data concepts and tools',
          topics: ['Hadoop Ecosystem', 'Spark Basics', 'Data Processing', 'Distributed Computing', 'Cloud Data Services'],
          projects: ['Data Processing Pipeline', 'ETL Job', 'Data Analysis Dashboard'],
          status: 'completed'
        },
        {
          title: 'Advanced Big Data Technologies',
          duration: '4-5 months',
          description: 'Master advanced big data technologies',
          topics: ['Spark Advanced', 'Kafka', 'NoSQL Databases', 'Data Warehousing', 'Real-time Processing'],
          projects: ['Real-time Analytics', 'Data Lake', 'Streaming Pipeline'],
          status: 'current'
        },
        {
          title: 'Data Engineering',
          duration: '2-3 months',
          description: 'Learn data engineering practices',
          topics: ['Data Pipeline Architecture', 'Data Quality', 'Data Governance', 'ML Pipelines', 'Data Security'],
          projects: ['Production Data Pipeline', 'ML Pipeline', 'Data Quality Framework'],
          status: 'upcoming'
        },
        {
          title: 'Big Data Specialization',
          duration: '2-3 months',
          description: 'Specialize in big data areas',
          topics: ['Cloud Big Data', 'IoT Data Processing', 'Graph Databases', 'Data Visualization', 'Big Data Architecture'],
          projects: ['Cloud Data Platform', 'IoT Data System', 'Data Visualization Platform'],
          status: 'upcoming'
        }
      ],
      'devops-engineer': [
        {
          title: 'DevOps Fundamentals',
          duration: '2-3 months',
          description: 'Learn DevOps principles and tools',
          topics: ['Linux/Unix Basics', 'Scripting', 'Version Control', 'CI/CD Concepts', 'Monitoring Basics'],
          projects: ['Automated Script', 'Basic CI Pipeline', 'Monitoring Setup'],
          status: 'completed'
        },
        {
          title: 'Containerization & Orchestration',
          duration: '3-4 months',
          description: 'Master containers and orchestration',
          topics: ['Docker', 'Kubernetes', 'Container Security', 'Service Mesh', 'Container Networking'],
          projects: ['Containerized Application', 'Kubernetes Cluster', 'Microservices Deployment'],
          status: 'current'
        },
        {
          title: 'Cloud & Infrastructure',
          duration: '2-3 months',
          description: 'Learn cloud platforms and infrastructure',
          topics: ['AWS/Azure/GCP', 'Infrastructure as Code', 'Cloud Security', 'Serverless', 'Cost Optimization'],
          projects: ['Cloud Infrastructure', 'Terraform Scripts', 'Serverless Application'],
          status: 'upcoming'
        },
        {
          title: 'Advanced DevOps',
          duration: '2-3 months',
          description: 'Master advanced DevOps practices',
          topics: ['GitOps', 'DevSecOps', 'Observability', 'Chaos Engineering', 'DevOps Culture'],
          projects: ['GitOps Pipeline', 'Security Integration', 'Observability Stack'],
          status: 'upcoming'
        }
      ],
      'data-scientist': [
        {
          title: 'Data Science Fundamentals',
          duration: '3-4 months',
          description: 'Learn data science basics',
          topics: ['Python/R Programming', 'Statistics', 'Data Cleaning', 'Exploratory Data Analysis', 'Data Visualization'],
          projects: ['Data Analysis Project', 'Statistical Analysis', 'Visualization Dashboard'],
          status: 'completed'
        },
        {
          title: 'Machine Learning',
          duration: '4-5 months',
          description: 'Master machine learning algorithms',
          topics: ['Supervised Learning', 'Unsupervised Learning', 'Feature Engineering', 'Model Evaluation', 'ML Pipelines'],
          projects: ['Classification Model', 'Regression Model', 'Clustering Analysis'],
          status: 'current'
        },
        {
          title: 'Advanced ML & Deep Learning',
          duration: '3-4 months',
          description: 'Learn advanced ML and deep learning',
          topics: ['Deep Learning', 'Neural Networks', 'NLP', 'Computer Vision', 'Reinforcement Learning'],
          projects: ['Neural Network Model', 'NLP Application', 'Computer Vision Project'],
          status: 'upcoming'
        },
        {
          title: 'Data Science Specialization',
          duration: '2-3 months',
          description: 'Specialize in data science areas',
          topics: ['Big Data ML', 'MLOps', 'AI Ethics', 'Production ML', 'Data Science Communication'],
          projects: ['Production ML Model', 'MLOps Pipeline', 'Research Paper'],
          status: 'upcoming'
        }
      ],
      'security-developer': [
        {
          title: 'Security Fundamentals',
          duration: '2-3 months',
          description: 'Learn cybersecurity basics',
          topics: ['Network Security', 'Cryptography', 'Security Principles', 'Risk Assessment', 'Security Tools'],
          projects: ['Security Audit', 'Encryption Tool', 'Vulnerability Scanner'],
          status: 'completed'
        },
        {
          title: 'Application Security',
          duration: '3-4 months',
          description: 'Master secure application development',
          topics: ['Secure Coding', 'OWASP Top 10', 'Penetration Testing', 'Security Testing', 'Code Review'],
          projects: ['Secure Application', 'Penetration Test', 'Security Framework'],
          status: 'current'
        },
        {
          title: 'Advanced Security',
          duration: '3-4 months',
          description: 'Learn advanced security concepts',
          topics: ['Advanced Cryptography', 'Security Architecture', 'Incident Response', 'Forensics', 'Compliance'],
          projects: ['Security Architecture', 'Incident Response Plan', 'Compliance Framework'],
          status: 'upcoming'
        },
        {
          title: 'Security Specialization',
          duration: '2-3 months',
          description: 'Specialize in security areas',
          topics: ['Cloud Security', 'IoT Security', 'AI Security', 'Security Research', 'Security Leadership'],
          projects: ['Cloud Security Solution', 'Security Research', 'Security Program'],
          status: 'upcoming'
        }
      ],
      'graphics-developer': [
        {
          title: 'Graphics Programming Basics',
          duration: '3-4 months',
          description: 'Learn graphics programming fundamentals',
          topics: ['OpenGL Basics', 'WebGL', 'Graphics Mathematics', 'Shaders', 'Rendering Pipeline'],
          projects: ['3D Scene', 'Shader Effects', 'Graphics Engine'],
          status: 'completed'
        },
        {
          title: 'Advanced Graphics',
          duration: '4-5 months',
          description: 'Master advanced graphics programming',
          topics: ['Advanced Shaders', 'Physics Simulation', 'Animation Systems', 'Optimization', 'GPU Computing'],
          projects: ['Physics Engine', 'Animation System', 'Optimized Renderer'],
          status: 'current'
        },
        {
          title: 'Graphics Specialization',
          duration: '3-4 months',
          description: 'Specialize in graphics areas',
          topics: ['Game Graphics', 'VR/AR Graphics', 'Visualization', 'Real-time Rendering', 'Graphics Tools'],
          projects: ['Game Graphics Engine', 'VR Experience', 'Visualization Tool'],
          status: 'upcoming'
        },
        {
          title: 'Graphics Industry Applications',
          duration: '2-3 months',
          description: 'Apply graphics skills to industries',
          topics: ['Game Industry', 'Film/VFX', 'Scientific Visualization', 'CAD/CAM', 'Graphics Research'],
          projects: ['Industry Project', 'Research Paper', 'Graphics Tool'],
          status: 'upcoming'
        }
      ]
    };

    return phaseTemplates[careerId] || phaseTemplates['frontend-developer'];
  };

  const getCareerMilestones = (careerId) => {
    return [
      {
        title: 'First Portfolio Project',
        description: 'Complete your first standalone project',
        icon: <FaTrophy />,
        achieved: true,
        date: 'Month 2'
      },
      {
        title: 'Internship Ready',
        description: 'Skills sufficient for junior internship',
        icon: <FaCheckCircle />,
        achieved: false,
        date: 'Month 4'
      },
      {
        title: 'First Job Ready',
        description: 'Complete skillset for entry-level position',
        icon: <FaCertificate />,
        achieved: false,
        date: 'Month 6'
      },
      {
        title: 'Mid-level Developer',
        description: 'Reach mid-level competency',
        icon: <FaTrophy />,
        achieved: false,
        date: 'Month 12'
      }
    ];
  };

  const getCareerResources = (careerId) => {
    return [
      {
        type: 'courses',
        title: 'Recommended Courses',
        items: [
          { name: 'Modern JavaScript Tutorial', provider: 'MDN', duration: '40 hours' },
          { name: 'React - The Complete Guide', provider: 'Udemy', duration: '48 hours' },
          { name: 'Full Stack Open', provider: 'University of Helsinki', duration: '60 hours' }
        ]
      },
      {
        type: 'books',
        title: 'Essential Books',
        items: [
          { name: 'Clean Code', author: 'Robert C. Martin', pages: 464 },
          { name: 'You Don\'t Know JS', author: 'Kyle Simpson', pages: 272 },
          { name: 'Design Patterns', author: 'Gang of Four', pages: 395 }
        ]
      },
      {
        type: 'practice',
        title: 'Practice Platforms',
        items: [
          { name: 'LeetCode', focus: 'Algorithm Practice', difficulty: 'Medium-Hard' },
          { name: 'HackerRank', focus: 'Coding Challenges', difficulty: 'Easy-Medium' },
          { name: 'CodeWars', focus: 'Problem Solving', difficulty: 'All Levels' }
        ]
      }
    ];
  };

  const resetRoadmap = () => {
    setSelectedCareer('');
    setRoadmap(null);
    setIsGenerating(false);
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'completed': return <FaCheckCircle className="status-completed" />;
      case 'current': return <FaPlay className="status-current" />;
      case 'upcoming': return <FaClock className="status-upcoming" />;
      default: return null;
    }
  };

  return (
    <div className="roadmap-container">
      <div className="roadmap-header">
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1><FaMap /> Personalized Learning Roadmap</h1>
        <p>Get a structured learning path tailored to your career goals</p>
      </div>

      {!roadmap ? (
        <div className="career-selection">
          <div className="selection-intro">
            <h2>Choose Your Career Path</h2>
            <p>Select a career path to generate a personalized learning roadmap with phases, milestones, and resources</p>
          </div>

          <div className="careers-grid">
            {careerPaths.map((career) => (
              <div
                key={career.id}
                className={`career-card ${selectedCareer === career.id ? 'selected' : ''}`}
                onClick={() => generateRoadmap(career)}
              >
                <div className="career-icon">{career.icon}</div>
                <h3>{career.title}</h3>
                <p>{career.description}</p>
                <div className="career-meta">
                  <span className="duration">{career.duration}</span>
                  <span className="difficulty">{career.difficulty}</span>
                </div>
                <button className="select-btn">
                  {isGenerating && selectedCareer === career.id ? 'Generating...' : 'Generate Roadmap'}
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="roadmap-display">
          <div className="roadmap-overview">
            <div className="overview-header">
              <h2>{roadmap.career} Learning Roadmap</h2>
              <div className="overview-stats">
                <div className="stat-item">
                  <span className="stat-label">Total Duration</span>
                  <span className="stat-value">{roadmap.totalDuration}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Difficulty</span>
                  <span className="stat-value">{roadmap.difficulty}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Phases</span>
                  <span className="stat-value">{roadmap.completedPhases}/{roadmap.totalPhases}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="roadmap-phases">
            <h3>Learning Phases</h3>
            <div className="phases-timeline">
              {roadmap.phases.map((phase, index) => (
                <div key={index} className={`phase-card ${phase.status}`}>
                  <div className="phase-header">
                    <div className="phase-number">
                      {getStatusIcon(phase.status)}
                      <span>Phase {index + 1}</span>
                    </div>
                    <div className="phase-duration">{phase.duration}</div>
                  </div>
                  
                  <h4>{phase.title}</h4>
                  <p>{phase.description}</p>
                  
                  <div className="phase-topics">
                    <h5>Topics to Cover:</h5>
                    <div className="topics-list">
                      {phase.topics.map((topic, topicIndex) => (
                        <span key={topicIndex} className="topic-tag">{topic}</span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="phase-projects">
                    <h5>Projects:</h5>
                    <div className="projects-list">
                      {phase.projects.map((project, projectIndex) => (
                        <div key={projectIndex} className="project-item">
                          <span className="project-name">{project}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="roadmap-milestones">
            <h3>Career Milestones</h3>
            <div className="milestones-timeline">
              {roadmap.milestones.map((milestone, index) => (
                <div key={index} className={`milestone-item ${milestone.achieved ? 'achieved' : ''}`}>
                  <div className="milestone-marker">
                    <div className="milestone-icon">{milestone.icon}</div>
                    <div className="milestone-date">{milestone.date}</div>
                  </div>
                  <div className="milestone-content">
                    <h4>{milestone.title}</h4>
                    <p>{milestone.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="roadmap-resources">
            <h3>Learning Resources</h3>
            <div className="resources-grid">
              {roadmap.resources.map((resourceGroup, groupIndex) => (
                <div key={groupIndex} className="resource-group">
                  <h4>{resourceGroup.title}</h4>
                  <div className="resource-list">
                    {resourceGroup.items.map((item, itemIndex) => (
                      <div key={itemIndex} className="resource-item">
                        <div className="resource-info">
                          <span className="resource-name">{item.name}</span>
                          <span className="resource-details">
                            {item.provider && `${item.provider} • `}
                            {item.duration && `${item.duration}`}
                            {item.author && `by ${item.author}`}
                            {item.focus && `${item.focus}`}
                            {item.difficulty && ` • ${item.difficulty}`}
                            {item.pages && ` • ${item.pages} pages`}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="roadmap-actions">
            <button className="action-btn primary" onClick={resetRoadmap}>
              Generate Different Roadmap
            </button>
            <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </button>
            <button className="action-btn tertiary">
              Download Roadmap PDF
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Roadmap;
