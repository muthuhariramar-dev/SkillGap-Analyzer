// src/pages/Register.js
import React, { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaUserPlus, FaUpload, FaUserCircle } from 'react-icons/fa';
import {
  validateEmail,
  validatePassword,
  validateName,
  validateConfirmPassword,
  validateFile
} from '../utils/validation';
import { useAuth } from '../context/AuthContext';
import '../styles/Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    userType: 'student',
    profilePhoto: null,
    resume: null
  });
  const [errors, setErrors] = useState({});
  const [preview, setPreview] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef(null);
  const resumeInputRef = useRef(null);
  const navigate = useNavigate();
  const { register } = useAuth();

  const validateForm = () => {
    const newErrors = {};

    // Basic validations
    newErrors.fullName = validateName(formData.fullName);
    newErrors.email = validateEmail(formData.email);
    newErrors.password = validatePassword(formData.password);
    newErrors.confirmPassword = validateConfirmPassword(formData.password, formData.confirmPassword);

    // Profile photo validation
    newErrors.profilePhoto = validateFile(formData.profilePhoto, {
      maxSize: 5 * 1024 * 1024, // 5MB
      allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
      typeName: 'Profile photo'
    });

    // Resume validation for students
    if (formData.userType === 'student') {
      newErrors.resume = validateFile(formData.resume, {
        maxSize: 10 * 1024 * 1024, // 10MB
        allowedTypes: ['application/pdf'],
        typeName: 'Resume'
      });
    }

    // Remove empty error messages
    Object.keys(newErrors).forEach(key => {
      if (!newErrors[key]) delete newErrors[key];
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const fieldName = e.target.name;
  const newErrors = { ...errors };

  if (fieldName === 'profilePhoto') {
    const error = validateFile(file, {
      maxSize: 5 * 1024 * 1024, // 5MB
      allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
      typeName: 'Profile photo'
    });

    if (error) {
      newErrors.profilePhoto = error;
      setErrors(newErrors);
      return;
    }

    // Create preview for profile photo
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);
  } 
  // ... rest of the function


  

    
    else if (fieldName === 'resume') {
      const error = validateFile(file, {
        maxSize: 10 * 1024 * 1024,
        allowedTypes: ['application/pdf'],
        typeName: 'Resume'
      });

      if (error) {
        newErrors.resume = error;
        setErrors(newErrors);
        return;
      }
    }

    // Clear any previous errors for this field
    delete newErrors[fieldName];
    setErrors(newErrors);

    // Update form data
    setFormData(prev => ({
      ...prev,
      [fieldName]: file
    }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      // Create FormData for API call
      const formDataToSend = new FormData();
      formDataToSend.append('fullName', formData.fullName);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('password', formData.password);
      formDataToSend.append('userType', formData.userType);
      
      if (formData.profilePhoto) {
        formDataToSend.append('profilePhoto', formData.profilePhoto);
      }
      
      if (formData.userType === 'student' && formData.resume) {
        formDataToSend.append('resume', formData.resume);
      }

      // Use only the AuthContext register function
      await register(formDataToSend);
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration error:', error);
      setErrors(prev => ({
        ...prev,
        form: error.message || 'Registration failed. Please try again.'
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div 
  className="auth-background"
  style={{
    backgroundImage: `url('/Australia.png')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '20px',
    position: 'relative'
  }}
>

      <div className="auth-container">
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
        <h2>Create Your Account</h2>
        <p className="text-muted text-center mb-4">Start your skills gap analysis journey</p>
        {errors.form && <div className="error-message form-error">{errors.form}</div>}
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          {/* Profile Photo Upload */}
          <div className="form-group photo-upload" data-field="profilePhoto">
            <div 
              className="profile-photo-preview" 
              onClick={() => fileInputRef.current?.click()}
            >
              {preview ? (
                <img src={preview} alt="Profile Preview" />
              ) : (
                <div className="placeholder-icon">
                  <FaUserCircle size={80} />
                  <span>Click to upload photo</span>
                </div>
              )}
            </div>
            <input
              type="file"
              ref={fileInputRef}
              name="profilePhoto"
              accept="image/jpeg, image/png, image/jpg"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            {errors.profilePhoto && <span className="error-message">{errors.profilePhoto}</span>}
          </div>

          <div className="form-group">
            <input
              type="text"
              name="fullName"
              placeholder="Full Name"
              value={formData.fullName}
              onChange={handleChange}
              className={errors.fullName ? 'error' : ''}
            />
            {errors.fullName && <span className="error-message">{errors.fullName}</span>}
          </div>
          
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>
          
          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>
          
          <div className="form-group">
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={errors.confirmPassword ? 'error' : ''}
            />
            {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
          </div>

          {/* Resume Upload (for students) */}
          {formData.userType === 'student' && (
            <div className="form-group file-upload" data-field="resume">
              <label>
                <FaUpload /> Upload Resume (PDF only)
                <input
                  type="file"
                  ref={resumeInputRef}
                  name="resume"
                  accept=".pdf"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                />
              </label>
              {formData.resume && (
                <div className="file-info">
                  {formData.resume.name} ({(formData.resume.size / 1024).toFixed(2)} KB)
                </div>
              )}
              {errors.resume && <span className="error-message">{errors.resume}</span>}
            </div>
          )}
          
          <div className="form-group radio-group">
            <label>
              <input
                type="radio"
                name="userType"
                value="student"
                checked={formData.userType === 'student'}
                onChange={handleChange}
              />
              Student
            </label>
            <label>
              <input
                type="radio"
                name="userType"
                value="professor"
                checked={formData.userType === 'professor'}
                onChange={handleChange}
              />
              Professor
            </label>
          </div>
          
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            <FaUserPlus /> {isSubmitting ? 'Registering...' : 'Register'}
          </button>
          
          <div className="form-footer">
            <p>Already have an account? <Link to="/login">Login here</Link></p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;