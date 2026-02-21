from flask import Blueprint, request, jsonify
import os
import json
import re
import random

# Create Blueprint
role_assessment_bp = Blueprint('role_assessment', __name__)

# ===== ROLE-TO-DATASET MAPPING =====
# Explicit mapping: Role Title -> kebab-case filename (without .json)
ROLE_MAP = {
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
}

def role_to_filename(role_name):
    """
    Convert a role name to a safe kebab-case filename.
    Rules:
      - lowercase
      - remove special chars like [ ] /
      - spaces -> hyphens
      - collapse multiple hyphens
    Examples:
      "Frontend Developer"        -> "frontend-developer"
      "Software Engineer[AGILE]"  -> "software-engineer-agile"
      "UI/UX Designer"            -> "ui-ux-designer"
    """
    # Check explicit map first
    if role_name in ROLE_MAP:
        return ROLE_MAP[role_name]
    # Fallback: auto-convert
    name = role_name.lower()
    name = re.sub(r'[\[\](){}]', '', name)   # remove brackets
    name = name.replace('/', '-')             # slash -> hyphen
    name = re.sub(r'[^a-z0-9\s-]', '', name) # remove other special chars
    name = name.strip().replace(' ', '-')     # spaces -> hyphens
    name = re.sub(r'-+', '-', name)           # collapse multiple hyphens
    return name

# ===== DATASET LOADING =====
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'roles')

def normalize_question(q, role_id, index):
    """Normalize a single question object with required fields."""
    # Ensure ID exists
    if 'id' not in q:
        q['id'] = f"{role_id}_q{index}"
    
    # Ensure skill exists (map from topic)
    if 'skill' not in q and 'topic' in q:
        q['skill'] = q['topic']
    elif 'skill' not in q:
        q['skill'] = 'General'
        
    # Ensure correct index exists (resolve from correctAnswer)
    if 'correct' not in q and 'correctAnswer' in q:
        try:
            # Trim whitespace for robust comparison
            target = str(q['correctAnswer']).strip()
            options = [str(opt).strip() for opt in q['options']]
            q['correct'] = options.index(target)
        except (ValueError, KeyError):
            q['correct'] = 0
    elif 'correct' not in q:
        q['correct'] = 0
    return q

def load_role_questions():
    """Load and normalize all role question datasets from JSON files."""
    questions = {}
    
    if not os.path.exists(DATA_DIR):
        print(f"[WARNING] Role data directory not found: {DATA_DIR}")
        return questions

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            role_id = filename.replace('.json', '')
            file_path = os.path.join(DATA_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    raw_qs = []
                    if isinstance(data, list):
                        raw_qs = data
                    elif isinstance(data, dict) and 'questions' in data:
                        raw_qs = data['questions']
                    
                    # Normalize questions
                    normalized_qs = [normalize_question(q, role_id, i) for i, q in enumerate(raw_qs)]
                    questions[role_id] = normalized_qs
                    
                print(f"[INFO] Loaded {len(questions[role_id])} questions for role: {role_id}")
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")

    return questions

def load_single_role(role_slug):
    """Load and normalize questions for a single role by its kebab-case slug."""
    file_path = os.path.join(DATA_DIR, f"{role_slug}.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            raw_qs = []
            if isinstance(data, list):
                raw_qs = data
            elif isinstance(data, dict) and 'questions' in data:
                raw_qs = data['questions']
            
            return [normalize_question(q, role_slug, i) for i, q in enumerate(raw_qs)]
    except Exception as e:
        print(f"[ERROR] Failed to load {role_slug}.json: {e}")
        return None

# Initialize all questions at startup
role_questions = load_role_questions()

# ===== API ENDPOINTS =====

@role_assessment_bp.route('/roles', methods=['GET'])
def list_roles():
    """List all available roles and their dataset status."""
    roles = []
    for title, slug in ROLE_MAP.items():
        q = role_questions.get(slug, [])
        roles.append({
            "title": title,
            "slug": slug,
            "questionCount": len(q),
            "available": len(q) > 0
        })
    return jsonify({"success": True, "roles": roles})

@role_assessment_bp.route('/questions/<role_slug>', methods=['GET'])
def get_questions_by_role(role_slug):
    """
    GET /api/questions/<role_slug>
    Fetch questions for a role by its kebab-case slug.
    Example: GET /api/questions/frontend-developer
    """
    questions = role_questions.get(role_slug)
    
    if questions is None:
        # Try loading dynamically in case it was added after startup
        questions = load_single_role(role_slug)
    
    if not questions:
        available = list(role_questions.keys())
        return jsonify({
            "success": False,
            "message": f"No questions found for role: {role_slug}",
            "availableRoles": available
        }), 404
    
    # Optional: limit via query param ?limit=10
    limit = request.args.get('limit', type=int)
    if limit:
        shuffled = questions.copy()
        random.shuffle(shuffled)
        questions = shuffled[:limit]
    
    return jsonify({
        "success": True,
        "role": role_slug,
        "questions": questions,
        "totalQuestions": len(questions)
    })

@role_assessment_bp.route('/generateRoleQuestions', methods=['POST'])
def generate_role_questions():
    try:
        data = request.get_json()
        role_id = data.get('roleId')
        role_title = data.get('roleTitle')
        required_skills = data.get('requiredSkills')

        if not role_id:
            return jsonify({
                'success': False,
                'message': 'Role ID is required'
            }), 400

        questions = role_questions.get(role_id)

        if not questions:
            return jsonify({
                'success': False,
                'message': f'Questions not found for role: {role_id}',
                'availableRoles': list(role_questions.keys())
            }), 404

        # Shuffle and select 10 questions
        shuffled_questions = questions.copy()
        random.shuffle(shuffled_questions)
        selected_questions = shuffled_questions[:10]
        
        formatted_questions = []
        for q in selected_questions:
            formatted_questions.append({
                'id': q['id'],
                'question': q['question'],
                'options': q['options'],
                'skill': q['skill']
            })

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'roleTitle': role_title,
            'totalQuestions': len(formatted_questions)
        })
    except Exception as error:
        print(f'Error generating questions: {error}')
        return jsonify({
            'success': False,
            'message': 'Error generating questions',
            'error': str(error)
        }), 500

