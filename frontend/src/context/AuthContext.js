import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

// Clear corrupted localStorage immediately on load
try {
  const allKeys = Object.keys(localStorage);
  allKeys.forEach(key => {
    const value = localStorage.getItem(key);
    if (value && value.startsWith('eyJ')) {
      console.log('Clearing corrupted JWT token from localStorage:', key);
      localStorage.removeItem(key);
    }
  });
} catch (error) {
  console.log('Error checking localStorage:', error);
}

export const AuthContext = createContext(null);

// Secure localStorage helpers
const secureStorage = {
  setItem: (key, value) => {
    try {
      if (typeof value === 'object') {
        // Add timestamp for session validation
        value.timestamp = Date.now();
        value = JSON.stringify(value);
      }
      localStorage.setItem(key, value);
      return true;
    } catch (error) {
      console.error('localStorage setItem error:', error);
      return false;
    }
  },

  getItem: (key) => {
    try {
      const value = localStorage.getItem(key);
      if (!value) return null;

      // Check if value looks like JSON (starts with { or [)
      if (!value.startsWith('{') && !value.startsWith('[') && !value.startsWith('"')) {
        console.warn('localStorage contains non-JSON data, clearing:', key);
        secureStorage.removeItem(key);
        return null;
      }

      // Additional check for JWT tokens that might be corrupted
      if (key === 'token' && value.length > 100 && !value.startsWith('"')) {
        console.warn('localStorage contains corrupted token data, clearing:', key);
        secureStorage.removeItem(key);
        return null;
      }

      const parsed = JSON.parse(value);

      // Check if session is expired (24 hours)
      if (parsed.timestamp && Date.now() - parsed.timestamp > 24 * 60 * 60 * 1000) {
        secureStorage.removeItem(key);
        return null;
      }

      return parsed;
    } catch (error) {
      console.error('localStorage getItem error:', error);
      console.log('Clearing all localStorage due to corruption...');
      // Clear all localStorage items on any parsing error
      secureStorage.clear();
      return null;
    }
  },

  removeItem: (key) => {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('localStorage removeItem error:', error);
      return false;
    }
  },

  clearAll: () => {
    try {
      Object.keys(localStorage).forEach(key => {
        localStorage.removeItem(key);
      });
      console.log('localStorage cleared');
      return true;
    } catch (error) {
      console.error('localStorage clearAll error:', error);
      return false;
    }
  },

  clear: () => {
    try {
      localStorage.clear();
      return true;
    } catch (error) {
      console.error('localStorage clear error:', error);
      return false;
    }
  }
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  // =========================
  // LOGOUT
  // =========================
  const logout = useCallback(() => {
    console.log('AuthContext - Logging out user');

    // Clear all auth data
    secureStorage.removeItem('token');
    secureStorage.removeItem('user');
    setUser(null);
    setAuthError(null);

    // Clear any other app data if needed
    try {
      // Optionally clear other app-specific data
      const keysToRemove = ['cachedData', 'tempFiles'];
      keysToRemove.forEach(key => secureStorage.removeItem(key));
    } catch (error) {
      console.error('AuthContext - Error clearing additional data:', error);
    }
  }, []);

  // =========================
  // SESSION VALIDATION
  // =========================
  const validateSession = useCallback(async (token) => {
    try {
      const apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiBaseUrl}/api/auth/validate`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        console.warn('AuthContext - Session validation failed');
        logout();
        return false;
      }

      console.log('AuthContext - Session validated');
      return true;
    } catch (error) {
      console.error('AuthContext - Session validation error:', error);
      // Don't logout on network errors, just log it
      return true;
    }
  }, [logout]);

  // =========================
  // LOAD USER FROM STORAGE
  // =========================
  const initializeAuth = useCallback(() => {
    try {
      console.log('AuthContext - Initializing authentication...');

      const storedUser = secureStorage.getItem('user');
      const storedToken = secureStorage.getItem('token');

      if (storedUser && storedToken) {
        // Validate token format
        if (typeof storedToken === 'string' && storedToken.length > 10) {
          const userWithToken = {
            ...storedUser,
            token: storedToken
          };

          setUser(userWithToken);
          console.log('AuthContext - User authenticated:', userWithToken.email);

          // Validate session with backend (optional)
          validateSession(storedToken);
        } else {
          console.warn('AuthContext - Invalid token format, clearing storage');
          secureStorage.removeItem('user');
          secureStorage.removeItem('token');
        }
      } else {
        console.log('AuthContext - No stored credentials found');
      }
    } catch (error) {
      console.error('AuthContext - Error initializing auth:', error);
      secureStorage.removeItem('user');
      secureStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  }, [validateSession]);

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  // =========================
  // AUTH FETCH (JWT SAFE)
  // =========================
  const authFetch = useCallback(async (url, options = {}) => {
    const token = user?.token || secureStorage.getItem('token');

    if (!token) {
      throw new Error('No authentication token found');
    }

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...(options.headers || {})
    };

    // Remove Content-Type for FormData
    if (options.body instanceof FormData) {
      delete headers['Content-Type'];
    }

    const apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    const finalUrl = url.startsWith('http') ? url : `${apiBaseUrl}${url.startsWith('/') ? '' : '/'}${url}`;

    console.log('AuthContext - Making authenticated request to:', finalUrl);

    try {
      const response = await fetch(finalUrl, {
        ...options,
        headers,
        credentials: 'include'
      });

      // Handle 401 Unauthorized
      if (response.status === 401) {
        console.warn('AuthContext - Token expired or invalid');
        logout();
        throw new Error('Session expired. Please log in again.');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        throw new Error('Access denied. Insufficient permissions.');
      }

      const responseText = await response.text();
      let data;

      try {
        data = responseText ? JSON.parse(responseText) : {};
      } catch (e) {
        console.error('AuthContext - Failed to parse response:', responseText);
        throw new Error('Invalid server response');
      }

      if (!response.ok) {
        throw new Error(data.error || data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('AuthContext - Auth fetch error:', error);
      throw error;
    }
  }, [user?.token, logout]);

  // =========================
  // LOGIN
  // =========================
  const login = useCallback(async (email, password) => {
    try {
      console.log('=== AUTH LOGIN START ===');
      console.log('AuthContext - Login attempt:', { email, password: '***' });

      // Use the API base URL from config
      const apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const loginUrl = `${apiBaseUrl}/api/auth/login`;

      console.log('AuthContext - Login URL:', loginUrl);

      const response = await fetch(loginUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      });

      console.log('AuthContext - Login response status:', response.status);
      console.log('AuthContext - Login response headers:', response.headers);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.log('AuthContext - Login error response:', errorData);
        throw new Error(errorData.error || errorData.message || 'Login failed');
      }

      const data = await response.json();
      console.log('AuthContext - Login response data:', data);

      if (!data.token || !data.user) {
        console.log('AuthContext - Invalid server response:', data);
        throw new Error('Invalid server response');
      }

      const loggedUser = {
        ...data.user,
        token: data.token
      };

      console.log('AuthContext - Storing authentication data...');

      // Securely store authentication data
      const tokenStored = secureStorage.setItem('token', data.token);
      const userStored = secureStorage.setItem('user', data.user);

      console.log('AuthContext - Storage results:', { tokenStored, userStored });

      if (!tokenStored || !userStored) {
        throw new Error('Failed to store authentication data');
      }

      setUser(loggedUser);
      setAuthError(null);

      console.log('AuthContext - Login successful:', loggedUser);
      console.log('=== AUTH LOGIN SUCCESS ===');
      return loggedUser;
    } catch (error) {
      console.error('=== AUTH LOGIN ERROR ===');
      console.error('AuthContext - Login error:', error);
      console.error('AuthContext - Error stack:', error.stack);
      setAuthError(error.message);
      throw error;
    }
  }, []);

  // =========================
  // REGISTER
  // =========================
  const register = useCallback(async (formData) => {
    try {
      console.log('=== AUTH REGISTER START ===');
      console.log('AuthContext - Register attempt with FormData');

      // Log FormData contents (without sensitive data)
      const formDataObj = {};
      for (let [key, value] of formData.entries()) {
        if (key === 'password') {
          formDataObj[key] = '***';
        } else if (value instanceof File) {
          formDataObj[key] = `File: ${value.name} (${value.size} bytes)`;
        } else {
          formDataObj[key] = value;
        }
      }
      console.log('AuthContext - FormData contents:', formDataObj);

      const apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiBaseUrl}/api/auth/register`, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      console.log('AuthContext - Register response status:', response.status);
      console.log('AuthContext - Register response headers:', response.headers);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.log('AuthContext - Register error response:', errorData);
        throw new Error(errorData.error || 'Registration failed');
      }

      const data = await response.json();
      console.log('AuthContext - Register response data:', data);

      if (!data.token || !data.user) {
        console.log('AuthContext - Invalid server response:', data);
        throw new Error('Invalid server response');
      }

      const newUser = {
        ...data.user,
        token: data.token
      };

      console.log('AuthContext - Storing authentication data...');

      // Securely store authentication data
      const tokenStored = secureStorage.setItem('token', data.token);
      const userStored = secureStorage.setItem('user', data.user);

      console.log('AuthContext - Storage results:', { tokenStored, userStored });

      if (!tokenStored || !userStored) {
        throw new Error('Failed to store authentication data');
      }

      setUser(newUser);
      setAuthError(null);

      console.log('AuthContext - Registration successful:', newUser);
      console.log('=== AUTH REGISTER SUCCESS ===');
      return newUser;
    } catch (error) {
      console.error('=== AUTH REGISTER ERROR ===');
      console.error('AuthContext - Registration error:', error);
      console.error('AuthContext - Error stack:', error.stack);
      setAuthError(error.message);
      throw error;
    }
  }, []);

  // =========================
  // UPDATE PROFILE
  // =========================
  const updateProfile = useCallback(async (profileData) => {
    try {
      console.log('AuthContext - updateProfile called with:', profileData);

      const data = await authFetch('/api/profile/update', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      });

      console.log('AuthContext - Backend response:', data);

      const updatedUser = { ...user, ...profileData };

      console.log('AuthContext - Updated user object:', updatedUser);

      // Update storage and state
      secureStorage.setItem('user', updatedUser);
      setUser(updatedUser);

      console.log('AuthContext - User state updated successfully');

      return updatedUser;
    } catch (error) {
      console.error('AuthContext - Profile update error:', error);
      throw error;
    }
  }, [user, authFetch]);

  // =========================
  // REFRESH TOKEN
  // =========================
  const refreshToken = useCallback(async () => {
    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();

      if (data.token) {
        secureStorage.setItem('token', data.token);
        setUser(prev => ({ ...prev, token: data.token }));
        console.log('AuthContext - Token refreshed successfully');
      }

      return data.token;
    } catch (error) {
      console.error('AuthContext - Token refresh error:', error);
      logout();
      throw error;
    }
  }, [logout]);

  const value = {
    user,
    loading,
    authError,
    login,
    register,
    logout,
    updateProfile,
    refreshToken,
    authFetch,
    setUser,
    isAuthenticated: !!user?.token,
    clearAuthError: () => setAuthError(null)
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export default AuthContext;
