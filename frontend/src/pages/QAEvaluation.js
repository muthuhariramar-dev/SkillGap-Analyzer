import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import SkillEvaluationIntro from '../components/SkillEvaluation/SkillEvaluationIntro';
import AssessmentEngine from '../components/SkillEvaluation/AssessmentEngine';

/**
 * QAEvaluation — Page entry-point.
 * Shows the Intro page first, then launches the AssessmentEngine on "Start".
 */
const QAEvaluation = () => {
  const [assessmentStarted, setAssessmentStarted] = useState(false);
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium');
  const location = useLocation();

  // Extract role/area from query string if available
  const queryParams = new URLSearchParams(location.search);
  const area = queryParams.get('area') || queryParams.get('role');

  const handleStart = (difficulty) => {
    setSelectedDifficulty(difficulty);
    setAssessmentStarted(true);
  };

  if (assessmentStarted) {
    return (
      <AssessmentEngine
        onExit={() => setAssessmentStarted(false)}
        role={area}
        difficulty={selectedDifficulty}
      />
    );
  }

  return (
    <SkillEvaluationIntro
      onStart={handleStart}
      role={area}
    />
  );
};

export default QAEvaluation;
