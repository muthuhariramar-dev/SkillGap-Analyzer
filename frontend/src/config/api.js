const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  REGISTER: `${API_BASE_URL}/api/auth/register`,
  GET_ME: `${API_BASE_URL}/api/auth/me`,
  LOGOUT: `${API_BASE_URL}/api/auth/logout`,
  VALIDATE: `${API_BASE_URL}/api/auth/validate`,

  // Resume Analysis (Python)
  PARSE_RESUME: `${API_BASE_URL}/api/resume/parse`,
  ANALYZE_DESCRIPTION: `${API_BASE_URL}/api/resume/analyze-description`,

  // Job Analysis
  SCRAPE_JOBS: `${API_BASE_URL}/api/jobs/scrape`,
  ANALYZE_SKILLS: `${API_BASE_URL}/api/jobs/analyze-skills`,

  // Curriculum Analysis
  ANALYZE_CURRICULUM: `${API_BASE_URL}/api/curriculum/analyze`,
  GET_CURRICULUM_PLAN: `${API_BASE_URL}/api/curriculum/plan`,

  // Learning Path
  GET_LEARNING_PATH: `${API_BASE_URL}/api/learning-path`,

  // ===== NEW ML MODELS ENDPOINTS =====

  // Learning Path Generation
  LEARNING_PATH_GENERATE: `${API_BASE_URL}/api/learning-path/generate`,
  LEARNING_PATH_PROGRESS: `${API_BASE_URL}/api/learning-path/progress`,

  // Competency Matrix
  COMPETENCY_ASSESS: `${API_BASE_URL}/api/competency/assess`,
  COMPETENCY_GAP_ANALYSIS: `${API_BASE_URL}/api/competency/gap-analysis`,

  // Career Trajectory
  CAREER_PREDICT: `${API_BASE_URL}/api/career/predict`,
  CAREER_NEXT_ROLES: `${API_BASE_URL}/api/career/next-roles`,

  // Skill Validation
  SKILLS_VALIDATE: `${API_BASE_URL}/api/skills/validate`,
  SKILLS_ASSESSMENT_TEST: `${API_BASE_URL}/api/skills/assessment-test`,
  SKILLS_VALIDATION_SUMMARY: `${API_BASE_URL}/api/skills/validation-summary`,

  // Market Analysis
  MARKET_SKILL_DEMAND: `${API_BASE_URL}/api/market/skill-demand`,
  MARKET_REGIONAL_INSIGHTS: `${API_BASE_URL}/api/market/regional-insights`,
  MARKET_SALARY_TRENDS: `${API_BASE_URL}/api/market/salary-trends`,
  MARKET_COMPETITION_ANALYSIS: `${API_BASE_URL}/api/market/competition-analysis`,
  MARKET_COMPREHENSIVE_REPORT: `${API_BASE_URL}/api/market/comprehensive-report`,

  // Role Analysis
  GENERATE_ROLE_QUESTIONS: `${API_BASE_URL}/api/generateRoleQuestions`,
  ANALYZE_ROLE_RESULTS: `${API_BASE_URL}/api/analyzeRoleResults`,
  QUESTIONS: `${API_BASE_URL}/api/questions`,

  // Camera Proctoring (Python)
  START_CAMERA: `${API_BASE_URL}/api/proctor/camera/start`,
  STOP_CAMERA: `${API_BASE_URL}/api/proctor/camera/stop`,
  ANALYZE_FRAME: `${API_BASE_URL}/api/proctor/camera`
};

export const apiRequest = async (endpoint, method = 'GET', data = null) => {
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(endpoint, config);
    const responseData = await response.json();

    if (!response.ok) {
      throw new Error(responseData.message || 'Something went wrong');
    }

    return responseData;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
