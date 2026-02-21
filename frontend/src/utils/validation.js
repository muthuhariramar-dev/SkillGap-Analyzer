// src/utils/validation.js
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) return 'Email is required';
  if (!emailRegex.test(email)) return 'Please enter a valid email address';
  return '';
};

export const validatePassword = (password) => {
  if (!password) return 'Password is required';
  if (password.length < 6) return 'Password must be at least 6 characters';
  return '';
};

export const validateName = (name) => {
  if (!name.trim()) return 'Full Name is required';
  if (name.trim().length < 3) return 'Name must be at least 3 characters';
  return '';
};

export const validateConfirmPassword = (password, confirmPassword) => {
  if (!confirmPassword) return 'Please confirm your password';
  if (password !== confirmPassword) return 'Passwords do not match';
  return '';
};

export const validateFile = (file, options = {}) => {
  const { maxSize = 5 * 1024 * 1024, allowedTypes = [], typeName = 'file' } = options;
  
  if (!file) return `${typeName} is required`;
  if (file.size > maxSize) return `${typeName} size should be less than ${maxSize / (1024 * 1024)}MB`;
  if (allowedTypes.length && !allowedTypes.includes(file.type)) {
    return `Only ${allowedTypes.map(t => t.split('/').pop()).join(', ')} files are allowed`;
  }
  return '';
};