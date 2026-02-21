"""
Adaptive Assessment System for Skills Gap Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

class AdaptiveAssessmentSystem:
    """
    Advanced Adaptive Assessment System for Skills Gap Analysis
    Features: Reinforcement Learning, Bayesian Networks, Decision Trees,
              Item Response Theory, Difficulty Adaptation, Personalized Testing
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.difficulty_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.skill_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.bayesian_classifier = GaussianNB()
        self.decision_tree = DecisionTreeClassifier(random_state=42)
        self.neural_network = MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
        self.is_trained = False
        
        # Item Response Theory parameters
        self.irt_parameters = {
            'discrimination': [],
            'difficulty': [],
            'guessing': []
        }
        
        # Reinforcement Learning parameters
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1

    def initialize_assessment(self, user_profile, skill_domain):
        """Initialize adaptive assessment for user"""
        try:
            assessment_config = {
                'user_id': user_profile.get('user_id'),
                'skill_domain': skill_domain,
                'initial_difficulty': self._estimate_initial_difficulty(user_profile, skill_domain),
                'assessment_strategy': self._select_assessment_strategy(user_profile),
                'question_bank': self._load_question_bank(skill_domain),
                'adaptation_rules': self._load_adaptation_rules(skill_domain),
                'start_time': datetime.now().isoformat()
            }
            
            return {
                'status': 'success',
                'assessment_id': f"assessment_{user_profile.get('user_id')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'config': assessment_config
            }
        except Exception as e:
            print(f"Error initializing assessment: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _estimate_initial_difficulty(self, user_profile, skill_domain):
        """Estimate initial difficulty level for user"""
        try:
            base_difficulty = 0.5  # Medium difficulty
            
            # Adjust based on user skill level
            skill_level = user_profile.get('skill_level', 3)
            if skill_level <= 2:
                base_difficulty -= 0.2
            elif skill_level >= 4:
                base_difficulty += 0.2
            
            # Adjust based on domain familiarity
            domain_experience = user_profile.get('domain_experience', {}).get(skill_domain, 0)
            base_difficulty += (domain_experience - 0.5) * 0.3
            
            return max(0.1, min(1.0, base_difficulty))
        except:
            return 0.5

    def _select_assessment_strategy(self, user_profile):
        """Select optimal assessment strategy based on user profile"""
        try:
            learning_style = user_profile.get('learning_style', 'mixed')
            time_preference = user_profile.get('time_preference', 'standard')
            
            strategy = {
                'type': 'adaptive',
                'style_preference': learning_style,
                'time_limit': self._get_time_limit(time_preference),
                'question_types': self._get_preferred_question_types(learning_style),
                'feedback_frequency': 'immediate' if learning_style == 'interactive' else 'deferred'
            }
            
            return strategy
        except:
            return {'type': 'standard', 'style_preference': 'mixed'}

    def _get_time_limit(self, time_preference):
        """Get time limit based on user preference"""
        time_limits = {
            'quick': 30,      # 30 minutes
            'standard': 60,   # 1 hour
            'extended': 120   # 2 hours
        }
        return time_limits.get(time_preference, 60)

    def _get_preferred_question_types(self, learning_style):
        """Get preferred question types based on learning style"""
        preferences = {
            'visual': ['diagram', 'image_based', 'flowchart'],
            'textual': ['multiple_choice', 'short_answer', 'essay'],
            'interactive': ['simulation', 'practical', 'hands_on'],
            'mixed': ['multiple_choice', 'short_answer', 'practical']
        }
        return preferences.get(learning_style, ['multiple_choice', 'short_answer'])

    def _load_question_bank(self, skill_domain):
        """Load question bank for skill domain"""
        try:
            # This would typically load from database
            # For now, return sample structure
            return {
                'total_questions': 100,
                'by_difficulty': {
                    'easy': 30,
                    'medium': 50,
                    'hard': 20
                },
                'by_type': {
                    'multiple_choice': 40,
                    'short_answer': 30,
                    'practical': 20,
                    'essay': 10
                },
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0'
                }
            }
        except:
            return {'total_questions': 0, 'by_difficulty': {}, 'by_type': {}}

    def _load_adaptation_rules(self, skill_domain):
        """Load adaptation rules for skill domain"""
        try:
            return {
                'difficulty_adjustment': {
                    'correct_answer_threshold': 0.8,
                    'incorrect_answer_threshold': 0.4,
                    'adjustment_factor': 0.1
                },
                'time_adaptation': {
                    'fast_response_threshold': 0.5,  # Relative to average
                    'slow_response_threshold': 2.0,
                    'time_adjustment_factor': 0.2
                },
                'content_adaptation': {
                    'skip_mastery_threshold': 0.9,
                    'remediation_threshold': 0.5,
                    'review_threshold': 0.7
                }
            }
        except:
            return {}

    def select_next_question(self, assessment_state, user_responses):
        """Select next question using adaptive algorithms"""
        try:
            current_difficulty = assessment_state.get('current_difficulty', 0.5)
            user_ability = self._estimate_user_ability(user_responses)
            
            # Item Response Theory based selection
            optimal_difficulty = self._calculate_optimal_difficulty(user_ability, current_difficulty)
            
            # Reinforcement Learning based selection
            rl_recommendation = self._rl_question_selection(assessment_state, user_responses)
            
            # Bayesian Network based selection
            bayesian_recommendation = self._bayesian_question_selection(assessment_state, user_responses)
            
            # Combine recommendations
            final_difficulty = self._combine_recommendations(
                optimal_difficulty, rl_recommendation, bayesian_recommendation
            )
            
            # Select question from bank
            selected_question = self._select_question_by_difficulty(
                assessment_state['question_bank'], final_difficulty, user_responses
            )
            
            return {
                'status': 'success',
                'question': selected_question,
                'difficulty': final_difficulty,
                'selection_method': 'adaptive_combined',
                'confidence': self._calculate_selection_confidence(user_responses)
            }
        except Exception as e:
            print(f"Error selecting next question: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _estimate_user_ability(self, user_responses):
        """Estimate user ability level from responses"""
        try:
            if not user_responses:
                return 0.5
            
            # Calculate weighted average of performance
            total_weight = 0
            weighted_score = 0
            
            for response in user_responses:
                difficulty = response.get('difficulty', 0.5)
                is_correct = response.get('is_correct', False)
                response_time = response.get('response_time', 1)
                
                # Weight by difficulty and response time
                weight = difficulty * (1 / max(0.1, response_time))
                score = 1.0 if is_correct else 0.0
                
                weighted_score += weight * score
                total_weight += weight
            
            if total_weight == 0:
                return 0.5
            
            estimated_ability = weighted_score / total_weight
            return max(0.1, min(1.0, estimated_ability))
        except:
            return 0.5

    def _calculate_optimal_difficulty(self, user_ability, current_difficulty):
        """Calculate optimal difficulty using Item Response Theory"""
        try:
            # Fisher Information maximization
            # Optimal difficulty is where information is maximized
            # This occurs when difficulty matches user ability
            
            alpha = 0.7  # Learning rate for difficulty adjustment
            optimal_difficulty = alpha * user_ability + (1 - alpha) * current_difficulty
            
            return max(0.1, min(1.0, optimal_difficulty))
        except:
            return current_difficulty

    def _rl_question_selection(self, assessment_state, user_responses):
        """Select question using Reinforcement Learning"""
        try:
            # State representation
            state = self._encode_state(assessment_state, user_responses)
            
            # Q-learning action selection
            if np.random.random() < self.epsilon:
                # Exploration: random difficulty
                action = np.random.uniform(0.1, 1.0)
            else:
                # Exploitation: best known action
                action = self._get_best_action(state)
            
            return action
        except:
            return 0.5

    def _encode_state(self, assessment_state, user_responses):
        """Encode current state for RL"""
        try:
            state_features = [
                assessment_state.get('current_difficulty', 0.5),
                len(user_responses),
                self._estimate_user_ability(user_responses),
                assessment_state.get('time_elapsed', 0) / assessment_state.get('time_limit', 60),
                assessment_state.get('correct_answers', 0) / max(1, len(user_responses))
            ]
            
            return tuple(state_features)
        except:
            return (0.5, 0, 0.5, 0.5, 0.5)

    def _get_best_action(self, state):
        """Get best action from Q-table"""
        try:
            if state not in self.q_table:
                return 0.5  # Default action
            
            q_values = self.q_table[state]
            return max(q_values.keys(), key=lambda k: q_values[k])
        except:
            return 0.5

    def _bayesian_question_selection(self, assessment_state, user_responses):
        """Select question using Bayesian Networks"""
        try:
            # Simple Bayesian inference
            # P(skill|responses) ∝ P(responses|skill) * P(skill)
            
            prior_skill = self._estimate_user_ability(user_responses)
            
            # Likelihood based on recent responses
            recent_responses = user_responses[-5:] if len(user_responses) >= 5 else user_responses
            if recent_responses:
                correct_rate = sum(1 for r in recent_responses if r.get('is_correct', False)) / len(recent_responses)
                likelihood = correct_rate
            else:
                likelihood = 0.5
            
            # Posterior
            posterior = (likelihood * prior_skill) / max(0.01, likelihood * prior_skill + (1 - likelihood) * (1 - prior_skill))
            
            return posterior
        except:
            return 0.5

    def _combine_recommendations(self, irt_rec, rl_rec, bayesian_rec):
        """Combine recommendations from different methods"""
        try:
            # Weighted combination
            weights = {'irt': 0.4, 'rl': 0.3, 'bayesian': 0.3}
            
            combined = (
                weights['irt'] * irt_rec +
                weights['rl'] * rl_rec +
                weights['bayesian'] * bayesian_rec
            )
            
            return max(0.1, min(1.0, combined))
        except:
            return 0.5

    def _select_question_by_difficulty(self, question_bank, difficulty, user_responses):
        """Select question with specified difficulty"""
        try:
            # This would typically query database
            # For now, return sample question structure
            
            question_types = ['multiple_choice', 'short_answer', 'practical']
            selected_type = np.random.choice(question_types)
            
            return {
                'id': f"q_{len(user_responses) + 1}",
                'type': selected_type,
                'difficulty': difficulty,
                'content': f"Sample {selected_type} question with difficulty {difficulty:.2f}",
                'options': ['Option A', 'Option B', 'Option C', 'Option D'] if selected_type == 'multiple_choice' else None,
                'correct_answer': 'A' if selected_type == 'multiple_choice' else 'Sample answer',
                'time_limit': 60 if selected_type == 'multiple_choice' else 120,
                'points': int(10 * difficulty)
            }
        except:
            return {}

    def _calculate_selection_confidence(self, user_responses):
        """Calculate confidence in question selection"""
        try:
            if len(user_responses) < 3:
                return 0.5
            
            # Confidence increases with more responses
            base_confidence = 0.3
            response_factor = min(0.5, len(user_responses) * 0.05)
            
            return min(1.0, base_confidence + response_factor)
        except:
            return 0.5

    def process_response(self, assessment_state, question, user_response):
        """Process user response and update assessment state"""
        try:
            # Evaluate response
            evaluation = self._evaluate_response(question, user_response)
            
            # Update assessment state
            updated_state = self._update_assessment_state(assessment_state, question, evaluation)
            
            # Update learning models
            self._update_learning_models(assessment_state, question, evaluation)
            
            # Generate feedback
            feedback = self._generate_feedback(question, evaluation, updated_state)
            
            return {
                'status': 'success',
                'evaluation': evaluation,
                'updated_state': updated_state,
                'feedback': feedback,
                'next_recommendation': self._get_next_recommendation(updated_state)
            }
        except Exception as e:
            print(f"Error processing response: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _evaluate_response(self, question, user_response):
        """Evaluate user response"""
        try:
            response_time = user_response.get('response_time', 0)
            user_answer = user_response.get('answer', '')
            correct_answer = question.get('correct_answer', '')
            
            # Correctness
            is_correct = self._check_correctness(user_answer, correct_answer, question.get('type', 'multiple_choice'))
            
            # Time efficiency
            expected_time = question.get('time_limit', 60)
            time_efficiency = min(1.0, expected_time / max(1, response_time))
            
            # Confidence score
            confidence = user_response.get('confidence', 0.5)
            
            # Overall score
            score = 0.0
            if is_correct:
                score = 0.7 + 0.2 * time_efficiency + 0.1 * confidence
            else:
                score = 0.1 * (1 - time_efficiency) + 0.1 * confidence
            
            return {
                'is_correct': is_correct,
                'score': max(0.0, min(1.0, score)),
                'response_time': response_time,
                'time_efficiency': time_efficiency,
                'confidence': confidence,
                'feedback_type': 'positive' if is_correct else 'constructive'
            }
        except Exception as e:
            print(f"Error evaluating response: {str(e)}")
            return {'is_correct': False, 'score': 0.0}

    def _check_correctness(self, user_answer, correct_answer, question_type):
        """Check if answer is correct"""
        try:
            if question_type == 'multiple_choice':
                return user_answer.strip().upper() == correct_answer.strip().upper()
            elif question_type == 'short_answer':
                # Simple string matching (could be enhanced with NLP)
                return user_answer.strip().lower() == correct_answer.strip().lower()
            elif question_type == 'practical':
                # Would involve more complex evaluation
                return user_answer.strip().lower() in correct_answer.strip().lower().split(',')
            else:
                return False
        except:
            return False

    def _update_assessment_state(self, assessment_state, question, evaluation):
        """Update assessment state based on response evaluation"""
        try:
            updated_state = assessment_state.copy()
            
            # Update response history
            if 'responses' not in updated_state:
                updated_state['responses'] = []
            
            updated_state['responses'].append({
                'question_id': question.get('id'),
                'difficulty': question.get('difficulty'),
                'evaluation': evaluation,
                'timestamp': datetime.now().isoformat()
            })
            
            # Update statistics
            updated_state['total_responses'] = len(updated_state['responses'])
            updated_state['correct_answers'] = sum(1 for r in updated_state['responses'] if r['evaluation']['is_correct'])
            updated_state['average_score'] = sum(r['evaluation']['score'] for r in updated_state['responses']) / len(updated_state['responses'])
            
            # Update difficulty based on performance
            current_difficulty = updated_state.get('current_difficulty', 0.5)
            if evaluation['is_correct']:
                # Increase difficulty if performing well
                updated_state['current_difficulty'] = min(1.0, current_difficulty + 0.05)
            else:
                # Decrease difficulty if struggling
                updated_state['current_difficulty'] = max(0.1, current_difficulty - 0.05)
            
            # Update time
            if 'time_elapsed' not in updated_state:
                updated_state['time_elapsed'] = 0
            updated_state['time_elapsed'] += evaluation.get('response_time', 0)
            
            return updated_state
        except Exception as e:
            print(f"Error updating assessment state: {str(e)}")
            return assessment_state

    def _update_learning_models(self, assessment_state, question, evaluation):
        """Update learning models with new data"""
        try:
            # Update Q-table for reinforcement learning
            state = self._encode_state(assessment_state, assessment_state.get('responses', []))
            action = question.get('difficulty', 0.5)
            reward = evaluation['score']
            
            if state not in self.q_table:
                self.q_table[state] = {}
            
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0.0
            
            # Q-learning update
            old_value = self.q_table[state][action]
            next_max = max(self.q_table[state].values()) if self.q_table[state] else 0.0
            new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
            self.q_table[state][action] = new_value
            
        except Exception as e:
            print(f"Error updating learning models: {str(e)}")

    def _generate_feedback(self, question, evaluation, updated_state):
        """Generate personalized feedback"""
        try:
            feedback = {
                'type': evaluation['feedback_type'],
                'message': self._create_feedback_message(question, evaluation),
                'suggestions': self._generate_suggestions(question, evaluation, updated_state),
                'next_steps': self._suggest_next_steps(updated_state)
            }
            
            return feedback
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return {'type': 'neutral', 'message': 'Response processed.'}

    def _create_feedback_message(self, question, evaluation):
        """Create feedback message"""
        try:
            if evaluation['is_correct']:
                if evaluation['time_efficiency'] > 0.8:
                    return "Excellent! You answered correctly and quickly."
                else:
                    return "Good job! You answered correctly."
            else:
                if evaluation['confidence'] > 0.7:
                    return "Not quite right. You seemed confident, but let's review this concept."
                else:
                    return "That's not correct. Let's work through this together."
        except:
            return "Response processed."

    def _generate_suggestions(self, question, evaluation, updated_state):
        """Generate learning suggestions"""
        try:
            suggestions = []
            
            if not evaluation['is_correct']:
                suggestions.append("Review the fundamental concepts related to this question.")
                suggestions.append("Try similar questions with lower difficulty first.")
            
            if evaluation['time_efficiency'] < 0.5:
                suggestions.append("Practice with time management techniques.")
            
            if evaluation['confidence'] < 0.5 and evaluation['is_correct']:
                suggestions.append("Build confidence in this area with more practice.")
            
            return suggestions
        except:
            return []

    def _suggest_next_steps(self, updated_state):
        """Suggest next learning steps"""
        try:
            performance = updated_state.get('average_score', 0.5)
            
            if performance > 0.8:
                return "You're doing great! Ready for more challenging questions."
            elif performance > 0.6:
                return "Good progress! Continue with current difficulty level."
            elif performance > 0.4:
                return "Focus on fundamentals before advancing."
            else:
                return "Let's start with basic concepts and build up gradually."
        except:
            return "Continue with the assessment."

    def _get_next_recommendation(self, updated_state):
        """Get recommendation for next action"""
        try:
            total_responses = updated_state.get('total_responses', 0)
            time_elapsed = updated_state.get('time_elapsed', 0)
            time_limit = updated_state.get('time_limit', 60)
            
            if time_elapsed >= time_limit:
                return {'action': 'complete', 'reason': 'Time limit reached'}
            elif total_responses >= 20:  # Maximum questions
                return {'action': 'complete', 'reason': 'Maximum questions reached'}
            elif updated_state.get('average_score', 0) > 0.9 and total_responses >= 10:
                return {'action': 'complete', 'reason': 'Mastery demonstrated'}
            else:
                return {'action': 'continue', 'reason': 'Assessment in progress'}
        except:
            return {'action': 'continue', 'reason': 'Continue assessment'}

    def generate_assessment_report(self, assessment_state):
        """Generate comprehensive assessment report"""
        try:
            responses = assessment_state.get('responses', [])
            
            if not responses:
                return {'status': 'error', 'message': 'No responses to analyze'}
            
            # Calculate metrics
            metrics = self._calculate_assessment_metrics(responses)
            
            # Skill analysis
            skill_analysis = self._analyze_skill_performance(responses)
            
            # Learning recommendations
            recommendations = self._generate_learning_recommendations(metrics, skill_analysis)
            
            # Predict future performance
            performance_prediction = self._predict_performance(responses)
            
            report = {
                'assessment_id': assessment_state.get('assessment_id'),
                'user_id': assessment_state.get('user_id'),
                'completion_time': assessment_state.get('time_elapsed', 0),
                'total_questions': len(responses),
                'metrics': metrics,
                'skill_analysis': skill_analysis,
                'recommendations': recommendations,
                'performance_prediction': performance_prediction,
                'generated_at': datetime.now().isoformat()
            }
            
            return {
                'status': 'success',
                'report': report
            }
        except Exception as e:
            print(f"Error generating assessment report: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _calculate_assessment_metrics(self, responses):
        """Calculate assessment performance metrics"""
        try:
            total_responses = len(responses)
            correct_responses = sum(1 for r in responses if r['evaluation']['is_correct'])
            
            metrics = {
                'accuracy': correct_responses / total_responses,
                'average_score': sum(r['evaluation']['score'] for r in responses) / total_responses,
                'average_response_time': sum(r['evaluation']['response_time'] for r in responses) / total_responses,
                'average_confidence': sum(r['evaluation']['confidence'] for r in responses) / total_responses,
                'difficulty_progression': [r['difficulty'] for r in responses],
                'score_progression': [r['evaluation']['score'] for r in responses],
                'time_efficiency': sum(r['evaluation']['time_efficiency'] for r in responses) / total_responses
            }
            
            # Additional metrics
            metrics['improvement_rate'] = self._calculate_improvement_rate(responses)
            metrics['consistency'] = self._calculate_consistency(responses)
            metrics['mastery_level'] = self._determine_mastery_level(metrics['accuracy'])
            
            return metrics
        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return {}

    def _calculate_improvement_rate(self, responses):
        """Calculate improvement rate over time"""
        try:
            if len(responses) < 3:
                return 0.0
            
            scores = [r['evaluation']['score'] for r in responses]
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            return second_avg - first_avg
        except:
            return 0.0

    def _calculate_consistency(self, responses):
        """Calculate response consistency"""
        try:
            scores = [r['evaluation']['score'] for r in responses]
            if len(scores) < 2:
                return 1.0
            
            # Lower variance means higher consistency
            variance = np.var(scores)
            max_variance = 0.25  # Maximum possible variance for scores 0-1
            
            consistency = 1 - (variance / max_variance)
            return max(0.0, min(1.0, consistency))
        except:
            return 0.5

    def _determine_mastery_level(self, accuracy):
        """Determine mastery level based on accuracy"""
        if accuracy >= 0.9:
            return 'Expert'
        elif accuracy >= 0.8:
            return 'Advanced'
        elif accuracy >= 0.7:
            return 'Proficient'
        elif accuracy >= 0.6:
            return 'Developing'
        elif accuracy >= 0.5:
            return 'Basic'
        else:
            return 'Novice'

    def _analyze_skill_performance(self, responses):
        """Analyze performance across different skills"""
        try:
            # Group responses by skill/difficulty
            by_difficulty = {}
            for response in responses:
                difficulty = response.get('difficulty', 0.5)
                if difficulty not in by_difficulty:
                    by_difficulty[difficulty] = []
                by_difficulty[difficulty].append(response['evaluation']['score'])
            
            # Calculate performance by difficulty
            performance_by_difficulty = {}
            for difficulty, scores in by_difficulty.items():
                performance_by_difficulty[difficulty] = {
                    'average_score': sum(scores) / len(scores),
                    'count': len(scores),
                    'performance_level': self._determine_mastery_level(sum(scores) / len(scores))
                }
            
            return {
                'performance_by_difficulty': performance_by_difficulty,
                'strengths': self._identify_strengths(performance_by_difficulty),
                'weaknesses': self._identify_weaknesses(performance_by_difficulty)
            }
        except Exception as e:
            print(f"Error analyzing skill performance: {str(e)}")
            return {}

    def _identify_strengths(self, performance_by_difficulty):
        """Identify areas of strength"""
        try:
            strengths = []
            for difficulty, performance in performance_by_difficulty.items():
                if performance['average_score'] > 0.8:
                    strengths.append({
                        'difficulty_level': difficulty,
                        'performance': performance['average_score'],
                        'description': f"Strong performance at difficulty {difficulty:.2f}"
                    })
            return strengths
        except:
            return []

    def _identify_weaknesses(self, performance_by_difficulty):
        """Identify areas needing improvement"""
        try:
            weaknesses = []
            for difficulty, performance in performance_by_difficulty.items():
                if performance['average_score'] < 0.6:
                    weaknesses.append({
                        'difficulty_level': difficulty,
                        'performance': performance['average_score'],
                        'description': f"Needs improvement at difficulty {difficulty:.2f}"
                    })
            return weaknesses
        except:
            return []

    def _generate_learning_recommendations(self, metrics, skill_analysis):
        """Generate personalized learning recommendations"""
        try:
            recommendations = []
            
            # Performance-based recommendations
            accuracy = metrics.get('accuracy', 0.5)
            if accuracy < 0.6:
                recommendations.append({
                    'type': 'foundational',
                    'priority': 'high',
                    'title': 'Focus on Fundamentals',
                    'description': 'Start with basic concepts and build a strong foundation.'
                })
            elif accuracy < 0.8:
                recommendations.append({
                    'type': 'practice',
                    'priority': 'medium',
                    'title': 'Increase Practice',
                    'description': 'Regular practice will help improve your performance.'
                })
            
            # Time-based recommendations
            if metrics.get('time_efficiency', 0.5) < 0.6:
                recommendations.append({
                    'type': 'time_management',
                    'priority': 'medium',
                    'title': 'Improve Time Management',
                    'description': 'Practice answering questions more efficiently.'
                })
            
            # Confidence-based recommendations
            if metrics.get('average_confidence', 0.5) < 0.6:
                recommendations.append({
                    'type': 'confidence_building',
                    'priority': 'low',
                    'title': 'Build Confidence',
                    'description': 'Start with easier questions to build confidence.'
                })
            
            return recommendations
        except:
            return []

    def _predict_performance(self, responses):
        """Predict future performance"""
        try:
            if len(responses) < 5:
                return {'prediction': 'insufficient_data', 'confidence': 0.0}
            
            # Simple trend analysis
            scores = [r['evaluation']['score'] for r in responses]
            recent_scores = scores[-5:]
            
            trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            
            if trend > 0.05:
                prediction = 'improving'
            elif trend < -0.05:
                prediction = 'declining'
            else:
                prediction = 'stable'
            
            # Confidence in prediction
            confidence = min(1.0, len(responses) / 20)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'trend_slope': trend,
                'predicted_next_score': max(0, min(1, recent_scores[-1] + trend))
            }
        except:
            return {'prediction': 'unknown', 'confidence': 0.0}

    def save_model(self, filepath):
        """Save trained models"""
        try:
            model_data = {
                'scaler': self.scaler,
                'difficulty_predictor': self.difficulty_predictor,
                'skill_classifier': self.skill_classifier,
                'bayesian_classifier': self.bayesian_classifier,
                'decision_tree': self.decision_tree,
                'neural_network': self.neural_network,
                'q_table': self.q_table,
                'irt_parameters': self.irt_parameters,
                'is_trained': self.is_trained
            }
            
            joblib.dump(model_data, filepath)
            return {'status': 'success', 'message': f'Model saved to {filepath}'}
        except Exception as e:
            print(f"Error saving model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def load_model(self, filepath):
        """Load trained models"""
        try:
            model_data = joblib.load(filepath)
            
            self.scaler = model_data['scaler']
            self.difficulty_predictor = model_data['difficulty_predictor']
            self.skill_classifier = model_data['skill_classifier']
            self.bayesian_classifier = model_data['bayesian_classifier']
            self.decision_tree = model_data['decision_tree']
            self.neural_network = model_data['neural_network']
            self.q_table = model_data['q_table']
            self.irt_parameters = model_data['irt_parameters']
            self.is_trained = model_data['is_trained']
            
            return {'status': 'success', 'message': f'Model loaded from {filepath}'}
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the adaptive assessment system
    assessment_system = AdaptiveAssessmentSystem()
    
    # Sample user profile
    sample_user_profile = {
        'user_id': 123,
        'skill_level': 3,
        'learning_style': 'visual',
        'time_preference': 'standard',
        'domain_experience': {'technical': 0.6, 'analytical': 0.4}
    }
    
    # Initialize assessment
    init_result = assessment_system.initialize_assessment(sample_user_profile, 'technical')
    print("Assessment Initialization:", json.dumps(init_result, indent=2))
    
    # Sample assessment state
    assessment_state = init_result.get('config', {})
    
    # Select first question
    question_result = assessment_system.select_next_question(assessment_state, [])
    print("Question Selection:", json.dumps(question_result, indent=2))
    
    # Process sample response
    if question_result.get('status') == 'success':
        sample_response = {
            'answer': 'A',
            'response_time': 45,
            'confidence': 0.8
        }
        
        response_result = assessment_system.process_response(
            assessment_state, question_result['question'], sample_response
        )
        print("Response Processing:", json.dumps(response_result, indent=2))
