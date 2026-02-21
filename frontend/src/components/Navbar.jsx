// src/components/Navbar.jsx
import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaUserCircle, FaSignOutAlt, FaBars, FaTimes, FaHome, FaTachometerAlt, FaBriefcase, FaAddressBook } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [scrolled]);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsOpen(false);
  }, [location]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <img 
            src="/techbuffalo.png" 
            alt="TechBuffalo Logo" 
            className="logo-img"
          />
          <span></span>
        </Link>

        {/* Mobile menu button */}
        <div className="menu-icon" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <FaTimes /> : <FaBars />}
        </div>

        {/* Navigation Links */}
        <ul className={`nav-menu ${isOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link to="/" className="nav-link">
              <FaHome className="nav-icon" /> Home
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/dashboard" className="nav-link">
              <FaTachometerAlt className="nav-icon" /> Dashboard
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/placements" className="nav-link">
              <FaBriefcase className="nav-icon" /> Placements
            </Link>
          </li>
          <li className="nav-item">
            <button 
              onClick={() => {
                // If already on home page, scroll to team section
                if (location.pathname === '/') {
                  const teamSection = document.getElementById('team');
                  if (teamSection) {
                    teamSection.scrollIntoView({ behavior: 'smooth' });
                  }
                } else {
                  // If not on home page, navigate to home with hash
                  navigate('/#team');
                  // After navigation, scroll to team section
                  setTimeout(() => {
                    const teamSection = document.getElementById('team');
                    if (teamSection) {
                      teamSection.scrollIntoView({ behavior: 'smooth' });
                    }
                  }, 100);
                }
                setIsOpen(false); // Close mobile menu if open
              }} 
              className="nav-link"
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                padding: '0.5rem 1rem',
                textDecoration: 'none',
                color: 'inherit',
                width: '100%',
                textAlign: 'left',
                fontSize: '1rem',
                fontFamily: 'inherit'
              }}
            >
              <FaAddressBook className="nav-icon" /> Contact Us
            </button>
          </li>
        </ul>

        {/* User Section */}
        {user ? (
          <div className="nav-user">
            <div className="user-info">
              <FaUserCircle className="user-icon" />
              <span className="username">{user.fullName || 'User'}</span>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <FaSignOutAlt /> Logout
            </button>
          </div>
        ) : (
          <div className="auth-buttons">
            <Link to="/login" className="login-btn">
              Login
            </Link>
            <Link to="/register" className="register-btn">
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;