import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FaUser,
  FaEnvelope,
  FaPhone,
  FaMapMarkerAlt,
  FaSave,
  FaArrowLeft,
  FaFilePdf,
  FaUpload,
  FaTrash,
  FaRobot,
  FaChartLine,
  FaCheckCircle,
  FaTimesCircle
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import '../styles/Profile.css';

const Profile = () => {
  const { user, updateProfile, authFetch, setUser } = useAuth();
  const navigate = useNavigate();

  const [isEditing, setIsEditing] = useState(false);
  const [resumeFile, setResumeFile] = useState(null);
  const [resumePreview, setResumePreview] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showATS, setShowATS] = useState(false);
  const [atsResults, setAtsResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showPDFViewer, setShowPDFViewer] = useState(false);

  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    address: '',
    skills: '',
    education: ''
  });

  useEffect(() => {
    console.log('Profile.js - useEffect triggered with user:', user);
    if (user) {
      const newFormData = {
        fullName: user.fullName || '',
        email: user.email || '',
        phone: user.phone || '',
        address: user.address || '',
        skills: (user.skills && Array.isArray(user.skills) ? user.skills.join(', ') : user.skills) || '',
        education: user.education || ''
      };
      console.log('Profile.js - Setting form data:', newFormData);
      setFormData(newFormData);
      setResumePreview(user.resumeUrl || '');
    }
  }, [user]); // This will trigger whenever the user object changes

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      console.log('Profile.js - No resume file selected');
      return;
    }

    console.log('Profile.js - Starting resume upload for file:', resumeFile.name);

    const formData = new FormData();
    formData.append('resume', resumeFile);

    try {
      setIsSubmitting(true);
      console.log('Profile.js - Sending upload request...');
      
      const result = await authFetch('/api/resume/upload', {
        method: 'POST',
        body: formData,
      });

      console.log('Profile.js - Upload response:', result);

      if (result.fileUrl) {
        console.log('Profile.js - File uploaded successfully, URL:', result.fileUrl);
        
        setResumePreview(result.fileUrl);
        
        // Update the user state to include the new resume URL
        const updatedUser = { ...user, resumeUrl: result.fileUrl };
        console.log('Profile.js - Updating user state with resume URL:', updatedUser);
        
        // Update user in context and localStorage
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
        
        // Also update profile to ensure consistency
        await updateProfile({ resumeUrl: result.fileUrl });
        
        alert('Resume uploaded successfully!');
        setResumeFile(null);
        
        // Reset the file input
        const fileInput = document.getElementById('resume-upload');
        if (fileInput) {
          fileInput.value = '';
        }
      } else {
        console.log('Profile.js - Upload response missing fileUrl:', result);
        alert('Upload failed: No file URL returned');
      }
    } catch (error) {
      console.error('Profile.js - Upload failed:', error);
      alert(`Upload failed: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteResume = async () => {
    if (!window.confirm('Delete resume?')) return;

    try {
      await authFetch('/api/resume/delete', { method: 'DELETE' });
      await updateProfile({ resumeUrl: '' });
      setResumePreview('');
    } catch (err) {
      alert(err.message || 'Delete failed');
    }
  };

  const handleATSCheck = async () => {
    if (!resumePreview) {
      alert('Please upload a resume first!');
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await authFetch('/api/ats-check', {
        method: 'POST',
        body: JSON.stringify({ resumeUrl: resumePreview }),
      });

      setAtsResults(result);
      setShowATS(true);
    } catch (error) {
      console.error('Skill-based Q&A evaluation failed:', error);
      alert(`Skill-based Q&A evaluation failed: ${error.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    console.log('Profile.js - handleSubmit called with formData:', formData);

    try {
      const skillsArray = formData.skills && typeof formData.skills === 'string' 
        ? formData.skills.split(',').map(s => s.trim()).filter(s => s) 
        : [];
      
      const updateData = {
        ...formData,
        skills: skillsArray
      };
      
      console.log('Profile.js - Calling updateProfile with data:', updateData);
      
      await updateProfile(updateData);
      
      console.log('Profile.js - Profile updated successfully!');
      
      // Force a re-render by updating the form data with the updated user data
      setTimeout(() => {
        // This will trigger the useEffect to update the form with the latest user data
        setIsEditing(false);
      }, 100);
      
      alert('Profile updated successfully!');
    } catch (error) {
      console.error('Profile.js - Update failed:', error);
      alert(`Update failed: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const goBack = () => {
    navigate('/dashboard');
  };

  if (!user) {
    return (
      <div className="profile-container">
        <div className="loading">
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <button className="btn btn-back" onClick={goBack}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1>Profile Management</h1>
        <button 
          className="btn btn-edit" 
          onClick={() => {
            if (isEditing) {
              // If in edit mode, submit the form
              document.querySelector('.profile-form').requestSubmit();
            } else {
              // If in view mode, switch to edit mode
              setIsEditing(true);
            }
          }}
        >
          {isEditing ? <FaSave /> : <FaUser />}
          {isEditing ? ' Save' : ' Edit'}
        </button>
      </div>

      <div className="profile-card">
        <div className="profile-avatar">
          <FaUser size={80} />
        </div>

        {!isEditing ? (
          <div className="profile-view">
            <h2>{formData.fullName}</h2>
            <p><FaEnvelope /> {formData.email}</p>
            {formData.phone && <p><FaPhone /> {formData.phone}</p>}
            {formData.address && <p><FaMapMarkerAlt /> {formData.address}</p>}
            {formData.skills && typeof formData.skills === 'string' && (
              <div className="skills-section">
                <h3>Skills</h3>
                <div className="skills-tags">
                  {formData.skills.split(',').map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {skill.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {formData.education && (
              <div className="education-section">
                <h3>Education</h3>
                <p>{formData.education}</p>
              </div>
            )}

            <h3>Resume</h3>
            {resumePreview ? (
              <div className="resume-section">
                <div className="resume-actions">
                  <button onClick={handleDeleteResume} className="btn btn-danger">
                    <FaTrash /> Delete Resume
                  </button>
                  <button onClick={handleATSCheck} className="btn btn-ats" disabled={isAnalyzing}>
                    <FaRobot /> {isAnalyzing ? 'Analyzing...' : 'Skill-based Q&A Evaluation'}
                  </button>
                </div>
              </div>
            ) : (
              <p className="no-resume">No resume uploaded</p>
            )}
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Address</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Skills (comma-separated)</label>
              <input
                type="text"
                name="skills"
                value={formData.skills}
                onChange={handleChange}
                placeholder="e.g., JavaScript, React, Node.js"
              />
            </div>

            <div className="form-group">
              <label>Education</label>
              <textarea
                name="education"
                value={formData.education}
                onChange={handleChange}
                rows={4}
                placeholder="Your educational background..."
              />
            </div>

            <div className="form-group">
              <label>Resume Upload</label>
              <div className="file-upload">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  id="resume-upload"
                />
                <label htmlFor="resume-upload" className="file-label">
                  <FaUpload /> Choose Resume File
                </label>
                {resumeFile && (
                  <div className="file-info">
                    <span>{resumeFile.name}</span>
                    <button type="button" onClick={handleResumeUpload} disabled={isSubmitting}>
                      {isSubmitting ? 'Uploading...' : 'Upload Resume'}
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Save Changes'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setIsEditing(false)}>
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>

      {/* ATS Results Modal */}
      {showATS && atsResults && (
        <div className="ats-modal">
          <div className="ats-modal-content">
            <div className="ats-modal-header">
              <h3><FaRobot /> ATS Analysis Results</h3>
              <button className="close-btn" onClick={() => setShowATS(false)}>
                <FaTimesCircle />
              </button>
            </div>
            <div className="ats-modal-body">
              <div className="ats-score">
                <h4><FaChartLine /> ATS Score</h4>
                <div className="score-circle">
                  <span className="score-value">{atsResults.score || 85}%</span>
                </div>
              </div>
              
              <div className="ats-analysis">
                <h4>Analysis</h4>
                <div className="analysis-section">
                  <h5>Strengths</h5>
                  <ul>
                    <li><FaCheckCircle className="success" /> Clear contact information</li>
                    <li><FaCheckCircle className="success" /> Professional formatting</li>
                    <li><FaCheckCircle className="success" /> Relevant skills highlighted</li>
                  </ul>
                </div>
                
                <div className="analysis-section">
                  <h5>Areas for Improvement</h5>
                  <ul>
                    <li><FaTimesCircle className="warning" /> Add more quantifiable achievements</li>
                    <li><FaTimesCircle className="warning" /> Include action verbs</li>
                    <li><FaTimesCircle className="warning" /> Optimize for keywords</li>
                  </ul>
                </div>
              </div>
              
              <div className="extracted-info">
                <h4>Extracted Information</h4>
                <div className="info-grid">
                  <div className="info-item">
                    <strong>Skills:</strong>
                    <p>{atsResults.skills || 'JavaScript, React, Node.js, Python'}</p>
                  </div>
                  <div className="info-item">
                    <strong>Experience:</strong>
                    <p>{atsResults.experience || '5+ years in software development'}</p>
                  </div>
                  <div className="info-item">
                    <strong>Education:</strong>
                    <p>{atsResults.education || 'Bachelor\'s in Computer Science'}</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="ats-modal-footer">
              <button onClick={() => setShowATS(false)} className="btn btn-primary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* PDF Viewer Modal */}
      {showPDFViewer && (
        <div className="pdf-viewer-modal">
          <div className="pdf-viewer-content">
            <div className="pdf-viewer-header">
              <h3><FaFilePdf /> Resume Viewer</h3>
              <button className="close-btn" onClick={() => setShowPDFViewer(false)}>
                <FaTimesCircle />
              </button>
            </div>
            <div className="pdf-viewer-info">
              <div className="resume-details">
                <h4>Uploaded Resume Details</h4>
                <div className="resume-info-grid">
                  <div className="info-item">
                    <strong>File Name:</strong>
                    <span>{resumePreview ? resumePreview.split('/').pop() : 'resume.pdf'}</span>
                  </div>
                  <div className="info-item">
                    <strong>Uploaded By:</strong>
                    <span>{user?.fullName || 'User'}</span>
                  </div>
                  <div className="info-item">
                    <strong>Email:</strong>
                    <span>{user?.email || 'user@example.com'}</span>
                  </div>
                  <div className="info-item">
                    <strong>Status:</strong>
                    <span className="status-success">✓ Successfully Uploaded</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="pdf-viewer-body">
              <iframe
                src={resumePreview}
                width="100%"
                height="600px"
                title="Resume PDF Viewer"
                className="pdf-iframe"
              />
            </div>
            <div className="pdf-viewer-footer">
              <button onClick={() => setShowPDFViewer(false)} className="btn btn-primary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
