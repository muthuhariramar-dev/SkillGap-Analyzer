import React from 'react';
import { useAuth } from '../context/AuthContext';

const AuthErrorBoundary = ({ children }) => {
  const { authError, clearAuthError } = useAuth();

  if (!authError) {
    return children;
  }

  const handleRetry = () => {
    clearAuthError();
    // Optionally redirect to login
    window.location.href = '/login';
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '10px',
        maxWidth: '400px',
        width: '100%',
        textAlign: 'center',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)'
      }}>
        <div style={{
          fontSize: '48px',
          marginBottom: '20px',
          color: '#e74c3c'
        }}>
          ⚠️
        </div>
        <h3 style={{ color: '#2c3e50', marginBottom: '15px' }}>
          Authentication Error
        </h3>
        <p style={{ color: '#7f8c8d', marginBottom: '25px', lineHeight: '1.5' }}>
          {authError}
        </p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button
            onClick={handleRetry}
            style={{
              backgroundColor: '#3498db',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Try Again
          </button>
          <button
            onClick={() => window.location.href = '/login'}
            style={{
              backgroundColor: '#2ecc71',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthErrorBoundary;
