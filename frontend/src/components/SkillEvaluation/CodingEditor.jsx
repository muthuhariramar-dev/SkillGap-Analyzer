import React, { useState } from 'react';
import axios from 'axios';

/**
 * CodingEditor – A themed code textarea for the coding section.
 * Now includes a RUN button and a console output panel.
 */
const CodingEditor = ({ question, language, code, onChange, questionIndex, totalQuestions }) => {
    const [isRunning, setIsRunning] = useState(false);
    const [output, setOutput] = useState(null);

    const BOILERPLATE = {
        C: '#include <stdio.h>\n\nint main() {\n    printf("Hello Technical Assessment!\\n");\n    return 0;\n}\n',
        'C++': '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello Technical Assessment!" << endl;\n    return 0;\n}\n',
        Java: 'public class Solution {\n    public static void main(String[] args) {\n        System.out.println("Hello Technical Assessment!");\n    }\n}\n',
        Python: '# Your code here\n\ndef solution():\n    print("Hello Technical Assessment!")\n\nif __name__ == "__main__":\n    solution()\n',
    };

    const placeholder = BOILERPLATE[language] || '// Write your code here\n';

    const handleRunCode = async () => {
        if (!code || isRunning) return;
        setIsRunning(true);
        setOutput(null);

        try {
            const token = localStorage.getItem('token');
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const res = await axios.post(`${API_URL}/api/run-code`, {
                code,
                language: language.toLowerCase()
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setOutput(res.data);
        } catch (err) {
            console.error('Run code error:', err);
            setOutput({
                error: err.response?.data?.error || err.message || 'Execution failed.'
            });
        } finally {
            setIsRunning(false);
        }
    };

    return (
        <div className="coding-wrapper-outer">
            {/* Question info */}
            <div className="coding-question-panel">
                <div className="question-header">
                    <span className="question-badge">
                        Coding {questionIndex}/{totalQuestions}
                    </span>
                    <span className={`difficulty-badge ${(question?.difficulty || '').toLowerCase()}`}>
                        {question?.difficulty || 'Medium'}
                    </span>
                </div>

                <h3>{question?.title || 'Coding Problem'}</h3>

                <div className="coding-meta">
                    <span>📂 {question?.topic || 'General'}</span>
                    <span>💻 {language}</span>
                </div>

                <p className="question-text">{question?.description || ''}</p>

                {question?.constraints && (
                    <p className="coding-constraints">
                        <strong>Constraints:</strong> {question.constraints}
                    </p>
                )}

                {question?.examples?.length > 0 && (
                    <div className="coding-example-box">
                        <strong className="coding-example-label">Example:</strong><br />
                        <strong>Input:</strong> {question.examples[0].input}<br />
                        <strong>Output:</strong> {question.examples[0].output}
                    </div>
                )}
            </div>

            {/* Editor */}
            <div className="code-editor-wrapper">
                <div className="code-editor-header">
                    <span>{language}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <span>{code ? code.split('\n').length : 0} lines</span>
                    </div>
                </div>
                <textarea
                    className="code-textarea"
                    value={code || ''}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder={placeholder}
                    spellCheck={false}
                    autoCapitalize="off"
                    autoCorrect="off"
                />

                {/* Runner Actions */}
                <div className="code-runner-actions">
                    <button
                        className="btn-run-code"
                        onClick={handleRunCode}
                        disabled={isRunning || !code}
                    >
                        {isRunning ? '⏳ Running...' : '▶ Run Code'}
                    </button>
                </div>

                {/* Output Console */}
                {output && (
                    <div className="output-console">
                        <div className="console-header">
                            <span>Output Console</span>
                            <button
                                style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
                                onClick={() => setOutput(null)}
                            >
                                ✕
                            </button>
                        </div>
                        <div className="console-body">
                            {output.error ? (
                                <div className="stderr-text">{output.error}</div>
                            ) : output.output ? (
                                <div className="stdout-text">{output.output}</div>
                            ) : (
                                <div className="empty-output">Program finished with no output.</div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CodingEditor;
