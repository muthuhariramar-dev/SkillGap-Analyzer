import React from 'react';
import '../../styles/SkillEvaluation.css';
import '../../styles/DifficultyLevels.css';

/**
 * SkillEvaluationIntro – Professional description page explaining
 * the 6-step evaluation process with step cards and icons.
 *
 * Props:
 *   onStart() – called when user clicks "Start Assessment"
 */
const SkillEvaluationIntro = ({ onStart }) => {

    const steps = [
        { icon: "🚀", title: "Step 1", name: "Assessment Initialization", desc: "Setting up your secure environment and verifying session parameters." },
        { icon: "📂", title: "Step 2", name: "Question Generation", desc: "AI-powered generation of 10 tech MCQs and 10 coding challenges." },
        { icon: "🖥️", title: "Step 3", name: "Secure Assessment", desc: "Controlled fullscreen environment with AI camera proctoring." },
        { icon: "🧠", title: "Step 4", name: "AI/ML Evaluation", desc: "Sophisticated scoring of accuracy, code quality, and time complexity." },
        { icon: "🔍", title: "Step 5", name: "Skill Gap Detection", desc: "ML analysis to identify low-performance clusters and knowledge gaps." },
        { icon: "🗺️", title: "Step 6", name: "Recommendations", desc: "Personalized learning paths and practice topics based on results." }
    ];

    return (
        <div className="skill-eval-intro">
            <div className="skill-eval-hero">
                <h1>Skill-Based QA Evaluation</h1>
                <p>Advanced AI-Proctored Skill Assessment & Gap Analysis</p>
            </div>

            <div className="process-steps-container">
                <h2 className="section-title">Evaluation Process</h2>
                <div className="steps-grid">
                    {steps.map((step, idx) => (
                        <div key={idx} className="step-card">
                            <div className="step-badge">{step.title}</div>
                            <div className="step-icon">{step.icon}</div>
                            <div className="step-content">
                                <h3>{step.name}</h3>
                                <p>{step.desc}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="start-assessment-section">
                <button
                    className="btn-start-assessment"
                    onClick={() => onStart('medium')}
                >
                    Start Full Assessment
                </button>
            </div>
        </div>
    );
};

export default SkillEvaluationIntro;
