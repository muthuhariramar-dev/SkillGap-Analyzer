"""
Skill-Based QA Evaluation — Backend Routes
Provides MCQ generation, coding question loading, and ML evaluation.
"""
import os
import json
import random
import re
import time
import subprocess
import tempfile
import shutil
import numpy as np
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

skill_evaluation_bp = Blueprint('skill_evaluation', __name__)


# ── Path to the 100 coding questions JSON ──
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
CODING_QUESTIONS_PATH = os.path.join(DATA_DIR, 'coding_questions.json')

# ── Load coding questions once at import time ──
try:
    with open(CODING_QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        ALL_CODING_QUESTIONS = json.load(f)
    print(f"[OK] Loaded {len(ALL_CODING_QUESTIONS)} coding questions")
except Exception as e:
    print(f"[WARN] Could not load coding questions: {e}")
    ALL_CODING_QUESTIONS = []

# ===================================================================
# ROLE-SPECIFIC MCQ TEMPLATES  (fallback when no LLM is available)
# ===================================================================
MCQ_TEMPLATES = {
    "software-engineer": [
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "correctAnswer": "O(log n)", "difficulty": "Easy", "topic": "Algorithms"},
        {"question": "Which data structure uses LIFO principle?", "options": ["Queue", "Stack", "Linked List", "Tree"], "correctAnswer": "Stack", "difficulty": "Easy", "topic": "Data Structures"},
        {"question": "What does the 'S' in SOLID stand for?", "options": ["Single Responsibility", "Simple Design", "Structured Programming", "Service Layer"], "correctAnswer": "Single Responsibility", "difficulty": "Medium", "topic": "Design Principles"},
        {"question": "Which sorting algorithm has the best average-case time complexity?", "options": ["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"], "correctAnswer": "Quick Sort", "difficulty": "Medium", "topic": "Algorithms"},
        {"question": "What is a deadlock in OS?", "options": ["A process crash", "Circular wait among processes", "Memory overflow", "CPU overload"], "correctAnswer": "Circular wait among processes", "difficulty": "Medium", "topic": "Operating Systems"},
        {"question": "Which HTTP method is idempotent?", "options": ["POST", "PATCH", "PUT", "None"], "correctAnswer": "PUT", "difficulty": "Medium", "topic": "API Design"},
        {"question": "What is the purpose of an index in a database?", "options": ["Store data", "Speed up queries", "Encrypt data", "Compress tables"], "correctAnswer": "Speed up queries", "difficulty": "Easy", "topic": "Databases"},
        {"question": "What does REST stand for?", "options": ["Remote Execution Standard Technology", "Representational State Transfer", "Reliable Endpoint Service Transfer", "Resource Estimation System"], "correctAnswer": "Representational State Transfer", "difficulty": "Easy", "topic": "API Design"},
        {"question": "Which design pattern provides a way to create objects without specifying the exact class?", "options": ["Observer", "Factory", "Singleton", "Adapter"], "correctAnswer": "Factory", "difficulty": "Medium", "topic": "Design Patterns"},
        {"question": "What is the worst-case time complexity of QuickSort?", "options": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], "correctAnswer": "O(n^2)", "difficulty": "Hard", "topic": "Algorithms"},
        {"question": "In a hash table, what is a collision?", "options": ["Two keys map to the same index", "Table overflow", "Key deletion", "Hash recalculation"], "correctAnswer": "Two keys map to the same index", "difficulty": "Easy", "topic": "Data Structures"},
        {"question": "Which traversal visits nodes level by level?", "options": ["Inorder", "Preorder", "BFS", "DFS"], "correctAnswer": "BFS", "difficulty": "Easy", "topic": "Data Structures"},
        {"question": "What is the space complexity of merge sort?", "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "correctAnswer": "O(n)", "difficulty": "Medium", "topic": "Algorithms"},
        {"question": "What is polymorphism in OOP?", "options": ["Hiding data", "Multiple forms of a method", "Inheriting classes", "Encapsulating objects"], "correctAnswer": "Multiple forms of a method", "difficulty": "Easy", "topic": "OOP"},
        {"question": "Which protocol is used for secure communication over the internet?", "options": ["HTTP", "FTP", "HTTPS", "SMTP"], "correctAnswer": "HTTPS", "difficulty": "Easy", "topic": "Networking"},
    ],
    "communication": [
        {"question": "What is the key to active listening?", "options": ["Interrupting to clarify", "Maintaining eye contact and nodding", "Thinking of your response while they speak", "Checking your phone"], "correctAnswer": "Maintaining eye contact and nodding", "difficulty": "Easy", "topic": "Communication"},
        {"question": "Which of these is a non-verbal communication cue?", "options": ["Tone of voice", "Word choice", "Email length", "Hand gestures"], "correctAnswer": "Hand gestures", "difficulty": "Easy", "topic": "Communication"},
    ],
    "problem-solving": [
        {"question": "What is the first step in the problem-solving process?", "options": ["Generating solutions", "Identifying the problem", "Evaluating alternatives", "Implementing a fix"], "correctAnswer": "Identifying the problem", "difficulty": "Easy", "topic": "Problem Solving"},
    ],
    "logical-thinking": [
        {"question": "If all A are B, and all B are C, then:", "options": ["Some A are C", "All A are C", "No A are C", "All C are A"], "correctAnswer": "All A are C", "difficulty": "Medium", "topic": "Logic"},
    ],
    "behavioral": [
        {"question": "In the STAR method, what does 'R' stand for?", "options": ["Resource", "Result", "Reasoning", "Reaction"], "correctAnswer": "Result", "difficulty": "Easy", "topic": "HR"},
    ],
    "time-management": [
        {"question": "Which technique involves working for 25 minutes then taking a 5-minute break?", "options": ["Kanban", "Pomodoro", "Eisenhower Matrix", "GTD"], "correctAnswer": "Pomodoro", "difficulty": "Easy", "topic": "Management"},
    ],
    "technical": [
        {"question": "What is the primary goal of Clean Code?", "options": ["Performance", "Readability", "Code length", "Compiler optimization"], "correctAnswer": "Readability", "difficulty": "Easy", "topic": "Best Practices"},
        {"question": "Which of these is a structural design pattern?", "options": ["Singleton", "Factory", "Adapter", "Observer"], "correctAnswer": "Adapter", "difficulty": "Medium", "topic": "Design Patterns"},
    ],
    "technical-interview": [
        {"question": "What is the time complexity of searching in a balanced binary search tree?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "correctAnswer": "O(log n)", "difficulty": "Easy", "topic": "Algorithms"},
    ],
    "aptitude": [
        {"question": "Which of the following is a prime number?", "options": ["15", "21", "29", "33"], "correctAnswer": "29", "difficulty": "Easy", "topic": "Quantitative"},
        {"question": "What is 15% of 200?", "options": ["20", "30", "40", "50"], "correctAnswer": "30", "difficulty": "Easy", "topic": "Quantitative"},
    ],
    "quantitative-aptitude": [
        {"question": "A train 100m long is running at 36km/h. How long will it take to pass a pole?", "options": ["5s", "10s", "15s", "20s"], "correctAnswer": "10s", "difficulty": "Medium", "topic": "Speed/Time"},
    ],
    "mock": [
        {"question": "What is the STAR method used for?", "options": ["Coding problems", "Behavioral questions", "Resume parsing", "System design"], "correctAnswer": "Behavioral questions", "difficulty": "Easy", "topic": "HR"},
        {"question": "Why do recruiters ask 'Tell me about yourself'?", "options": ["To check your family background", "To understand your professional journey", "To waste time", "To see if you are nervous"], "correctAnswer": "To understand your professional journey", "difficulty": "Easy", "topic": "HR"},
    ],
    "resume": [
        {"question": "Which file format is best for sending a resume?", "options": [".doc", ".txt", ".pdf", ".jpg"], "correctAnswer": ".pdf", "difficulty": "Easy", "topic": "Career"},
        {"question": "What should be included in a professional summary?", "options": ["Home address", "Key skills and experience", "Hobbies", "Salary expectations"], "correctAnswer": "Key skills and experience", "difficulty": "Easy", "topic": "Career"},
    ],
    "default": [
        {"question": "What is an algorithm?", "options": ["A programming language", "A step-by-step procedure", "A data structure", "A software tool"], "correctAnswer": "A step-by-step procedure", "difficulty": "Easy", "topic": "Fundamentals"},
        {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Processing Utility"], "correctAnswer": "Central Processing Unit", "difficulty": "Easy", "topic": "Computer Architecture"},
        {"question": "What is the primary purpose of an operating system?", "options": ["Run applications", "Manage hardware resources", "Browse the internet", "Write code"], "correctAnswer": "Manage hardware resources", "difficulty": "Easy", "topic": "Operating Systems"},
        {"question": "Which of the following is a NoSQL database?", "options": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"], "correctAnswer": "MongoDB", "difficulty": "Easy", "topic": "Databases"},
        {"question": "What is Big O notation used for?", "options": ["Naming variables", "Describing algorithm efficiency", "Writing loops", "Designing UI"], "correctAnswer": "Describing algorithm efficiency", "difficulty": "Easy", "topic": "Algorithms"},
        {"question": "Which data structure is best for implementing a priority queue?", "options": ["Array", "Linked List", "Heap", "Stack"], "correctAnswer": "Heap", "difficulty": "Medium", "topic": "Data Structures"},
        {"question": "What is a foreign key in a database?", "options": ["Primary identifier", "A field referencing another table's primary key", "An index", "A stored procedure"], "correctAnswer": "A field referencing another table's primary key", "difficulty": "Easy", "topic": "Databases"},
        {"question": "What is version control?", "options": ["Software testing", "Tracking changes in code", "Code compilation", "Server management"], "correctAnswer": "Tracking changes in code", "difficulty": "Easy", "topic": "DevOps"},
        {"question": "What is encapsulation?", "options": ["Bundling data and methods together", "Inheriting properties", "Overriding methods", "Abstracting logic"], "correctAnswer": "Bundling data and methods together", "difficulty": "Easy", "topic": "OOP"},
        {"question": "What is recursion?", "options": ["A loop construct", "A function calling itself", "A data type", "A design pattern"], "correctAnswer": "A function calling itself", "difficulty": "Medium", "topic": "Fundamentals"},
        {"question": "Which layer of the OSI model handles routing?", "options": ["Data Link", "Transport", "Network", "Application"], "correctAnswer": "Network", "difficulty": "Medium", "topic": "Networking"},
        {"question": "What is the purpose of a constructor in OOP?", "options": ["Delete objects", "Initialize objects", "Copy objects", "Compare objects"], "correctAnswer": "Initialize objects", "difficulty": "Easy", "topic": "OOP"},
        {"question": "What is SQL injection?", "options": ["A database backup", "A type of cyber attack", "A query optimization", "A join operation"], "correctAnswer": "A type of cyber attack", "difficulty": "Medium", "topic": "Security"},
        {"question": "What is a linked list?", "options": ["An array", "A linear data structure with nodes", "A tree structure", "A hash map"], "correctAnswer": "A linear data structure with nodes", "difficulty": "Easy", "topic": "Data Structures"},
        {"question": "What does API stand for?", "options": ["Application Programming Interface", "Automated Process Integration", "Application Protocol Interface", "Advanced Programming Integration"], "correctAnswer": "Application Programming Interface", "difficulty": "Easy", "topic": "API Design"},
    ]
}


# ===================================================================
# AI QUESTION GENERATOR — Google Gemini helper
# ===================================================================
def _generate_mcqs_via_gemini(role: str, count: int) -> list:
    """
    Call Google Gemini API to generate `count` MCQ questions for `role`.
    Returns a list of question dicts, or [] on any failure.
    """
    gemini_key = os.getenv('GEMINI_API_KEY', '').strip()
    if not gemini_key:
        print("[INFO] GEMINI_API_KEY not set — using static templates")
        return []

    try:
        import urllib.request
        import urllib.error

        prompt = (
            f"Generate role-based technical assessment questions with structured JSON output.\n"
            f"Generate exactly {count} MCQ questions for a {role} role.\n"
            f"Each question MUST have these exact fields:\n"
            f"  question (string), options (array of exactly 4 strings), "
            f"correctAnswer (string — must match one of the options exactly), "
            f"difficulty (one of: Easy, Medium, Hard), topic (string).\n"
            f"Focus on practical, industry-level knowledge.\n"
            f"Return ONLY a valid JSON array — no markdown fences, no extra text."
        )

        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096,
                "topP": 0.8
            }
        }).encode('utf-8')

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={gemini_key}"
        )

        req = urllib.request.Request(
            url,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode('utf-8'))

        # Extract text from Gemini response
        text = (
            body.get('candidates', [{}])[0]
                .get('content', {})
                .get('parts', [{}])[0]
                .get('text', '')
        )

        # Strip markdown code fences if present
        text = re.sub(r'```(?:json)?', '', text).strip()

        questions_raw = json.loads(text)
        if not isinstance(questions_raw, list):
            raise ValueError("Gemini did not return a JSON array")

        # Validate and normalise each question
        validated = []
        for i, q in enumerate(questions_raw[:count]):
            if not all(k in q for k in ('question', 'options', 'correctAnswer', 'difficulty', 'topic')):
                continue
            if not isinstance(q['options'], list) or len(q['options']) != 4:
                continue
            validated.append({
                "id": len(validated) + 1,
                "question": str(q['question']),
                "options": [str(o) for o in q['options']],
                "correctAnswer": str(q['correctAnswer']),
                "difficulty": str(q.get('difficulty', 'Medium')),
                "topic": str(q.get('topic', role))
            })

        print(f"[AI] Gemini generated {len(validated)} MCQs for role '{role}'")
        return validated

    except Exception as e:
        print(f"[WARN] Gemini MCQ generation failed: {e} — falling back to static templates")
        return []


