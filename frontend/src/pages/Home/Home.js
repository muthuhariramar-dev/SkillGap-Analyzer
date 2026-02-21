// frontend/src/pages/Home/Home.js
import React from 'react';
import HeroSection from '../../components/home/HeroSection';
import Features from '../../components/home/Features';
import StudentsProfessor from '../../components/home/StudentsProfessor';
import '../../styles/Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <HeroSection />
      <Features />
      <StudentsProfessor /> 
    </div>
  );
};

export default Home;