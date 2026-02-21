import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/SkillEvaluation.css';

/**
 * ResultAnalytics – Displays the ML-based evaluation results.
 *
 * Props:
 *   result  – The full result object returned by the /evaluate endpoint
 *   onReset – Callback to go back / retake
 */
const ResultAnalytics = ({ result, onReset }) => {
    const navigate = useNavigate();
    const scores = result?.scores || {};
    const weakTopics = result?.weakTopics || [];
    const recommendations = result?.recommendations || {};
    const topicAnalysis = result?.topicAnalysis || {};

    const getRiskInfo = (score) => {
        if (score >= 75) return { level: 'LOW RISK', color: '#00e676', desc: 'Candidate demonstrates strong technical and interview readiness.' };
        if (score >= 40) return { level: 'MEDIUM RISK', color: '#ffc107', desc: 'Candidate has foundational skills but requires improvement.' };
        return { level: 'HIGH RISK', color: '#f44336', desc: 'Candidate needs structured preparation across technical and non-technical skills.' };
    };

    const risk = getRiskInfo(scores.proficiency ?? 0);

    const getScoreColor = (val) => {
        if (val >= 75) return '#00e676';
        if (val >= 40) return '#ffc107';
        return '#f44336';
    };

    const barClass = (val) => {
        if (val >= 75) return '';
        if (val >= 40) return 'mid';
        return 'low';
    };

    return (
        <div className="result-analytics">
            {/* Header */}
            <div className="result-header">
                <h1>📊 Placement Risk Analysis Report</h1>
                <p>Comprehensive evaluation of your job market readiness</p>
            </div>

            {/* Overall Risk Card */}
            <div className="risk-summary-card" style={{
                borderColor: risk.color,
                backgroundColor: '#ffffff',
                boxShadow: `0 10px 40px ${risk.color}15`
            }}>
                <div className="risk-badge" style={{ backgroundColor: risk.color }}>{risk.level}</div>
                <h2 style={{ color: '#1e293b' }}>Overall Placement Risk</h2>
                <div className="proficiency-score-large" style={{
                    color: risk.color,
                    WebkitTextFillColor: risk.color,
                    background: 'none'
                }}>
                    {scores.proficiency ?? 0}%
                </div>
                <p className="risk-description" style={{ color: '#64748b', fontWeight: 500 }}>{risk.desc}</p>
            </div>

            {/* Score cards */}
            <div className="scores-grid">
                <div className="score-card">
                    <div className="score-label">Technical Score</div>
                    <div className="score-value" style={{ color: getScoreColor(scores.mcq?.score) }}>
                        {scores.mcq?.score ?? 0}%
                    </div>
                </div>

                <div className="score-card">
                    <div className="score-label">Non-Technical / Coding Score</div>
                    <div className="score-value" style={{ color: getScoreColor(scores.coding?.score) }}>
                        {scores.coding?.score ?? 0}%
                    </div>
                </div>

                <div className="score-card">
                    <div className="score-label">Proctoring Fidelity</div>
                    <div className="score-value" style={{ color: getScoreColor(scores.behavior?.score) }}>
                        {scores.behavior?.score ?? 0}%
                    </div>
                    <div className="score-label">{scores.behavior?.violations} incidents logged</div>
                </div>
            </div>

            {/* Area Breakdown */}
            {Object.keys(topicAnalysis).length > 0 && (
                <div className="topic-chart-section">
                    <h2>🔍 Area Breakdown & Skill Analysis</h2>
                    <div className="topic-bar-chart">
                        {Object.entries(topicAnalysis).map(([topic, info]) => (
                            <div className="topic-bar-row" key={topic}>
                                <span className="topic-bar-label">{topic}</span>
                                <div className="topic-bar-track">
                                    <div
                                        className={`topic-bar-fill ${barClass(info.accuracy)}`}
                                        style={{ width: `${Math.min(info.accuracy, 100)}%`, backgroundColor: getScoreColor(info.accuracy) }}
                                    />
                                </div>
                                <span className="topic-bar-value">{info.accuracy}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Skill Gaps */}
            {weakTopics.length > 0 && (
                <div className="weak-topics-section">
                    <h2>⚠️ Critical Skill Gaps Detected</h2>
                    <div className="weak-topics-list">
                        {weakTopics.map((wt, idx) => (
                            <div className="weak-topic-item" key={idx}>
                                <span className="weak-topic-name">{wt.topic}</span>
                                <span className="weak-topic-acc" style={{ color: '#f44336' }}>{wt.accuracy}% efficiency</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Personalized Roadmap */}
            {recommendations.topicRecommendations?.length > 0 && (
                <div className="recommendations-section">
                    <h2>🎯 Personalized Improvement Roadmap</h2>
                    <div className="roadmap-grid">
                        {recommendations.topicRecommendations.map((rec, idx) => (
                            <div className="rec-card" key={idx}>
                                <div className="rec-header">
                                    <h4>{rec.topic}</h4>
                                    <span className={`difficulty-badge ${rec.difficulty.toLowerCase()}`}>{rec.difficulty}</span>
                                </div>
                                <div className="rec-content">
                                    <p><strong>Action Items:</strong> {rec.practiceTopics?.join(', ')}</p>
                                    <p className="learning-path"><strong>Path:</strong> {rec.learningPath}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Overall guidance */}
            <div className="overall-guidance" style={{ marginTop: '30px' }}>
                <h3>📝 Professional Recommendation</h3>
                <p>{recommendations.overall}</p>
            </div>

            {/* Actions */}
            <div className="result-actions" style={{ marginTop: '40px', display: 'flex', gap: '20px' }}>
                <button className="btn-back-dashboard" style={{ flex: 1 }} onClick={() => navigate('/dashboard')}>
                    ← Back to Dashboard
                </button>
                {/* <button className="btn-confirm-lang" style={{ flex: 1, margin: 0 }} onClick={() => navigate('/preparation')}>
                    Retake Assessment ↺
                </button> */}
            </div>
        </div>
    );
};

export default ResultAnalytics;