@role_assessment_bp.route('/analyzeRoleResults', methods=['POST'])
def analyze_role_results():
    try:
        data = request.get_json()
        role_id = data.get('roleId')
        role_title = data.get('roleTitle')
        questions = data.get('questions')
        answers = data.get('answers')

        if not role_id or not questions or not answers:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        role_question_bank = role_questions.get(role_id)
        if not role_question_bank:
            return jsonify({
                'success': False,
                'message': f'Role not found: {role_id}'
            }), 404

        # Calculate scores
        total_score = 0
        skill_scores = {}

        for question in questions:
            answer = next((a for a in answers if a.get('questionId') == question['id']), None)
            correct_question = next((q for q in role_question_bank if q['id'] == question['id']), None)

            if answer and correct_question:
                # Find correct index
                correct_base = correct_question.get('correct', 0)
                
                # Robust comparison: cast to int to prevent type mismatch
                try:
                    user_sel = int(answer.get('selectedOption', -1))
                except (ValueError, TypeError):
                    user_sel = -1

                is_correct = user_sel == correct_base
                if is_correct:
                    total_score += 1

                # Track skill scores
                skill = correct_question.get('skill', 'General')
                if skill not in skill_scores:
                    skill_scores[skill] = {'correct': 0, 'total': 0}
                skill_scores[skill]['total'] += 1
                if is_correct:
                    skill_scores[skill]['correct'] += 1

        overall_score = round((total_score / len(questions)) * 100) if len(questions) > 0 else 0

        # Determine readiness level
        readiness = 'Need Improvement'
        if overall_score >= 80:
            readiness = 'Excellent'
        elif overall_score >= 60:
            readiness = 'Good'
        elif overall_score >= 40:
            readiness = 'Moderate'

        # Build skill breakdown
        skill_breakdown = []
        for skill, scores in skill_scores.items():
            score_percent = round((scores['correct'] / scores['total']) * 100)
            level = 'Strong' if scores['correct'] / scores['total'] >= 0.7 else 'Needs Work'
            skill_breakdown.append({
                'skill': skill,
                'correct': scores['correct'],
                'total': scores['total'],
                'score': score_percent,
                'level': level
            })

        # Generate recommendations
        recommendations = []
        for skill in skill_breakdown:
            if skill['level'] == 'Needs Work':
                recommendations.append(f"Focus on improving your {skill['skill']} skills - current proficiency: {skill['score']}%")

        if not recommendations:
            recommendations.append(f"Excellent grasp of {role_title} fundamentals! Consider advanced topics.")

        # Generate next steps
        next_steps = [
            f"Complete online courses in weak skill areas",
            f"Practice real-world projects related to {role_title}",
            "Review concepts with score below 70%",
            "Build a portfolio demonstrating your skills",
            "Seek mentorship in relevant areas"
        ]

        return jsonify({
            'success': True,
            'analysis': {
                'roleTitle': role_title,
                'overallScore': overall_score,
                'readiness': readiness,
                'skillScores': skill_breakdown,
                'recommendations': recommendations,
                'nextSteps': next_steps,
                'totalAttempted': len(questions),
                'totalCorrect': total_score
            }
        })
    except Exception as error:
        print(f'Error analyzing results: {error}')
        return jsonify({
            'success': False,
            'message': 'Error analyzing results',
            'error': str(error)
        }), 500
