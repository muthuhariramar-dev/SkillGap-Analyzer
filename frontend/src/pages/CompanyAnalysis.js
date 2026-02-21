// src/pages/CompanyAnalysis.js
import React, { useEffect } from 'react';

const CompanyAnalysis = () => {
  useEffect(() => {
    // Open the HTML file in the same tab
    window.open('/companyanalysis.html', '_self');
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      flexDirection: 'column'
    }}>
      <h2>Redirecting to Company Analysis...</h2>
      <p>If you are not redirected automatically, <a href="/companyanalysis.html" target="_self">click here</a>.</p>
    </div>
  );
};

export default CompanyAnalysis;
