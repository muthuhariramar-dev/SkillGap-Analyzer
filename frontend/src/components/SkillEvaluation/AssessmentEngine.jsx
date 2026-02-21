import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import CodingEditor from './CodingEditor';
import CameraMonitor from './CameraMonitor';
import ResultAnalytics from './ResultAnalytics';
import '../../styles/SkillEvaluation.css';

const ViolationNotification = ({ message }) => (
    <div className="warning-overlay">
        <h2>⚠️ Proctoring Warning</h2>
        <p>{message}</p>
        <div className="warning-pulse"></div>
    </div>
);

const LANGUAGES = ['C', 'C++', 'Java', 'Python'];

/**
 * AssessmentEngine – Full-screen, proctored assessment.
 *
 * Props:
 *   onExit()  – called to leave the assessment
 *   role      – target role string (e.g. 'software-engineer'). Falls back to
 *               localStorage value or 'software-engineer' if not provided.
 *
 * Phases: loading | loadError | mcq | langSelect | coding | submitting | results
 */
const AssessmentEngine = ({ onExit, role: roleProp, difficulty = 'medium', mcqCount = 10, codingCount = 10 }) => {
    // ── Resolve & Normalize Role ──
    const normalizeRole = (name) => {
        if (!name) return 'software-engineer';
        const map = {
            "WordPress Developer": "wordpress-developer",
            "Software Engineer[AGILE]": "software-engineer-agile",
            "Mobile Developer": "mobile-developer",
            "Game Developer": "game-developer",
            "Big Data Developer": "big-data-developer",
            "Developmental Operations Engineer": "devops-engineer",
            "Data Scientist": "data-scientist",
            "Security Developer": "security-developer",
            "Graphics Developer": "graphics-developer",
            "Frontend Developer": "frontend-developer",
            "Backend Developer": "backend-developer",
            "Full Stack Developer": "fullstack-developer",
            "Product Manager": "product-manager",
            "Team Lead": "team-lead",
            "UI/UX Designer": "ui-ux-designer",
        };
        if (map[name]) return map[name];
        // eslint-disable-next-line no-useless-escape
        return name.toLowerCase()
            // eslint-disable-next-line no-useless-escape
            .replace(/[\[\](){}]/g, '')
            .replace(/\//g, '-')
            .replace(/[^a-z0-9\s-]/g, '')
            .trim()
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');
    };

    const resolvedRole = (() => {
        let rawRole = roleProp;
        if (!rawRole) {
            try {
                const stored = JSON.parse(localStorage.getItem('user') || '{}');
                rawRole = stored.targetRole || stored.role || 'software-engineer';
            } catch {
                rawRole = 'software-engineer';
            }
        }
        return normalizeRole(rawRole);
    })();

    // Config based on difficulty - Standardized to 10 MCQ as per original process
    const diffConfig = {
        low: { qCount: 10, time: 15 * 60 },
        medium: { qCount: 10, time: 25 * 60 },
        high: { qCount: 10, time: 35 * 60 }
    }[difficulty] || { qCount: 10, time: 25 * 60 };

    // ── Refined 6-Step Assessment Lifecycle ──
    // READY -> INITIALIZING -> WALKTHROUGH -> QUESTION_LOADING -> PROCTORING_START -> TEST_ACTIVE
    const [assessmentStage, setAssessmentStage] = useState('READY');
    const [phase, setPhase] = useState('loading'); // Maintain for component compatibility
    const [loadStatus, setLoadStatus] = useState('Initialising your assessment…');
    const [loadError, setLoadError] = useState(null);
    const [terminationReason, setTerminationReason] = useState(null);
    const isMonitoringActiveRef = useRef(false);

    const [mcqQuestions, setMcqQuestions] = useState([]);
    const [codingQuestions, setCodingQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [mcqAnswers, setMcqAnswers] = useState({});
    const [selectedLang, setSelectedLang] = useState('');
    const [codingAnswers, setCodingAnswers] = useState({});
    const [violations] = useState([]);
    const [result, setResult] = useState(null);
    const [timer, setTimer] = useState(0);
    const [violationWarned, setViolationWarned] = useState(false);
    const [warningMessage, setWarningMessage] = useState(null);
    const startTime = useRef(Date.now());

    // ── STEP 4, 5 & 6: Loading & Activation ──
    const handleBeginAssessment = useCallback(async () => {
        setAssessmentStage('QUESTION_LOADING');
        setLoadStatus('📂 Generating your personalized assessment…');

        const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

        try {
            const token = localStorage.getItem('token');
            // Call the unified generation API (10 MCQ + 10 Coding)
            const res = await axios.post(`${API_URL}/api/generate-assessment`, {
                role: resolvedRole,
                count_mcq: mcqCount,
                count_coding: codingCount
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (!res.data.success) throw new Error(res.data.error || 'Failed to generate questions.');

            setMcqQuestions(res.data.mcqQuestions || []);
            setCodingQuestions(res.data.codingQuestions || []);

            // STEP 5: Start AI Proctoring (Camera -> Fullscreen)
            setAssessmentStage('PROCTORING_START');
            setLoadStatus('📹 Initializing AI Proctoring & Fullscreen…');

            // 1. Camera Access
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                // We only need to verify access here; the actual monitoring stream is managed by CameraMonitor
                stream.getTracks().forEach(track => track.stop());
            } catch (camErr) {
                console.warn('Camera Access Error:', camErr);
                throw new Error('Camera and Microphone access are mandatory for this proctored assessment.');
            }

            // 2. Enable Fullscreen
            if (document.documentElement.requestFullscreen) {
                try {
                    await document.documentElement.requestFullscreen();
                } catch (fsErr) {
                    console.warn('Fullscreen request failed:', fsErr);
                }
            }

            // STEP 6: Activate Test
            startTime.current = Date.now();
            setAssessmentStage('TEST_ACTIVE');
            setPhase('mcq');
            setCurrentIndex(0);

            // Activate monitoring only after UI is ready
            setTimeout(() => {
                isMonitoringActiveRef.current = true;
            }, 2000);

        } catch (err) {
            console.error('Workflow Execution Error:', err);
            setLoadError(err.message || 'Assessment initialization failed. Please retry.');
            setAssessmentStage('ERROR');
        }
    }, [resolvedRole, mcqCount, codingCount]);

    // ── STEP 1 & 2: Initialization Pipeline ──
    const startInitialization = useCallback(async () => {
        setAssessmentStage('INITIALIZING');
        setLoadStatus('Validating session parameters…');

        try {
            if (!resolvedRole) throw new Error('Target role not identified.');

            // Move directly to Loading Stage (SKIP WALKTHROUGH)
            handleBeginAssessment();
        } catch (err) {
            setLoadError('Assessment initialization failed. Please retry.');
            setAssessmentStage('ERROR');
        }
    }, [resolvedRole, handleBeginAssessment]);

    // ── Log violation to backend ──
    const logViolationToBackend = useCallback(async (reason) => {
        try {
            const token = localStorage.getItem('token');
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            await axios.post(`${API_URL}/api/assessment/violation`, {
                violationType: reason,
                timestamp: new Date().toISOString()
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
        } catch (err) {
            console.error('Failed to log violation:', err);
        }
    }, []);

    // ── Submit ──
    const handleSubmit = useCallback(async (forced = false, reason = '') => {
        if (phase === 'results' || (phase === 'submitting' && !forced)) return;

        if (!forced) setPhase('submitting');

        try {
            const token = localStorage.getItem('token');
            const completionTime = Math.floor((Date.now() - startTime.current) / 1000);

            const payload = {
                mcqAnswers: mcqQuestions.map((_, i) => mcqAnswers[i] || null),
                mcqQuestions,
                codingAnswers: codingQuestions.map((_, i) => codingAnswers[i] || { code: '', timeTaken: 0 }),
                codingQuestions,
                violations: forced ? [...violations, { reason, timestamp: new Date().toISOString() }] : violations,
                completionTime,
                forcedSubmission: forced,
            };

            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const res = await axios.post(`${API_URL}/api/skill-evaluation/evaluate`, payload, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setResult(res.data);
            if (!forced) setPhase('results');
        } catch (err) {
            console.error('Evaluation error:', err);
            const mcqCorrect = mcqQuestions.reduce((c, q, i) => c + (mcqAnswers[i] === q.correctAnswer ? 1 : 0), 0);
            setResult({
                scores: {
                    mcq: { score: Math.round((mcqCorrect / Math.max(mcqQuestions.length, 1)) * 100), correct: mcqCorrect, total: mcqQuestions.length },
                    coding: { score: 0, attempted: Object.keys(codingAnswers).length, total: codingQuestions.length },
                    behavior: { score: 0, violations: violations.length + (forced ? 1 : 0) },
                    proficiency: 0
                },
                topicAnalysis: {},
                weakTopics: [],
                recommendations: { overall: 'Evaluation failed (server unavailable).', proficiencyLevel: 'Terminated', topicRecommendations: [] },
            });
            if (!forced) setPhase('results');
        }
    }, [phase, mcqQuestions, mcqAnswers, codingQuestions, codingAnswers, violations]);

    // ── Terminate or Warn Assessment ──
    const terminateAssessment = useCallback(async (reason, immediate = false) => {
        const isTestPhase = phase === 'mcq' || phase === 'coding';
        if (!isMonitoringActiveRef.current || !isTestPhase || phase === 'terminated' || phase === 'results' || phase === 'submitting') {
            return;
        }

        if (immediate) {
            setTerminationReason(reason);
            setPhase('terminated');
            await logViolationToBackend(`TERMINATION (IMMEDIATE): ${reason}`);
            handleSubmit(true, reason);
            return;
        }

        if (!violationWarned) {
            setViolationWarned(true);
            setWarningMessage(reason);
            await logViolationToBackend(`WARNING: ${reason}`);
            setTimeout(() => setWarningMessage(null), 5000);
            return;
        }

        setTerminationReason(reason);
        setPhase('terminated');
        await logViolationToBackend(`TERMINATION (REPEATED): ${reason}`);
        handleSubmit(true, reason);
    }, [phase, violationWarned, logViolationToBackend, handleSubmit]);

    useEffect(() => {
        if (assessmentStage === 'READY') {
            startInitialization();
        }
    }, [assessmentStage, startInitialization]);

    // ── Optimized Timer (No Drift) ──
    useEffect(() => {
        if (phase === 'mcq' || phase === 'coding') {
            const id = setInterval(() => {
                const elapsed = Math.floor((Date.now() - startTime.current) / 1000);
                setTimer(elapsed);
            }, 1000);
            return () => clearInterval(id);
        }
    }, [phase]);

    const fmtTime = (s) => {
        const m = Math.floor(s / 60);
        const sec = s % 60;
        return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
    };

    // Auto-submit when time limit reached
    useEffect(() => {
        if ((phase === 'mcq' || phase === 'coding') && timer >= diffConfig.time) {
            handleSubmit(true, 'Assessment time limit reached.');
        }
    }, [timer, phase, diffConfig.time, handleSubmit]);

    // ── Fullscreen & Exit Detection ──
    useEffect(() => {
        const el = document.documentElement;
        if (el.requestFullscreen) el.requestFullscreen().catch(() => { });

        const onFsChange = () => {
            if (isMonitoringActiveRef.current && !document.fullscreenElement) {
                // IMMEDIATE for fullscreen exit
                terminateAssessment('Fullscreen exited', true);
            }
        };

        document.addEventListener('fullscreenchange', onFsChange);
        return () => {
            document.removeEventListener('fullscreenchange', onFsChange);
            // Non-destructive: we don't necessarily want to force exit here 
            // but we do need the listener to be cleaned up.
        };
    }, [terminateAssessment]);

    // ── Security Hardening: shortcuts, refresh, copy/paste ──
    useEffect(() => {
        const noCtx = (e) => e.preventDefault();

        const onKeyDown = (e) => {
            if (!isMonitoringActiveRef.current) return;

            // Block Refresh
            if (e.key === 'F5' || (e.ctrlKey && e.key === 'r') || (e.metaKey && e.key === 'r')) {
                e.preventDefault();
                terminateAssessment('Attempted browser refresh');
            }
            // Block DevTools
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
                e.preventDefault();
                terminateAssessment('DevTools shortcut detected');
            }
            // Block Copy
            if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'copy')) {
                e.preventDefault();
                terminateAssessment('Attempted to copy content');
            }
        };

        const onPaste = (e) => {
            if (!isMonitoringActiveRef.current) return;
            e.preventDefault();
            terminateAssessment('Attempted to paste content');
        };

        const onBeforeUnload = (e) => {
            if (phase === 'mcq' || phase === 'coding' || phase === 'langSelect') {
                e.preventDefault();
                e.returnValue = '';
            }
        };

        document.addEventListener('contextmenu', noCtx);
        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('paste', onPaste);
        window.addEventListener('beforeunload', onBeforeUnload);

        return () => {
            document.removeEventListener('contextmenu', noCtx);
            document.removeEventListener('keydown', onKeyDown);
            document.removeEventListener('paste', onPaste);
            window.removeEventListener('beforeunload', onBeforeUnload);
        };
    }, [terminateAssessment, phase]);

    // ── Security: tab-switch / window-blur ──
    useEffect(() => {
        const onBlur = () => {
            if (isMonitoringActiveRef.current) {
                // IMMEDIATE for tab switch
                terminateAssessment('Tab switch / Window blur detected', true);
            }
        };
        const onVisChange = () => {
            if (isMonitoringActiveRef.current && document.hidden) {
                // IMMEDIATE for tab hidden
                terminateAssessment('Tab hidden', true);
            }
        };
        window.addEventListener('blur', onBlur);
        document.addEventListener('visibilitychange', onVisChange);
        return () => {
            window.removeEventListener('blur', onBlur);
            document.removeEventListener('visibilitychange', onVisChange);
        };
    }, [terminateAssessment]);

    // ── Camera violation handler ──
    const handleCameraViolation = useCallback((reason) => {
        // Distinguish severity: multiple faces or camera hidden are high severity (immediate)
        const isImmediate = reason.toLowerCase().includes('multiple') ||
            reason.toLowerCase().includes('hidden') ||
            reason.toLowerCase().includes('covered');

        terminateAssessment(reason, isImmediate);
    }, [terminateAssessment]);

    // ── MCQ answer selection ──
    const selectMcqAnswer = (qIdx, answer) => {
        setMcqAnswers((prev) => ({ ...prev, [qIdx]: answer }));
    };

    // ── Coding answer update ──
    const updateCodingCode = (qIdx, code) => {
        setCodingAnswers((prev) => ({
            ...prev,
            [qIdx]: { code, timeTaken: Math.floor((Date.now() - startTime.current) / 1000) },
        }));
    };

    // ── Navigation ──
    const totalMcq = mcqQuestions.length;
    const totalCoding = codingQuestions.length;

    const goNext = () => {
        if (phase === 'mcq') {
            if (currentIndex < totalMcq - 1) setCurrentIndex((i) => i + 1);
            else {
                if (codingQuestions.length > 0) {
                    setCurrentIndex(0);
                    setPhase('langSelect');
                } else {
                    handleSubmit(false);
                }
            }
        } else if (phase === 'coding') {
            if (currentIndex < totalCoding - 1) setCurrentIndex((i) => i + 1);
        }
    };

    const goPrev = () => {
        if (currentIndex > 0) setCurrentIndex((i) => i - 1);
    };

    const confirmLanguage = () => {
        if (selectedLang) setPhase('coding');
    };

    // ── RENDER STAGES ──
    if (assessmentStage === 'ERROR' || phase === 'loadError') {
        return (
            <div className="loading-overlay">
                <div className="loading-error">
                    <h3>Assessment Failed to Load</h3>
                    <p>{loadError}</p>
                    <button className="btn-retry" onClick={() => setAssessmentStage('READY')}>🔄 Retry</button>
                    <button className="btn-retry" style={{ background: '#475569' }} onClick={onExit}>← Exit</button>
                </div>
            </div>
        );
    }

    if (assessmentStage === 'READY' || assessmentStage === 'INITIALIZING') {
        return (
            <div className="loading-overlay">
                <div className="spinner" />
                <p>{loadStatus}</p>
            </div>
        );
    }


    if (assessmentStage === 'QUESTION_LOADING' || assessmentStage === 'PROCTORING_START') {
        return (
            <div className="loading-overlay">
                <div className="spinner" />
                <p>{loadStatus}</p>
                <div className="gen-progress-dots">
                    <span /><span /><span />
                </div>
            </div>
        );
    }

    if (phase === 'terminated') {
        return (
            <div className="loading-overlay" style={{ background: '#450a0a' }}>
                <div className="loading-error">
                    <span style={{ fontSize: '4rem' }}>🛑</span>
                    <h2 style={{ color: '#fca5a5' }}>Assessment Terminated</h2>
                    <p style={{ color: '#fecaca', fontSize: '1.2rem', margin: '20px 0' }}>
                        Reason: <strong>{terminationReason}</strong>
                    </p>
                    <button className="btn-retry" style={{ background: '#f87171' }} onClick={() => setPhase('results')}>
                        View Partial Results
                    </button>
                </div>
            </div>
        );
    }

    if (phase === 'submitting') {
        return (
            <div className="submitting-overlay">
                <div className="spinner" />
                <p>Securing and submitting results…</p>
            </div>
        );
    }

    if (phase === 'results') {
        return <ResultAnalytics result={result} onReset={onExit} />;
    }

    // Default to Assessment UI (TEST_ACTIVE)
    return (
        <div className="assessment-fullscreen">
            {warningMessage && <ViolationNotification message={warningMessage} />}
            {/* Top bar */}
            <div className="assessment-topbar">
                <h2>{resolvedRole.charAt(0).toUpperCase() + resolvedRole.slice(1).replace(/-/g, ' ')} Assessment</h2>
                <div className="topbar-info">
                    <span className="role-tag">{resolvedRole.replace(/-/g, ' ')}</span>
                    <span>
                        {phase === 'mcq' && `MCQ ${currentIndex + 1}/${totalMcq}`}
                        {phase === 'langSelect' && 'Select Language'}
                        {phase === 'coding' && `Coding ${currentIndex + 1}/${totalCoding}`}
                    </span>
                    <span className="timer">⏱ {fmtTime(timer)} / {fmtTime(diffConfig.time)}</span>
                </div>
            </div>

            {/* Selection */}
            {phase === 'langSelect' && (
                <div className="language-selector">
                    <h2>Select Language</h2>
                    <div className="lang-options">
                        {LANGUAGES.map((lang) => (
                            <button
                                key={lang}
                                className={`lang-btn ${selectedLang === lang ? 'selected' : ''}`}
                                onClick={() => setSelectedLang(lang)}
                            >
                                {lang}
                            </button>
                        ))}
                    </div>
                    <button className="btn-confirm-lang" onClick={confirmLanguage} disabled={!selectedLang}>
                        Confirm &amp; Proceed →
                    </button>
                </div>
            )}

            {/* Body */}
            {(phase === 'mcq' || phase === 'coding') && (
                <div className="assessment-body">
                    <div className="assessment-main">
                        {phase === 'mcq' && mcqQuestions[currentIndex] && (
                            <div className="question-card">
                                <div className="question-header">
                                    <span className="question-badge">MCQ {currentIndex + 1}</span>
                                    <span className={`difficulty-badge ${mcqQuestions[currentIndex].difficulty?.toLowerCase()}`}>
                                        {mcqQuestions[currentIndex].difficulty}
                                    </span>
                                </div>
                                <div className="question-text">{mcqQuestions[currentIndex].question}</div>
                                <div className="options-grid">
                                    {mcqQuestions[currentIndex].options?.map((opt, oi) => (
                                        <button
                                            key={oi}
                                            className={`option-btn ${mcqAnswers[currentIndex] === opt ? 'selected' : ''}`}
                                            onClick={() => selectMcqAnswer(currentIndex, opt)}
                                        >
                                            {opt}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {phase === 'coding' && codingQuestions[currentIndex] && (
                            <CodingEditor
                                question={codingQuestions[currentIndex]}
                                language={selectedLang}
                                code={codingAnswers[currentIndex]?.code || ''}
                                onChange={(code) => updateCodingCode(currentIndex, code)}
                                questionIndex={currentIndex + 1}
                                totalQuestions={totalCoding}
                            />
                        )}
                    </div>

                    <div className="assessment-sidebar">
                        <CameraMonitor
                            onViolation={handleCameraViolation}
                            active={phase === 'mcq' || phase === 'coding'}
                        />
                        <div className="question-progress" style={{ marginTop: '20px' }}>
                            {(phase === 'mcq' ? mcqQuestions : codingQuestions).map((_, qi) => (
                                <div
                                    key={qi}
                                    className={`q-dot ${qi === currentIndex ? 'active' : ''} ${phase === 'mcq' ? (mcqAnswers[qi] ? 'answered' : '') : (codingAnswers[qi]?.code ? 'answered' : '')}`}
                                    onClick={() => setCurrentIndex(qi)}
                                >
                                    {qi + 1}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Nav */}
            {(phase === 'mcq' || phase === 'coding') && (
                <div className="assessment-nav">
                    <button className="btn-nav prev" onClick={goPrev} disabled={currentIndex === 0}>← Previous</button>
                    {phase === 'coding' && currentIndex === totalCoding - 1 ? (
                        <button className="btn-submit" onClick={() => handleSubmit(false)}>Submit Assessment ✓</button>
                    ) : (
                        <button className="btn-nav next" onClick={goNext}>Next →</button>
                    )}
                </div>
            )}
        </div>
    );
};

export default AssessmentEngine;
