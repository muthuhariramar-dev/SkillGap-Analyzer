// src/pages/Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaSignInAlt } from 'react-icons/fa';
import { validateEmail, validatePassword } from '../utils/validation';
import { useAuth } from '../context/AuthContext';
import '../styles/Login.css';

const authBackgroundStyle = {
  backgroundImage: `url('/scad1.png')`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: '20px',
  position: 'relative'
};

const authContainerStyle = {
  background: 'white',
  padding: '2rem',
  borderRadius: '10px',
  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
  width: '100%',
  maxWidth: '400px',
  position: 'relative',
  zIndex: 1,
  transition: 'transform 0.3s ease, box-shadow 0.3s ease'
};

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    const emailError = validateEmail(formData.email);
    const passwordError = validatePassword(formData.password);

    if (emailError) newErrors.email = emailError;
    if (passwordError) newErrors.password = passwordError;

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));

    if (errors[name]) {
      setErrors(prev => {
        const copy = { ...prev };
        delete copy[name];
        return copy;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setErrors({
        form: err.message || 'Invalid email or password',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={authBackgroundStyle}>
      <div style={authContainerStyle}>
        <div className="auth-logo">
          <img 
            src="/techbuffalo.png" 
            alt="TechBuffalo Logo" 
            style={{
              width: '120px',
              height: 'auto',
              borderRadius: '10px',
              boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
              margin: '0 auto'
            }}
          />
        </div>
        <h2>Welcome Back</h2>
        <p className="text-muted text-center mb-4">Please enter your credentials to continue</p>

        {errors.form && (
          <div className="error-message form-error">{errors.form}</div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              disabled={isSubmitting}
            />
            {errors.email && (
              <span className="error-message">{errors.email}</span>
            )}
          </div>

          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
              disabled={isSubmitting}
            />
            {errors.password && (
              <span className="error-message">{errors.password}</span>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            <FaSignInAlt />
            {isSubmitting ? ' Logging in...' : ' Login'}
          </button>

          <div className="form-footer">
            <Link to="/forgot-password">Forgot Password?</Link>
            <p>
              Don&apos;t have an account? <Link to="/register">Register</Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
