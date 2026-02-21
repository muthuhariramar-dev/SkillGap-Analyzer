import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaUser, FaSignOutAlt } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import '../../styles/header.css';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <header className="main-header">
      <div className="container">
        <div className="header-content">
          <Link to="/" className="logo">
            Skills Gap Analyzer
          </Link>
          
          <nav className="main-nav">
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
              Home
            </Link>
            <Link to="/about" className={location.pathname === '/about' ? 'active' : ''}>
              About
            </Link>
            <Link to="/students" className={location.pathname === '/students' ? 'active' : ''}>
              Students
            </Link>
            <Link to="/placements" className={location.pathname === '/placements' ? 'active' : ''}>
              Placements
            </Link>
            <Link to="/contact" className={location.pathname === '/contact' ? 'active' : ''}>
              Contact
            </Link>
          </nav>

          <div className="auth-actions">
            {user ? (
              <>
                <Link to="/profile" className="profile-link">
                  <FaUser /> {user.name || 'Profile'}
                </Link>
                <button onClick={logout} className="btn btn-link">
                  <FaSignOutAlt /> Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline">
                  Login
                </Link>
                <Link to="/register" className="btn btn-primary">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
