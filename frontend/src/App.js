// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import AuthErrorBoundary from './components/AuthErrorBoundary';
import ScrollToTop from './components/ScrollToTop';
import ScrollToTopOnRouteChange from './components/ScrollToTopOnRouteChange';

// Import components
import Home from './pages/Home/Home';  // Updated import path
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Students from './pages/Students';
import Placements from './pages/Placements';
import Assessments from './pages/Assessments';
import Login from './pages/Login';
import Register from './pages/Register';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import QAEvaluation from './pages/QAEvaluation';
import SkillAnalysis from './pages/SkillAnalysis';
import PlacementRisk from './pages/PlacementRisk';
import ImprovementRoadmap from './pages/ImprovementRoadmap';
import ATSCheck from './pages/ATSCheck';
import Roadmap from './pages/Roadmap';
import Preparation from './pages/Preparation';
import CompanyAnalysis from './pages/CompanyAnalysis';
import LearningPathGeneration from './pages/LearningPathGeneration';
import CareerTrajectory from './pages/CareerTrajectory';

// Styles
import './styles/App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, user } = useAuth();

  console.log('ProtectedRoute - Auth state:', { isAuthenticated, loading, user });

  if (loading) return null; // or a loading spinner

  if (!isAuthenticated) {
    console.log('ProtectedRoute - Not authenticated, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  console.log('ProtectedRoute - Authenticated, rendering protected content');
  return children;
};

// Component to handle conditional layout
const AppLayout = ({ children }) => {
  const location = useLocation();

  // Routes that should hide navbar and footer
  const fullScreenRoutes = ['/qa-evaluation', '/skill-analysis', '/placement-risk', '/risk-assessment', '/improvement-roadmap', '/ats-check', '/roadmap'];
  const shouldHideLayout = fullScreenRoutes.includes(location.pathname);

  return (
    <div className="app">
      {!shouldHideLayout && <Navbar />}
      <main className={`main-content ${shouldHideLayout ? 'full-screen' : ''}`}>
        {children}
      </main>
      {!shouldHideLayout && <Footer />}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AuthErrorBoundary>
        <Router future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true
        }}>
          <ScrollToTopOnRouteChange>
            <AppLayout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/students"
                  element={
                    <ProtectedRoute>
                      <Students />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/placements"
                  element={
                    <ProtectedRoute>
                      <Placements />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/preparation"
                  element={
                    <ProtectedRoute>
                      <Preparation />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/companyanalysis"
                  element={
                    <ProtectedRoute>
                      <CompanyAnalysis />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/assessments"
                  element={
                    <ProtectedRoute>
                      <Assessments />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/qa-evaluation"
                  element={
                    <ProtectedRoute>
                      <QAEvaluation />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/skill-analysis"
                  element={
                    <ProtectedRoute>
                      <SkillAnalysis />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/risk-assessment"
                  element={
                    <ProtectedRoute>
                      <QAEvaluation />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/placement-risk"
                  element={
                    <ProtectedRoute>
                      <PlacementRisk />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/improvement-roadmap"
                  element={
                    <ProtectedRoute>
                      <ImprovementRoadmap />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/learning-path-generation"
                  element={
                    <ProtectedRoute>
                      <LearningPathGeneration />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/career-trajectory"
                  element={
                    <ProtectedRoute>
                      <CareerTrajectory />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/ats-check"
                  element={
                    <ProtectedRoute>
                      <ATSCheck />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/roadmap"
                  element={
                    <ProtectedRoute>
                      <Roadmap />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AppLayout>
          </ScrollToTopOnRouteChange>
        </Router>
      </AuthErrorBoundary>
      <ScrollToTop />
    </AuthProvider>
  );
}

export default App;