# ===================================================================
# ENDPOINT 0 — Unified Assessment Generator (AI-powered)
# ===================================================================
@skill_evaluation_bp.route('/generate-assessment', methods=['POST'])
@jwt_required()
def generate_assessment():
    """
    POST /api/generate-assessment
    Body: { role, count_mcq, count_coding }

    Returns 10 AI-generated MCQs + 10 randomly selected coding questions.
    Falls back to static MCQ templates if Gemini is unavailable.
    """
    try:
        data = request.get_json() or {}
        role = data.get('role', 'software-engineer').lower().strip().replace(' ', '-')
        
        # Robust mapping for primary modules
        mapping = {
            'technical': 'software-engineer',
            'technical-interview': 'software-engineer',
            'aptitude': 'aptitude',
            'quantitative-aptitude': 'aptitude',
            'problem-solving': 'problem-solving',
            'problemsolving': 'problem-solving',
            'logical-thinking': 'logical-thinking',
            'logicalthinking': 'logical-thinking',
            'time-management': 'time-management',
            'timemanagement': 'time-management'
        }
        mapped_role = mapping.get(role, role)
        
        count_mcq = int(data.get('count_mcq', 10))
        count_coding = int(data.get('count_coding', 10))

        # ── 1. Generate MCQs via Gemini (or fall back) ──
        mcq_questions = _generate_mcqs_via_gemini(mapped_role, count_mcq)

        if not mcq_questions:
            # Fallback to static templates
            pool = MCQ_TEMPLATES.get(role, MCQ_TEMPLATES['default'])
            selected = random.sample(pool, min(count_mcq, len(pool)))

            # Pad from default if needed
            if len(selected) < count_mcq:
                extras = random.sample(
                    MCQ_TEMPLATES['default'],
                    min(count_mcq - len(selected), len(MCQ_TEMPLATES['default']))
                )
                selected.extend(extras)

            mcq_questions = [
                {
                    "id": i + 1,
                    "question": q["question"],
                    "options": q["options"],
                    "correctAnswer": q["correctAnswer"],
                    "difficulty": q["difficulty"],
                    "topic": q["topic"]
                }
                for i, q in enumerate(selected[:count_mcq])
            ]

        # ── 2. Select coding questions ──
        if not ALL_CODING_QUESTIONS:
            return jsonify({"error": "Coding questions not loaded"}), 500

        coding_questions = random.sample(
            ALL_CODING_QUESTIONS,
            min(count_coding, len(ALL_CODING_QUESTIONS))
        )

        return jsonify({
            "success": True,
            "role": role,
            "mcqQuestions": mcq_questions,
            "codingQuestions": coding_questions,
            "source": "gemini" if len(mcq_questions) > 0 and mcq_questions[0].get('id') else "static"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERROR] generate_assessment: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# ENDPOINT 0.1 — Risk Assessment Question Generator
# ===================================================================
@skill_evaluation_bp.route('/risk-assessment/generate-questions', methods=['POST'])
@jwt_required()
def generate_risk_questions():
    """
    POST /api/risk-assessment/generate-questions
    Body: { area, count }
    
    Generates 35-50 randomized MCQ questions for a specific assessment area.
    """
    try:
        data = request.get_json() or {}
        area = data.get('area', 'Technical Interview').lower().strip().replace(' ', '-')
        
        # Robust mapping for primary modules
        mapping = {
            'technical': 'software-engineer',
            'technical-interview': 'software-engineer',
            'aptitude': 'aptitude',
            'quantitative-aptitude': 'aptitude',
            'mock': 'mock',
            'resume': 'resume',
            'problem-solving': 'problem-solving',
            'problemsolving': 'problem-solving',
            'logical-thinking': 'logical-thinking',
            'logicalthinking': 'logical-thinking',
            'time-management': 'time-management',
            'timemanagement': 'time-management'
        }
        mapped_area = mapping.get(area, area)
        
        count = int(data.get('count', 35))
        
        # Ensure count is within requested range
        count = max(35, min(50, count))
        
        # 1. Attempt AI Generation
        questions = _generate_mcqs_via_gemini(mapped_area, count)
        
        # 2. Fallback to templates if AI fails
        if not questions:
            pool = MCQ_TEMPLATES.get(mapped_area, MCQ_TEMPLATES['default'])
            
            # Since templates are small, we might need to "generate" more or repeat with variations
            # For a real implementation, we'd have a larger pool or better AI fallback
            selected = []
            while len(selected) < count:
                item = random.choice(pool)
                # Avoid exact duplicates in the same set
                if item not in selected or len(pool) < count:
                    selected.append(item.copy())
                if len(selected) > 200: # Safety break
                    break
                    
            questions = [
                {
                    "id": i + 1,
                    "question": q["question"],
                    "options": q["options"],
                    "correctAnswer": q["correctAnswer"],
                    "difficulty": q["difficulty"],
                    "topic": q.get("topic", area)
                }
                for i, q in enumerate(selected[:count])
            ]
            
        return jsonify({
            "success": True,
            "area": area,
            "questions": questions,
            "count": len(questions)
        })
        
    except Exception as e:
        print(f"[ERROR] generate_risk_questions: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# ENDPOINT 1 — Generate MCQs
# ===================================================================
@skill_evaluation_bp.route('/skill-evaluation/generate-mcqs', methods=['POST'])
@jwt_required()
def generate_mcqs():
    """Return 10 MCQs for the given role."""
    try:
        data = request.get_json() or {}
        role = data.get('role', 'default').lower().replace(' ', '-')
        count = int(data.get('count', 10))

        # Pick the template pool (fall back to default)
        pool = MCQ_TEMPLATES.get(role, MCQ_TEMPLATES['default'])
        selected = random.sample(pool, min(count, len(pool)))

        # Pad with default questions if needed
        if len(selected) < count:
            remaining = count - len(selected)
            extras = random.sample(MCQ_TEMPLATES['default'],
                                   min(remaining, len(MCQ_TEMPLATES['default'])))
            selected.extend(extras)

        # Add unique id to each question
        questions = []
        for i, q in enumerate(selected[:count]):
            questions.append({
                "id": i + 1,
                "question": q["question"],
                "options": q["options"],
                "correctAnswer": q["correctAnswer"],
                "difficulty": q["difficulty"],
                "topic": q["topic"]
            })

        return jsonify({"success": True, "questions": questions})

    except Exception as e:
        print(f"[ERROR] generate_mcqs: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# ENDPOINT 2 — Get random coding questions
# ===================================================================
@skill_evaluation_bp.route('/skill-evaluation/coding-questions', methods=['GET'])
@jwt_required()
def get_coding_questions():
    """Return 10 random coding questions from the 100-question dataset."""
    try:
        count = int(request.args.get('count', 10))
        if not ALL_CODING_QUESTIONS:
            return jsonify({"error": "Coding questions not loaded"}), 500

        selected = random.sample(ALL_CODING_QUESTIONS,
                                 min(count, len(ALL_CODING_QUESTIONS)))
        return jsonify({"success": True, "questions": selected})

    except Exception as e:
        print(f"[ERROR] get_coding_questions: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# ENDPOINT 3 — Secure Code Runner
# ===================================================================
@skill_evaluation_bp.route('/run-code', methods=['POST'])
@jwt_required()
def run_code():
    """
    POST /api/run-code
    Executes user-submitted code in a temporary directory.
    Supports: Python, C, C++, Java.
    """
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        language = data.get('language', 'python').lower()

        # Basic security filters (can be expanded)
        blocked_keywords = ['os.remove', 'os.system', 'shutil.rmtree', 'rm -rf', 'format c:', 'socket']
        for kw in blocked_keywords:
            if kw in code.lower():
                return jsonify({"output": "", "error": f"Security violation: usage of '{kw}' is blocked."}), 400

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_name = ""
            compile_cmd = None
            run_cmd = []

            if language == 'python':
                file_name = "solution.py"
                run_cmd = ["python", os.path.join(tmp_dir, file_name)]
            elif language == 'c':
                file_name = "solution.c"
                exec_name = os.path.join(tmp_dir, "solution.exe")
                compile_cmd = ["gcc", os.path.join(tmp_dir, file_name), "-o", exec_name]
                run_cmd = [exec_name]
            elif language == 'c++':
                file_name = "solution.cpp"
                exec_name = os.path.join(tmp_dir, "solution.exe")
                compile_cmd = ["g++", os.path.join(tmp_dir, file_name), "-o", exec_name]
                run_cmd = [exec_name]
            elif language == 'java':
                # Java requires class name to match file name. We'll enforce/assume "Solution" class.
                file_name = "Solution.java"
                compile_cmd = ["javac", os.path.join(tmp_dir, file_name)]
                run_cmd = ["java", "-cp", tmp_dir, "Solution"]
            else:
                return jsonify({"error": f"Language '{language}' not supported."}), 400

            # Write code to file
            with open(os.path.join(tmp_dir, file_name), 'w', encoding='utf-8') as f:
                f.write(code)

            # Compile if needed
            if compile_cmd:
                cp = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
                if cp.returncode != 0:
                    return jsonify({"output": cp.stdout, "error": f"Compilation Error:\n{cp.stderr}"})

            # Execute
            try:
                cp = subprocess.run(run_cmd, capture_output=True, text=True, timeout=5)
                return jsonify({
                    "output": cp.stdout,
                    "error": cp.stderr if cp.returncode != 0 else None
                })
            except subprocess.TimeoutExpired:
                return jsonify({"output": "", "error": "Execution Timeout: Code took too long to run."})

    except Exception as e:
        print(f"[ERROR] run_code: {e}")
        return jsonify({"error": f"Server Error: {str(e)}"}), 500


# ===================================================================
# ENDPOINT 4 — Violation Logging
# ===================================================================
@skill_evaluation_bp.route('/assessment/violation', methods=['POST'])
@jwt_required()
def log_violation():
    """
    POST /api/assessment/violation
    Logs a proctoring violation for record-keeping.
    """
    try:
        data = request.get_json() or {}
        current_user = get_jwt_identity()
        violation_type = data.get('violationType', 'Unknown')
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())

        # In a real app, this would be saved to a database.
        # For now, we'll log it to the console with detail.
        print(f"[VIOLATION] User: {current_user} | Type: {violation_type} | Time: {timestamp}")

        return jsonify({"success": True, "message": "Violation logged."})

    except Exception as e:
        print(f"[ERROR] log_violation: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# ENDPOINT 5 — ML Evaluation
# ===================================================================
@skill_evaluation_bp.route('/skill-evaluation/evaluate', methods=['POST'])
@jwt_required()
def evaluate_assessment():
    """
    Receive assessment answers and produce:
      • MCQ accuracy score
      • Coding performance score
      • Behavior / proctoring score
      • Overall Skill Proficiency Score (0-100) via ML model
      • Skill-gap analysis (weak topics)
      • Personalized recommendations
    """
    try:
        data = request.get_json()
        current_user = get_jwt_identity()

        mcq_answers    = data.get('mcqAnswers', [])
        mcq_questions  = data.get('mcqQuestions', [])
        coding_answers = data.get('codingAnswers', [])
        coding_questions = data.get('codingQuestions', [])
        violations     = data.get('violations', [])
        completion_time = data.get('completionTime', 0)  # seconds

        # ── 1. MCQ Score ──
        mcq_correct = 0
        topic_results = {}  # topic → {correct, total}
        for i, q in enumerate(mcq_questions):
            topic = q.get('topic', 'General')
            if topic not in topic_results:
                topic_results[topic] = {'correct': 0, 'total': 0}
            topic_results[topic]['total'] += 1

            user_ans = mcq_answers[i] if i < len(mcq_answers) else None
            if user_ans == q.get('correctAnswer'):
                mcq_correct += 1
                topic_results[topic]['correct'] += 1

        mcq_total = max(len(mcq_questions), 1)
        mcq_score = round((mcq_correct / mcq_total) * 100, 1)

        # ── 2. Coding Score ──
        coding_attempted = 0
        coding_score_raw = 0
        coding_topic_results = {}
        for i, cq in enumerate(coding_questions):
            topic = cq.get('topic', 'General')
            if topic not in coding_topic_results:
                coding_topic_results[topic] = {'attempted': 0, 'total': 0, 'score': 0}
            coding_topic_results[topic]['total'] += 1

            ans = coding_answers[i] if i < len(coding_answers) else None
            if ans and ans.get('code', '').strip():
                coding_attempted += 1
                coding_topic_results[topic]['attempted'] += 1

                # Heuristic scoring based on code properties
                code = ans.get('code', '')
                q_score = 0

                # Syntax success — basic check that code is non-trivial
                if len(code) > 20:
                    q_score += 30
                if len(code) > 80:
                    q_score += 10

                # Structural signals
                keywords = ['def ', 'function ', 'class ', 'for ', 'while ', 'if ',
                            'return', 'int ', 'void ', 'public ', 'import ',
                            '#include', 'print', 'cout', 'System.out']
                kw_hits = sum(1 for kw in keywords if kw in code)
                q_score += min(kw_hits * 5, 30)

                # Complexity-related keywords
                complexity_kw = ['sort', 'heap', 'queue', 'stack', 'hash',
                                 'map', 'set', 'dict', 'dp', 'memo', 'cache',
                                 'binary', 'log', 'O(']
                ck_hits = sum(1 for ck in complexity_kw if ck.lower() in code.lower())
                q_score += min(ck_hits * 5, 20)

                # Time penalty factor (gentle)
                time_taken = ans.get('timeTaken', 0)
                if time_taken > 0 and time_taken < 120:
                    q_score += 10  # quick answer bonus

                q_score = min(q_score, 100)
                coding_score_raw += q_score
                coding_topic_results[topic]['score'] += q_score

        coding_total = max(len(coding_questions), 1)
        coding_score = round(coding_score_raw / coding_total, 1)

        # ── 3. Behavior Score ──
        violations_count = len(violations)
        behavior_score = max(0, 100 - violations_count * 15)

        # ── 4. ML Proficiency Score (Using sklearn LogisticRegression) ──
        # Feature vector: [mcq, coding, time_normalized, violations]
        time_norm = min(completion_time / 60, 60) / 60  # normalized 0-1 (cap 60 min)
        features = np.array([[
            mcq_score / 100,
            coding_score / 100,
            1.0 - time_norm,  # faster is better
            max(0, 1.0 - (violations_count / 10)) # fewer violations better
        ]])

        from sklearn.linear_model import LogisticRegression
        # Create a mock-trained model by injecting weights
        model = LogisticRegression()
        
        if len(coding_questions) == 0:
            # Risk/Aptitude weights
            model.coef_ = np.array([[3.0, 0.0, 0.5, 0.5]])
            model.intercept_ = np.array([-1.5])
        else:
            # Technical QA weights
            model.coef_ = np.array([[1.5, 2.0, 0.3, 0.2]])
            model.intercept_ = np.array([-1.0])
        
        # Binary classes: 0=Below, 1=Expert
        model.classes_ = np.array([0, 1])

        # Compute probability of class 1 as the proficiency score
        scores_prob = model.predict_proba(features)
        proficiency_score = round(scores_prob[0][1] * 100, 1)

        # ── 5. Skill Gap Detection ──
        weak_topics = []
        all_topics = {}

        for topic, res in topic_results.items():
            acc = (res['correct'] / max(res['total'], 1)) * 100
            all_topics[topic] = {'accuracy': round(acc, 1), 'source': 'mcq'}
            if acc < 50:
                weak_topics.append({'topic': topic, 'accuracy': round(acc, 1),
                                    'source': 'mcq'})

        for topic, res in coding_topic_results.items():
            avg = (res['score'] / max(res['total'], 1))
            all_topics[topic] = {'accuracy': round(avg, 1), 'source': 'coding'}
            if avg < 50:
                weak_topics.append({'topic': topic, 'accuracy': round(avg, 1),
                                    'source': 'coding'})

        weak_topics.sort(key=lambda x: x['accuracy'])

        # ── 6. Recommendations ──
        recommendations = _generate_recommendations(weak_topics, proficiency_score)

        # ── Build response ──
        result = {
            'success': True,
            'user': current_user,
            'timestamp': datetime.utcnow().isoformat(),
            'scores': {
                'mcq': {
                    'score': mcq_score,
                    'correct': mcq_correct,
                    'total': mcq_total
                },
                'coding': {
                    'score': coding_score,
                    'attempted': coding_attempted,
                    'total': len(coding_questions)
                },
                'behavior': {
                    'score': behavior_score,
                    'violations': violations_count
                },
                'proficiency': proficiency_score
            },
            'topicAnalysis': all_topics,
            'weakTopics': weak_topics,
            'recommendations': recommendations
        }

        print(f"[OK] Evaluation complete for {current_user}: proficiency={proficiency_score}")
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERROR] evaluate_assessment: {e}")
        return jsonify({"error": str(e)}), 500


# ===================================================================
# Recommendation Engine (rule-enhanced)
# ===================================================================
def _generate_recommendations(weak_topics, proficiency_score):
    """Produce personalised learning recommendations."""

    TOPIC_RESOURCES = {
        "Algorithms": {"practice": ["Binary Search problems", "Sorting algorithm drills"], "path": "Algorithms → Searching → Sorting → Graph Algorithms"},
        "Data Structures": {"practice": ["Linked List reversal", "BST construction"], "path": "Arrays → Linked Lists → Trees → Graphs"},
        "Dynamic Programming": {"practice": ["Climbing Stairs", "Coin Change", "LIS"], "path": "Recursion → Memoization → Tabulation → Advanced DP"},
        "API Design": {"practice": ["Build a REST API", "Implement CRUD endpoints"], "path": "HTTP Basics → REST Conventions → GraphQL"},
        "Databases": {"practice": ["SQL JOIN exercises", "Index optimization"], "path": "SQL Basics → Joins → Indexing → NoSQL"},
        "Design Principles": {"practice": ["Refactor code using SOLID", "Apply DRY"], "path": "SOLID → Clean Code → Design Patterns"},
        "OOP": {"practice": ["Implement inheritance hierarchies", "Polymorphism exercises"], "path": "Classes → Inheritance → Polymorphism → SOLID"},
        "Operating Systems": {"practice": ["Process scheduling simulations", "Deadlock avoidance"], "path": "Processes → Threads → Scheduling → Memory"},
        "Design Patterns": {"practice": ["Implement Singleton", "Factory Method"], "path": "Creational → Structural → Behavioral"},
        "Networking": {"practice": ["TCP/IP exercises", "HTTP request analysis"], "path": "OSI Model → TCP/IP → HTTP → WebSockets"},
        "Security": {"practice": ["SQL injection prevention", "XSS defense"], "path": "OWASP Top 10 → Auth → Encryption"},
        "Array & Matrix": {"practice": ["Two Sum variants", "Matrix rotation"], "path": "Basics → Two Pointers → Sliding Window → Matrix"},
        "Strings": {"practice": ["Palindrome checks", "Anagram grouping"], "path": "Basics → Pattern Matching → Advanced String DP"},
        "Trees": {"practice": ["Tree traversals", "BST validation"], "path": "Binary Trees → BST → AVL → Segment Trees"},
        "Graphs": {"practice": ["BFS/DFS drills", "Shortest path problems"], "path": "BFS/DFS → Dijkstra → Topological Sort → MST"},
        "Hashing / Sliding Window": {"practice": ["Two-pointer drills", "Window substring problems"], "path": "HashMaps → Sliding Window → Two Pointers"},
        "Recursion / Backtracking": {"practice": ["N-Queens", "Sudoku Solver"], "path": "Recursion → Backtracking → Branch and Bound"},
        "Math & Bit Manipulation": {"practice": ["Sieve of Eratosthenes", "Bit counting"], "path": "Number Theory → Bit Manipulation → Combinatorics"},
        "Miscellaneous / Greedy / Heap / Stack": {"practice": ["Histogram problems", "Merge K sorted lists"], "path": "Stack → Heap → Greedy → Advanced"},
    }

    recommendations = []
    for wt in weak_topics:
        topic = wt['topic']
        res = TOPIC_RESOURCES.get(topic, {
            "practice": [f"Practice more {topic} problems"],
            "path": f"Beginner {topic} → Intermediate → Advanced"
        })
        difficulty = "Beginner" if wt['accuracy'] < 25 else "Intermediate"
        recommendations.append({
            'topic': topic,
            'accuracy': wt['accuracy'],
            'skillsToImprove': [topic],
            'practiceTopics': res['practice'],
            'learningPath': res['path'],
            'difficulty': difficulty
        })

    # Overall guidance
    if proficiency_score >= 80:
        overall = "Excellent performance! Focus on mastering advanced topics and system design."
    elif proficiency_score >= 60:
        overall = "Good foundation. Strengthen weak areas and practice timed problem-solving."
    elif proficiency_score >= 40:
        overall = "Moderate performance. Revisit fundamentals and practice consistently."
    else:
        overall = "Needs significant improvement. Start with basics and build up gradually."

    return {
        'overall': overall,
        'proficiencyLevel': (
            'Expert' if proficiency_score >= 80 else
            'Proficient' if proficiency_score >= 60 else
            'Developing' if proficiency_score >= 40 else
            'Beginner'
        ),
        'topicRecommendations': recommendations
    }
