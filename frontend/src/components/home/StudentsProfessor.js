import React from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import './StudentsProfessor.css';
import { FaUserGraduate, FaChalkboardTeacher, FaQuoteLeft, FaFilePdf, FaExternalLinkAlt } from 'react-icons/fa';

const StudentsProfessor = () => {
  const { user } = React.useContext(AuthContext);
  const [selectedStudent, setSelectedStudent] = React.useState(null);
  const [showModal, setShowModal] = React.useState(false);

  const teamMembers = [
    {
      id: 1,
      name: 'Dr. Muthuselvi ME PhD',
      role: 'Professor of Information Technology',
      description: 'With over 15+ years of experience in AI and Machine Learning, Dr. Muthuselvi guides students in cutting-edge research and practical applications.',
      isProfessor: true,
      image: 'https://picsum.photos/seed/professor-muthuselvi/400/300.jpg',
      phone: '+91 9443829654',
      email: 'mselvi.serma@gmail.com',
      link: 'https://vidwan.inflibnet.ac.in/profile/260480'
    },
    {
      id: 2,
      name: 'Mr. Santhosh.B',
      role: 'Student & QA Testing Engineer',
      description: 'Specializing in Data Science and AI, Santhosh has completed multiple internships at top tech companies and leads our student research group.',
      isProfessor: false,
      image: '/santhosh.jpg',
      phone: '+91 9876543211',
      email: 'santhoshnaga6643@gmail.com'
    },
    {
      id: 3,
      name: 'Mr. Muthu. H',
      role: 'Student Innovator & Developer',
      description: 'Focusing on Human-Computer Interaction, Muthu bridges the gap between technology and user experience in his research.',
      isProfessor: false,
      image: '/muthu.jpg',
      phone: '+91 7418062898',
      email: 'muthuharimar@gmail.com'
    },
    {
      id: 4,
      name: 'Mottaya Samy. K',
      role: 'Undergraduate Student',
      description: 'Passionate about computer vision, Samy works on developing innovative solutions for real-world problems using deep learning.',
      isProfessor: false,
      image: '/samy.jpg',
      phone: '+91 8300293129',
      email: 'samykmottaya@gmail.com'
    }
  ];

  const generateProfessorPDF = async (professor) => {
    // Create a temporary element to render the PDF content
    const element = document.createElement('div');
    element.style.position = 'absolute';
    element.style.left = '-9999px';
    element.style.width = '600px';
    element.style.padding = '30px';
    element.style.backgroundColor = 'white';
    element.style.color = '#333';
    element.style.fontFamily = 'Arial, sans-serif';

    // Format the HTML for the PDF
    element.innerHTML = `
      <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #4a90e2; padding-bottom: 20px;">
        <h1 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 28px;">${professor.name}</h1>
        <h2 style="color: #4a90e2; margin: 5px 0; font-size: 18px; font-weight: 500;">${professor.role}</h2>
      </div>

      <div style="display: flex; margin: 20px 0;">
        <div style="flex: 1; padding-right: 20px; border-right: 1px solid #eee;">
          <img 
            src="${professor.image}" 
            alt="${professor.name}" 
            style="width: 100%; max-width: 250px; border-radius: 8px; border: 1px solid #e5e7eb;"
            onerror="this.onerror=null; this.src='/placeholder-professor.jpg'"
          />
        </div>

        <div style="flex: 2; padding-left: 20px;">
          <div style="margin-bottom: 20px;">
            <h3 style="color: #2c3e50; border-bottom: 2px solid #4a90e2; padding-bottom: 5px; display: inline-block; font-size: 16px;">
              <FaGraduationCap style="margin-right: 8px;" /> Professional Profile
            </h3>
            <p style="font-size: 14px; line-height: 1.6; color: #555;">${professor.description}</p>
          </div>

          <div style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #4a90e2;">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 15px;">Contact Information</h4>
            <p style="margin: 5px 0; font-size: 13px; color: #555;">
              <FaPhone style="margin-right: 8px; color: #4a90e2;" /> ${professor.phone}
            </p>
            <p style="margin: 5px 0; font-size: 13px; color: #555;">
              <FaEnvelope style="margin-right: 8px; color: #4a90e2;" /> ${professor.email}
            </p>
            <p style="margin: 5px 0; font-size: 13px; color: #555;">
              <FaUniversity style="margin-right: 8px; color: #4a90e2;" /> Department of Information Technology
            </p>
          </div>
        </div>
      </div>

      <div style="margin-top: 20px;">
        <h3 style="color: #2c3e50; border-bottom: 2px solid #4a90e2; padding-bottom: 5px; display: inline-block; font-size: 16px;">
          Research Interests
        </h3>
        <ul style="padding-left: 20px; font-size: 14px; color: #555;">
          <li>Artificial Intelligence</li>
          <li>Machine Learning</li>
          <li>Data Science</li>
          <li>Educational Technology</li>
        </ul>
      </div>

      <div style="margin-top: 30px; font-size: 12px; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 10px;">
        <p>Generated on ${new Date().toLocaleDateString()} | Skills Gap Analysis System</p>
      </div>
    `;

    // Add the element to the document
    document.body.appendChild(element);

    try {
      // Create a canvas from the element
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        logging: false
      });

      // Convert canvas to image
      const imgData = canvas.toDataURL('image/png');

      // Create a new PDF
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth() - 20;
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      // Add the image to the PDF
      pdf.addImage(imgData, 'PNG', 10, 10, pdfWidth, pdfHeight);

      // Save the PDF
      pdf.save(`${professor.name.replace(/\s+/g, '_')}_Profile.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
      // Fallback to simple download if there's an error
      const link = document.createElement('a');
      link.href = '/Mottaya Samy K - Resume.pdf';
      link.download = `${professor.name.replace(/\s+/g, '_')}_Resume.pdf`;
      link.click();
    } finally {
      // Clean up
      document.body.removeChild(element);
    }
  };

  const handleStudentClick = (student) => {
    setSelectedStudent(student);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedStudent(null);
  };

  const TeamMemberCard = ({ member, isProfessor = false }) => (
    <div 
      className={`team-card ${isProfessor ? 'professor-card' : 'student-card'} ${!isProfessor ? 'clickable' : ''}`}
      onClick={() => !isProfessor && handleStudentClick(member)}
    >
      {isProfessor && (
        <button
          onClick={() => generateProfessorPDF(member)}
          className="pdf-download-btn"
          title="Download PDF"
        >
          <FaFilePdf />
        </button>
      )}
      <div className="card-image">
        <img 
          src={member.image} 
          alt={member.name} 
          className="member-image"
          style={{ 
            width: '100%', 
            height: '100%', 
            objectFit: 'cover',
            backgroundColor: '#f0f0f0'
          }}
          onError={(e) => {
            console.log('Image failed to load:', member.image);
            e.target.onerror = null;
            e.target.src = `https://picsum.photos/seed/${member.name}/400/300.jpg`;
          }}
          onLoad={() => {
            console.log('Image loaded successfully:', member.image);
          }}
        />
        <div className="member-icon">
          {isProfessor ? <FaChalkboardTeacher className="icon" /> : <FaUserGraduate className="icon" />}
        </div>
      </div>
      <div className="card-content">
        <h3>
          {member.link ? (
            <a 
              href={member.link} 
              target="_blank" 
              rel="noopener noreferrer"
              className="profile-link"
            >
              {member.name}
              <FaExternalLinkAlt className="external-link-icon" />
            </a>
          ) : (
            member.name
          )}
        </h3>
        <span className="role">{member.role}</span>
        <div className="testimonial">
          <FaQuoteLeft className="quote-icon" />
          <p>{member.description}</p>
          <div className="member-contact">
            {member.phone && <span>📞 {member.phone}</span>}
            {member.email && <span>📧 {member.email}</span>}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <section id="team" className="team-section">
      <div className="container">
        <div className="section-header">
          <h2>Meet Our Team</h2>
          <p>Dedicated educators and talented students working together to advance knowledge</p>
        </div>
        
        <div className="team-grid">
          {/* Professor Row */}
          <div className="professor-row">
            {teamMembers
              .filter(member => member.isProfessor)
              .map(member => (
                <TeamMemberCard key={member.id} member={member} isProfessor />
              ))}
          </div>
          
          {/* Students Row */}
          <div className="students-row">
            {teamMembers
              .filter(member => !member.isProfessor)
              .map(member => (
                <TeamMemberCard key={member.id} member={member} />
              ))}
          </div>
        </div>
        
        {!user && (
          <div className="cta-section">
            <h3>Ready to join our community?</h3>
            <Link to="/register" className="btn btn-primary">
              Get Started Today
            </Link>
          </div>
        )}
      </div>

      {/* Student Details Modal */}
      {showModal && selectedStudent && (
        <div className="student-modal-overlay" onClick={closeModal}>
          <div className="student-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>×</button>
            <div className="modal-header">
              <img 
                src={selectedStudent.image} 
                alt={selectedStudent.name} 
                className="modal-image"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = `https://picsum.photos/seed/${selectedStudent.name}/400/300.jpg`;
                }}
              />
              <div className="modal-title">
                <h2>{selectedStudent.name}</h2>
                <p className="modal-role">{selectedStudent.role}</p>
              </div>
            </div>
            <div className="modal-body">
              <div className="modal-section">
                <h3>About</h3>
                <p>{selectedStudent.description}</p>
              </div>
              <div className="modal-section">
                <h3>Contact Information</h3>
                <div className="contact-details">
                  <p><strong>Phone:</strong> 📞 {selectedStudent.phone}</p>
                  <p><strong>Email:</strong> 📧 {selectedStudent.email}</p>
                </div>
              </div>
              <div className="modal-section">
                <h3>Skills & Expertise</h3>
                <div className="skills-list">
                  {selectedStudent.name.includes('Santhosh') && (
                    <>
                      <span className="skill-tag">Data Science</span>
                      <span className="skill-tag">Artificial Intelligence</span>
                      <span className="skill-tag">QA Testing</span>
                      <span className="skill-tag">Research</span>
                    </>
                  )}
                  {selectedStudent.name.includes('Muthu') && (
                    <>
                      <span className="skill-tag">Human-Computer Interaction</span>
                      <span className="skill-tag">User Experience</span>
                      <span className="skill-tag">Development</span>
                      <span className="skill-tag">Research</span>
                    </>
                  )}
                  {selectedStudent.name.includes('Samy') && (
                    <>
                      <span className="skill-tag">Computer Vision</span>
                      <span className="skill-tag">Deep Learning</span>
                      <span className="skill-tag">Machine Learning</span>
                      <span className="skill-tag">Innovation</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default StudentsProfessor;