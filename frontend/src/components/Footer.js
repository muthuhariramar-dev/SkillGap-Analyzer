// src/components/Footer.js
import React from 'react';
import { FaGithub, FaTwitter, FaLinkedin } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>TechBuffalo</h3>
          <p className="footer-description">
            Building secure, modern, and user-friendly digital experiences.
            We focus on simplicity, performance, and trust—turning ideas into impactful solutions.
          </p>
        </div>

        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul className="footer-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/about">About Us</Link></li>
            <li><Link to="/services">Services</Link></li>
            <li><Link to="/projects">Projects</Link></li>
            <li><Link to="/contact">Contact</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>What We Do</h4>
          <ul className="footer-links">
            <li>Web Development</li>
            <li>UI/UX Design</li>
            <li>Authentication Systems</li>
            <li>Secure Applications</li>
            <li>Cloud-Ready Solutions</li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Why Choose Us</h4>
          <ul className="footer-features">
            <li>✔ Clean & Scalable Architecture</li>
            <li>✔ Security-First Approach</li>
            <li>✔ Modern Design Standards</li>
            <li>✔ Reliable & Fast Performance</li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Get in Touch</h4>
          <div className="contact-info">
            <p>📧 samykmottaya@gmail.com</p>
            <p>📞 +91-8300293129</p>
            <p>📍 India</p>
          </div>
          <div className="social-links">
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              <FaGithub />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
              <FaTwitter />
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
              <FaLinkedin />
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>
          © {new Date().getFullYear()} Skills Gap Analysis System. All rights reserved.
          <br />
          Designed with passion. Built for the future.
        </p>
      </div>
    </footer>
  );
};

export default Footer;