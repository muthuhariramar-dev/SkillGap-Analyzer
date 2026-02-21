import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaArrowRight, FaUsers } from 'react-icons/fa';
import '../styles/Contact.css';

const Contact = ({ id }) => {
  const navigate = useNavigate();

  const handleMeetTeamClick = () => {
    // Navigate to home page with hash to team section
    navigate('/#team');
    // Smooth scroll to team section after navigation
    setTimeout(() => {
      const teamSection = document.getElementById('team');
      if (teamSection) {
        teamSection.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  return (
    <section id={id} className="contact-section">
      <div className="container">
        <h2>Contact Us</h2>
        <div className="contact-content">
          <div className="contact-info">
            <p>Email: support@skillgapai.com</p>
            <p>Phone: +1 (123) 456-7890</p>
            <div className="meet-team-cta">
              <p>Or meet our team directly:</p>
              <button 
                onClick={handleMeetTeamClick}
                className="btn btn-secondary"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginTop: '15px',
                  padding: '10px 20px',
                  backgroundColor: '#4a90e2',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  transition: 'background-color 0.3s',
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#357abd'}
                onMouseOut={(e) => e.target.style.backgroundColor = '#4a90e2'}
              >
                <FaUsers /> Meet Our Team <FaArrowRight />
              </button>
            </div>
          </div>
          <form className="contact-form">
            <input type="text" placeholder="Your Name" required />
            <input type="email" placeholder="Your Email" required />
            <textarea placeholder="Your Message" rows="5" required></textarea>
            <button type="submit" className="btn btn-primary">Send Message</button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Contact;