import { API_ENDPOINTS, apiRequest } from '../config/api';

export const resumeService = {
  parseResume: async (formData) => {
    const response = await fetch(API_ENDPOINTS.PARSE_RESUME, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  },
  analyzeDescription: (description) => 
    apiRequest(API_ENDPOINTS.ANALYZE_DESCRIPTION, 'POST', { description }),
};

export const jobService = {
  scrapeJobs: (role, location) => 
    apiRequest(API_ENDPOINTS.SCRAPE_JOBS, 'POST', { role, location }),
  
  analyzeSkills: (jobDescription, userSkills) => 
    apiRequest(API_ENDPOINTS.ANALYZE_SKILLS, 'POST', { jobDescription, userSkills }),
};

export const curriculumService = {
  analyzeCurriculum: (curriculumText) => 
    apiRequest(API_ENDPOINTS.ANALYZE_CURRICULUM, 'POST', { curriculumText }),
  
  getCurriculumPlan: (analysisResults) => 
    apiRequest(API_ENDPOINTS.GET_CURRICULUM_PLAN, 'POST', analysisResults),
};

export const learningPathService = {
  getLearningPath: (skills) => 
    apiRequest(API_ENDPOINTS.GET_LEARNING_PATH, 'POST', { skills }),
};

// ===== NEW ML MODELS SERVICES =====

// Learning Path Generation Services
export const learningPathGenerationService = {
  generateLearningPath: (requestData) => 
    apiRequest(API_ENDPOINTS.LEARNING_PATH_GENERATE, 'POST', requestData),
  
  updateProgress: (requestData) => 
    apiRequest(API_ENDPOINTS.LEARNING_PATH_PROGRESS, 'POST', requestData),
};

// Competency Matrix Services
export const competencyService = {
  assessCompetency: (requestData) => 
    apiRequest(API_ENDPOINTS.COMPETENCY_ASSESS, 'POST', requestData),
  
  analyzeSkillGaps: (requestData) => 
    apiRequest(API_ENDPOINTS.COMPETENCY_GAP_ANALYSIS, 'POST', requestData),
};

// Career Trajectory Services
export const careerTrajectoryService = {
  predictCareerTrajectory: (requestData) => 
    apiRequest(API_ENDPOINTS.CAREER_PREDICT, 'POST', requestData),
  
  predictNextRoles: (requestData) => 
    apiRequest(API_ENDPOINTS.CAREER_NEXT_ROLES, 'POST', requestData),
};

// Skill Validation Services
export const skillValidationService = {
  validateSkills: (requestData) => 
    apiRequest(API_ENDPOINTS.SKILLS_VALIDATE, 'POST', requestData),
  
  takeAssessmentTest: (requestData) => 
    apiRequest(API_ENDPOINTS.SKILLS_ASSESSMENT_TEST, 'POST', requestData),
  
  getValidationSummary: () => 
    apiRequest(API_ENDPOINTS.SKILLS_VALIDATION_SUMMARY, 'GET'),
};

// Market Analysis Services
export const marketAnalysisService = {
  analyzeSkillDemand: (requestData) => 
    apiRequest(API_ENDPOINTS.MARKET_SKILL_DEMAND, 'POST', requestData),
  
  getRegionalInsights: (requestData) => 
    apiRequest(API_ENDPOINTS.MARKET_REGIONAL_INSIGHTS, 'POST', requestData),
  
  predictSalaryTrends: (requestData) => 
    apiRequest(API_ENDPOINTS.MARKET_SALARY_TRENDS, 'POST', requestData),
  
  analyzeMarketCompetition: (requestData) => 
    apiRequest(API_ENDPOINTS.MARKET_COMPETITION_ANALYSIS, 'POST', requestData),
  
  generateComprehensiveReport: (requestData) => 
    apiRequest(API_ENDPOINTS.MARKET_COMPREHENSIVE_REPORT, 'POST', requestData),
};
