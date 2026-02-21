"""
Competency Matrix Assessment and Mapping System
Provides comprehensive competency evaluation, skill mapping, and gap analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
import matplotlib.pyplot as plt
import seaborn as sns

class CompetencyMatrix:
    """
    Advanced Competency Assessment and Mapping System
    Features: Multi-dimensional competency evaluation, Skill gap analysis,
             Role-based competency mapping, Progress tracking
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.competency_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.gap_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.skill_clusterer = KMeans(n_clusters=5, random_state=42)
        
        # Competency framework
        self.competency_framework = {}
        self.skill_categories = {}
        self.role_competencies = {}
        
        # Assessment data
        self.user_assessments = {}
        self.competency_scores = {}
        self.gap_analysis = {}
        
        # Competency levels
        self.competency_levels = {
            'novice': 1,
            'beginner': 2,
            'intermediate': 3,
            'advanced': 4,
            'expert': 5,
            'master': 6
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def initialize_competency_framework(self, framework_data: Dict) -> None:
        """Initialize the competency framework"""
        try:
            self.logger.info("Initializing competency framework...")
            
            # Load competency categories
            self.skill_categories = framework_data.get('categories', {
                'technical': ['Programming', 'Data Analysis', 'System Design', 'Cloud Computing'],
                'soft_skills': ['Communication', 'Leadership', 'Teamwork', 'Problem Solving'],
                'business': ['Project Management', 'Strategic Thinking', 'Financial Analysis', 'Marketing'],
                'domain': ['Industry Knowledge', 'Regulatory Compliance', 'Best Practices']
            })
            
            # Load competency definitions
            self.competency_framework = framework_data.get('competencies', {})
            
            # Load role-based competency requirements
            self.role_competencies = framework_data.get('role_requirements', {})
            
            self.logger.info(f"Framework initialized with {len(self.competency_framework)} competencies")
            
        except Exception as e:
            self.logger.error(f"Error initializing competency framework: {str(e)}")
            raise

    def assess_user_competencies(self, user_id: str, assessment_data: Dict) -> Dict:
        """Comprehensive competency assessment for user"""
        try:
            assessment = {
                'user_id': user_id,
                'assessment_date': datetime.now().isoformat(),
                'assessment_type': assessment_data.get('type', 'comprehensive'),
                'competency_scores': {},
                'skill_evidence': assessment_data.get('evidence', {}),
                'self_assessment': assessment_data.get('self_assessment', {}),
                'peer_feedback': assessment_data.get('peer_feedback', {}),
                'performance_data': assessment_data.get('performance_metrics', {})
            }
            
            # Calculate competency scores
            for category, skills in self.skill_categories.items():
                category_scores = {}
                for skill in skills:
                    score = self._calculate_competency_score(skill, assessment_data)
                    category_scores[skill] = score
                
                assessment['competency_scores'][category] = category_scores
            
            # Calculate overall competency level
            assessment['overall_level'] = self._calculate_overall_level(assessment['competency_scores'])
            
            # Store assessment
            self.user_assessments[user_id] = assessment
            self.competency_scores[user_id] = assessment['competency_scores']
            
            return assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing user competencies: {str(e)}")
            return {}

    def _calculate_competency_score(self, skill: str, assessment_data: Dict) -> Dict:
        """Calculate competency score for a specific skill"""
        try:
            # Gather evidence from different sources
            self_assessment = assessment_data.get('self_assessment', {}).get(skill, 0)
            peer_feedback = assessment_data.get('peer_feedback', {}).get(skill, 0)
            performance_metrics = assessment_data.get('performance_metrics', {}).get(skill, 0)
            
            # Weight different sources
            weights = {
                'self_assessment': 0.3,
                'peer_feedback': 0.3,
                'performance': 0.4
            }
            
            # Calculate weighted score
            weighted_score = (
                self_assessment * weights['self_assessment'] +
                peer_feedback * weights['peer_feedback'] +
                performance_metrics * weights['performance']
            )
            
            # Convert to competency level
            competency_level = self._score_to_level(weighted_score)
            
            # Add confidence score
            confidence = self._calculate_confidence_score(assessment_data, skill)
            
            return {
                'score': round(weighted_score, 2),
                'level': competency_level,
                'confidence': confidence,
                'evidence_count': len(assessment_data.get('evidence', {}).get(skill, [])),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating competency score for {skill}: {str(e)}")
            return {'score': 0, 'level': 'novice', 'confidence': 0}

    def _score_to_level(self, score: float) -> str:
        """Convert numerical score to competency level"""
        if score >= 5.0:
            return 'master'
        elif score >= 4.0:
            return 'expert'
        elif score >= 3.0:
            return 'advanced'
        elif score >= 2.0:
            return 'intermediate'
        elif score >= 1.0:
            return 'beginner'
        else:
            return 'novice'

    def _calculate_confidence_score(self, assessment_data: Dict, skill: str) -> float:
        """Calculate confidence score for competency assessment"""
        try:
            evidence = assessment_data.get('evidence', {}).get(skill, [])
            peer_count = len(assessment_data.get('peer_feedback', {}).get(skill, []))
            
            # Base confidence on evidence and peer feedback
            base_confidence = min(1.0, (len(evidence) + peer_count) / 10.0)
            
            # Adjust for recency of evidence
            recency_bonus = self._calculate_recency_bonus(evidence)
            
            return min(1.0, base_confidence + recency_bonus)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence score: {str(e)}")
            return 0.5

    def _calculate_recency_bonus(self, evidence: List) -> float:
        """Calculate bonus based on recency of evidence"""
        try:
            if not evidence:
                return 0.0
            
            current_date = datetime.now()
            recent_evidence = 0
            
            for item in evidence:
                if 'date' in item:
                    evidence_date = datetime.fromisoformat(item['date'])
                    days_diff = (current_date - evidence_date).days
                    if days_diff <= 90:  # Evidence from last 3 months
                        recent_evidence += 1
            
            return min(0.3, recent_evidence / len(evidence) * 0.3)
            
        except Exception as e:
            self.logger.error(f"Error calculating recency bonus: {str(e)}")
            return 0.0

    def _calculate_overall_level(self, competency_scores: Dict) -> Dict:
        """Calculate overall competency level"""
        try:
            all_scores = []
            for category_scores in competency_scores.values():
                for skill_data in category_scores.values():
                    if isinstance(skill_data, dict) and 'score' in skill_data:
                        all_scores.append(skill_data['score'])
            
            if not all_scores:
                return {'level': 'novice', 'score': 0, 'confidence': 0}
            
            avg_score = np.mean(all_scores)
            overall_level = self._score_to_level(avg_score)
            
            # Calculate category breakdown
            category_averages = {}
            for category, scores in competency_scores.items():
                cat_scores = [s['score'] for s in scores.values() if isinstance(s, dict) and 'score' in s]
                category_averages[category] = np.mean(cat_scores) if cat_scores else 0
            
            return {
                'level': overall_level,
                'score': round(avg_score, 2),
                'confidence': np.mean([s.get('confidence', 0) for s in all_scores if isinstance(s, dict)]),
                'category_breakdown': category_averages,
                'strengths': self._identify_strengths(category_averages),
                'improvement_areas': self._identify_improvement_areas(category_averages)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating overall level: {str(e)}")
            return {'level': 'novice', 'score': 0, 'confidence': 0}

    def _identify_strengths(self, category_averages: Dict) -> List[str]:
        """Identify user's strength areas"""
        try:
            sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)
            return [cat for cat, score in sorted_categories[:2] if score >= 3.0]
            
        except Exception as e:
            self.logger.error(f"Error identifying strengths: {str(e)}")
            return []

    def _identify_improvement_areas(self, category_averages: Dict) -> List[str]:
        """Identify areas needing improvement"""
        try:
            sorted_categories = sorted(category_averages.items(), key=lambda x: x[1])
            return [cat for cat, score in sorted_categories[:2] if score < 3.0]
            
        except Exception as e:
            self.logger.error(f"Error identifying improvement areas: {str(e)}")
            return []

    def analyze_skill_gaps(self, user_id: str, target_role: str) -> Dict:
        """Analyze skill gaps for target role"""
        try:
            if user_id not in self.competency_scores:
                raise ValueError(f"No competency data found for user {user_id}")
            
            if target_role not in self.role_competencies:
                raise ValueError(f"No competency requirements found for role {target_role}")
            
            current_competencies = self.competency_scores[user_id]
            required_competencies = self.role_competencies[target_role]
            
            gap_analysis = {
                'user_id': user_id,
                'target_role': target_role,
                'analysis_date': datetime.now().isoformat(),
                'overall_readiness': 0,
                'category_gaps': {},
                'skill_gaps': [],
                'strengths': [],
                'development_priorities': [],
                'estimated_timeline': {}
            }
            
            # Analyze category gaps
            for category, required_skills in required_competencies.items():
                category_gap = self._analyze_category_gap(
                    category, current_competencies.get(category, {}), required_skills
                )
                gap_analysis['category_gaps'][category] = category_gap
            
            # Calculate overall readiness
            gap_analysis['overall_readiness'] = self._calculate_role_readiness(gap_analysis['category_gaps'])
            
            # Identify specific skill gaps
            gap_analysis['skill_gaps'] = self._identify_skill_gaps(current_competencies, required_competencies)
            
            # Identify strengths
            gap_analysis['strengths'] = self._identify_role_strengths(current_competencies, required_competencies)
            
            # Set development priorities
            gap_analysis['development_priorities'] = self._prioritize_development(gap_analysis['skill_gaps'])
            
            # Estimate timeline
            gap_analysis['estimated_timeline'] = self._estimate_development_timeline(gap_analysis['skill_gaps'])
            
            # Store gap analysis
            self.gap_analysis[f"{user_id}_{target_role}"] = gap_analysis
            
            return gap_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing skill gaps: {str(e)}")
            return {}

    def _analyze_category_gap(self, category: str, current: Dict, required: Dict) -> Dict:
        """Analyze gap for a specific competency category"""
        try:
            gap_data = {
                'current_level': 0,
                'required_level': 0,
                'gap_size': 0,
                'readiness_percentage': 0,
                'priority': 'medium',
                'skill_gaps': []
            }
            
            # Calculate current and required levels
            current_scores = []
            required_scores = []
            
            for skill, req_data in required.items():
                required_score = req_data.get('level', 3)
                required_scores.append(required_score)
                
                current_score = 0
                if skill in current and isinstance(current[skill], dict):
                    current_score = current[skill].get('score', 0)
                
                current_scores.append(current_score)
                
                # Identify specific skill gaps
                if current_score < required_score:
                    gap_data['skill_gaps'].append({
                        'skill': skill,
                        'current_score': current_score,
                        'required_score': required_score,
                        'gap_size': required_score - current_score
                    })
            
            if current_scores and required_scores:
                gap_data['current_level'] = np.mean(current_scores)
                gap_data['required_level'] = np.mean(required_scores)
                gap_data['gap_size'] = gap_data['required_level'] - gap_data['current_level']
                gap_data['readiness_percentage'] = (gap_data['current_level'] / gap_data['required_level']) * 100
                
                # Set priority based on gap size
                if gap_data['gap_size'] >= 2:
                    gap_data['priority'] = 'high'
                elif gap_data['gap_size'] >= 1:
                    gap_data['priority'] = 'medium'
                else:
                    gap_data['priority'] = 'low'
            
            return gap_data
            
        except Exception as e:
            self.logger.error(f"Error analyzing category gap: {str(e)}")
            return {}

    def _calculate_role_readiness(self, category_gaps: Dict) -> float:
        """Calculate overall readiness for target role"""
        try:
            if not category_gaps:
                return 0.0
            
            readiness_scores = []
            for category_gap in category_gaps.values():
                readiness_scores.append(category_gap.get('readiness_percentage', 0))
            
            return np.mean(readiness_scores)
            
        except Exception as e:
            self.logger.error(f"Error calculating role readiness: {str(e)}")
            return 0.0

    def _identify_skill_gaps(self, current: Dict, required: Dict) -> List[Dict]:
        """Identify specific skill gaps"""
        try:
            skill_gaps = []
            
            for category, required_skills in required.items():
                current_category = current.get(category, {})
                
                for skill, req_data in required_skills.items():
                    required_level = req_data.get('level', 3)
                    
                    current_level = 0
                    if skill in current_category and isinstance(current_category[skill], dict):
                        current_level = current_category[skill].get('score', 0)
                    
                    if current_level < required_level:
                        gap = {
                            'category': category,
                            'skill': skill,
                            'current_level': current_level,
                            'required_level': required_level,
                            'gap_size': required_level - current_level,
                            'priority': self._calculate_gap_priority(required_level - current_level),
                            'development_difficulty': req_data.get('difficulty', 'medium')
                        }
                        skill_gaps.append(gap)
            
            # Sort by gap size (descending)
            skill_gaps.sort(key=lambda x: x['gap_size'], reverse=True)
            return skill_gaps
            
        except Exception as e:
            self.logger.error(f"Error identifying skill gaps: {str(e)}")
            return []

    def _calculate_gap_priority(self, gap_size: float) -> str:
        """Calculate priority based on gap size"""
        if gap_size >= 3:
            return 'critical'
        elif gap_size >= 2:
            return 'high'
        elif gap_size >= 1:
            return 'medium'
        else:
            return 'low'

    def _identify_role_strengths(self, current: Dict, required: Dict) -> List[Dict]:
        """Identify strengths relative to role requirements"""
        try:
            strengths = []
            
            for category, required_skills in required.items():
                current_category = current.get(category, {})
                
                for skill, req_data in required_skills.items():
                    required_level = req_data.get('level', 3)
                    
                    current_level = 0
                    if skill in current_category and isinstance(current_category[skill], dict):
                        current_level = current_category[skill].get('score', 0)
                    
                    if current_level >= required_level:
                        strength = {
                            'category': category,
                            'skill': skill,
                            'current_level': current_level,
                            'required_level': required_level,
                            'strength_level': current_level - required_level
                        }
                        strengths.append(strength)
            
            # Sort by strength level (descending)
            strengths.sort(key=lambda x: x['strength_level'], reverse=True)
            return strengths
            
        except Exception as e:
            self.logger.error(f"Error identifying role strengths: {str(e)}")
            return []

    def _prioritize_development(self, skill_gaps: List[Dict]) -> List[Dict]:
        """Prioritize development areas"""
        try:
            priorities = []
            
            for gap in skill_gaps:
                priority_score = 0
                
                # Base score from gap size
                priority_score += gap['gap_size'] * 2
                
                # Adjust for priority level
                priority_multipliers = {
                    'critical': 3,
                    'high': 2,
                    'medium': 1,
                    'low': 0.5
                }
                priority_score *= priority_multipliers.get(gap['priority'], 1)
                
                # Adjust for development difficulty
                difficulty_multipliers = {
                    'easy': 1.5,
                    'medium': 1.0,
                    'hard': 0.7
                }
                priority_score *= difficulty_multipliers.get(gap['development_difficulty'], 1.0)
                
                gap['development_priority_score'] = priority_score
                priorities.append(gap)
            
            # Sort by priority score (descending)
            priorities.sort(key=lambda x: x['development_priority_score'], reverse=True)
            return priorities[:10]  # Return top 10 priorities
            
        except Exception as e:
            self.logger.error(f"Error prioritizing development: {str(e)}")
            return skill_gaps[:5]

    def _estimate_development_timeline(self, skill_gaps: List[Dict]) -> Dict:
        """Estimate timeline for closing skill gaps"""
        try:
            timeline = {
                'total_weeks': 0,
                'phases': [],
                'milestones': []
            }
            
            if not skill_gaps:
                return timeline
            
            # Estimate time per skill based on gap size and difficulty
            total_weeks = 0
            current_phase = 1
            phase_skills = []
            phase_time = 0
            
            for i, gap in enumerate(skill_gaps):
                # Estimate weeks to close gap
                gap_size = gap['gap_size']
                difficulty = gap['development_difficulty']
                
                # Base time calculation
                base_weeks = gap_size * 4  # 4 weeks per level
                
                # Adjust for difficulty
                difficulty_multipliers = {
                    'easy': 0.7,
                    'medium': 1.0,
                    'hard': 1.5
                }
                skill_weeks = base_weeks * difficulty_multipliers.get(difficulty, 1.0)
                
                total_weeks += skill_weeks
                phase_time += skill_weeks
                phase_skills.append(gap['skill'])
                
                # Create phase (every 3-4 skills or 12 weeks)
                if len(phase_skills) >= 3 or phase_time >= 12:
                    phase = {
                        'phase': current_phase,
                        'skills': phase_skills.copy(),
                        'estimated_weeks': phase_time,
                        'focus': self._get_phase_focus(phase_skills)
                    }
                    timeline['phases'].append(phase)
                    
                    # Create milestone
                    milestone = {
                        'week': int(total_weeks),
                        'title': f"Phase {current_phase} Complete",
                        'skills_mastered': phase_skills.copy()
                    }
                    timeline['milestones'].append(milestone)
                    
                    # Reset for next phase
                    current_phase += 1
                    phase_skills = []
                    phase_time = 0
            
            # Add remaining skills as final phase
            if phase_skills:
                phase = {
                    'phase': current_phase,
                    'skills': phase_skills,
                    'estimated_weeks': phase_time,
                    'focus': self._get_phase_focus(phase_skills)
                }
                timeline['phases'].append(phase)
                
                milestone = {
                    'week': int(total_weeks),
                    'title': f"Phase {current_phase} Complete",
                    'skills_mastered': phase_skills
                }
                timeline['milestones'].append(milestone)
            
            timeline['total_weeks'] = int(total_weeks)
            return timeline
            
        except Exception as e:
            self.logger.error(f"Error estimating development timeline: {str(e)}")
            return {'total_weeks': 12, 'phases': [], 'milestones': []}

    def _get_phase_focus(self, skills: List[str]) -> str:
        """Determine focus area for a development phase"""
        try:
            # Count skills by category
            category_counts = {}
            for skill in skills:
                category = self._get_skill_category(skill)
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # Return category with most skills
            if category_counts:
                return max(category_counts, key=category_counts.get)
            
            return "General Skill Development"
            
        except Exception as e:
            self.logger.error(f"Error getting phase focus: {str(e)}")
            return "Skill Development"

    def _get_skill_category(self, skill: str) -> str:
        """Get category for a skill"""
        try:
            for category, skills in self.skill_categories.items():
                if skill in skills:
                    return category
            
            return 'general'
            
        except Exception as e:
            self.logger.error(f"Error getting skill category: {str(e)}")
            return 'general'

    def create_competency_heatmap(self, user_id: str) -> Dict:
        """Create competency heatmap visualization data"""
        try:
            if user_id not in self.competency_scores:
                return {}
            
            competencies = self.competency_scores[user_id]
            heatmap_data = []
            
            for category, skills in competencies.items():
                for skill, skill_data in skills.items():
                    if isinstance(skill_data, dict):
                        heatmap_data.append({
                            'category': category,
                            'skill': skill,
                            'score': skill_data.get('score', 0),
                            'level': skill_data.get('level', 'novice'),
                            'confidence': skill_data.get('confidence', 0)
                        })
            
            return {
                'user_id': user_id,
                'heatmap_data': heatmap_data,
                'categories': list(self.skill_categories.keys()),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating competency heatmap: {str(e)}")
            return {}

    def compare_competencies(self, user_ids: List[str]) -> Dict:
        """Compare competencies across multiple users"""
        try:
            comparison = {
                'users': user_ids,
                'comparison_date': datetime.now().isoformat(),
                'category_comparisons': {},
                'skill_comparisons': {},
                'overall_rankings': []
            }
            
            # Collect all competency data
            user_competencies = {}
            for user_id in user_ids:
                if user_id in self.competency_scores:
                    user_competencies[user_id] = self.competency_scores[user_id]
            
            # Compare categories
            for category in self.skill_categories.keys():
                category_comparison = {
                    'category': category,
                    'user_scores': {}
                }
                
                for user_id, competencies in user_competencies.items():
                    if category in competencies:
                        scores = [s.get('score', 0) for s in competencies[category].values() if isinstance(s, dict)]
                        category_comparison['user_scores'][user_id] = np.mean(scores) if scores else 0
                
                comparison['category_comparisons'][category] = category_comparison
            
            # Calculate overall rankings
            user_overall_scores = {}
            for user_id, competencies in user_competencies.items():
                all_scores = []
                for category_scores in competencies.values():
                    for skill_data in category_scores.values():
                        if isinstance(skill_data, dict) and 'score' in skill_data:
                            all_scores.append(skill_data['score'])
                
                user_overall_scores[user_id] = np.mean(all_scores) if all_scores else 0
            
            # Sort users by overall score
            ranked_users = sorted(user_overall_scores.items(), key=lambda x: x[1], reverse=True)
            comparison['overall_rankings'] = [
                {'user_id': user_id, 'score': score, 'rank': i + 1}
                for i, (user_id, score) in enumerate(ranked_users)
            ]
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error comparing competencies: {str(e)}")
            return {}

    def generate_development_plan(self, user_id: str, target_role: str) -> Dict:
        """Generate personalized development plan"""
        try:
            gap_key = f"{user_id}_{target_role}"
            if gap_key not in self.gap_analysis:
                return {}
            
            gap_analysis = self.gap_analysis[gap_key]
            
            development_plan = {
                'user_id': user_id,
                'target_role': target_role,
                'plan_date': datetime.now().isoformat(),
                'current_readiness': gap_analysis['overall_readiness'],
                'target_readiness': 85,  # Target 85% readiness
                'development_phases': [],
                'learning_resources': {},
                'assessment_schedule': [],
                'success_metrics': []
            }
            
            # Create development phases based on priorities
            priorities = gap_analysis['development_priorities']
            phases = self._create_development_phases(priorities)
            development_plan['development_phases'] = phases
            
            # Recommend learning resources
            for phase in phases:
                phase_resources = []
                for skill in phase['skills']:
                    resources = self._recommend_learning_resources(skill)
                    phase_resources.extend(resources)
                development_plan['learning_resources'][f"phase_{phase['phase']}"] = phase_resources
            
            # Create assessment schedule
            development_plan['assessment_schedule'] = self._create_assessment_schedule(phases)
            
            # Define success metrics
            development_plan['success_metrics'] = self._define_success_metrics(target_role)
            
            return development_plan
            
        except Exception as e:
            self.logger.error(f"Error generating development plan: {str(e)}")
            return {}

    def _create_development_phases(self, priorities: List[Dict]) -> List[Dict]:
        """Create development phases from priorities"""
        try:
            phases = []
            skills_per_phase = 3
            
            for i in range(0, len(priorities), skills_per_phase):
                phase_skills = priorities[i:i + skills_per_phase]
                phase = {
                    'phase': len(phases) + 1,
                    'skills': [skill['skill'] for skill in phase_skills],
                    'focus_areas': [skill['category'] for skill in phase_skills],
                    'estimated_duration': sum(skill.get('gap_size', 1) * 4 for skill in phase_skills),  # weeks
                    'priority_level': max(skill.get('priority', 'medium') for skill in phase_skills)
                }
                phases.append(phase)
            
            return phases
            
        except Exception as e:
            self.logger.error(f"Error creating development phases: {str(e)}")
            return []

    def _recommend_learning_resources(self, skill: str) -> List[Dict]:
        """Recommend learning resources for skill development"""
        try:
            resources = [
                {
                    'type': 'online_course',
                    'title': f"Complete {skill} Course",
                    'provider': "Online Learning Platform",
                    'duration': "4-6 weeks",
                    'difficulty': "intermediate"
                },
                {
                    'type': 'book',
                    'title': f"{skill}: The Complete Guide",
                    'author': "Industry Expert",
                    'pages': 300,
                    'difficulty': "beginner"
                },
                {
                    'type': 'practice_project',
                    'title': f"{skill} Practical Projects",
                    'description': f"Hands-on projects to master {skill}",
                    'projects': 5,
                    'difficulty': "intermediate"
                }
            ]
            
            return resources
            
        except Exception as e:
            self.logger.error(f"Error recommending learning resources: {str(e)}")
            return []

    def _create_assessment_schedule(self, phases: List[Dict]) -> List[Dict]:
        """Create assessment schedule for development plan"""
        try:
            schedule = []
            week_counter = 0
            
            for phase in phases:
                # Mid-phase assessment
                mid_assessment = {
                    'week': week_counter + phase['estimated_duration'] // 2,
                    'type': 'formative',
                    'skills': phase['skills'],
                    'purpose': 'Check progress and adjust learning approach'
                }
                schedule.append(mid_assessment)
                
                # End-of-phase assessment
                end_assessment = {
                    'week': week_counter + phase['estimated_duration'],
                    'type': 'summative',
                    'skills': phase['skills'],
                    'purpose': 'Evaluate mastery of phase skills'
                }
                schedule.append(end_assessment)
                
                week_counter += phase['estimated_duration']
            
            return schedule
            
        except Exception as e:
            self.logger.error(f"Error creating assessment schedule: {str(e)}")
            return []

    def _define_success_metrics(self, target_role: str) -> List[Dict]:
        """Define success metrics for development plan"""
        try:
            metrics = [
                {
                    'metric': 'Competency Score Improvement',
                    'target': 'Increase average competency score by 2 points',
                    'measurement': 'Pre and post assessment comparison'
                },
                {
                    'metric': 'Role Readiness',
                    'target': 'Achieve 85% role readiness',
                    'measurement': 'Competency gap analysis'
                },
                {
                    'metric': 'Skill Mastery',
                    'target': 'Master 80% of priority skills',
                    'measurement': 'Skill assessment results'
                },
                {
                    'metric': 'Practical Application',
                    'target': 'Complete 3 real-world projects',
                    'measurement': 'Project evaluation and feedback'
                }
            ]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error defining success metrics: {str(e)}")
            return []

    def track_progress(self, user_id: str, progress_data: Dict) -> Dict:
        """Track user progress over time"""
        try:
            progress_entry = {
                'user_id': user_id,
                'date': datetime.now().isoformat(),
                'competency_scores': progress_data.get('competency_scores', {}),
                'skills_improved': progress_data.get('skills_improved', []),
                'skills_mastered': progress_data.get('skills_mastered', []),
                'assessments_completed': progress_data.get('assessments_completed', []),
                'learning_hours': progress_data.get('learning_hours', 0),
                'projects_completed': progress_data.get('projects_completed', [])
            }
            
            # Calculate progress metrics
            if user_id in self.user_assessments:
                previous_scores = self.user_assessments[user_id]['competency_scores']
                progress_metrics = self._calculate_progress_metrics(previous_scores, progress_entry['competency_scores'])
                progress_entry['progress_metrics'] = progress_metrics
            
            return progress_entry
            
        except Exception as e:
            self.logger.error(f"Error tracking progress: {str(e)}")
            return {}

    def _calculate_progress_metrics(self, previous_scores: Dict, current_scores: Dict) -> Dict:
        """Calculate progress metrics between assessments"""
        try:
            metrics = {
                'overall_improvement': 0,
                'category_improvements': {},
                'skills_improved': [],
                'skills_declined': [],
                'new_skills': []
            }
            
            # Calculate overall improvement
            previous_total = 0
            current_total = 0
            skill_count = 0
            
            for category in current_scores:
                if category in previous_scores:
                    for skill, current_data in current_scores[category].items():
                        if isinstance(current_data, dict) and 'score' in current_data:
                            current_score = current_data['score']
                            current_total += current_score
                            
                            if skill in previous_scores[category]:
                                previous_data = previous_scores[category][skill]
                                if isinstance(previous_data, dict) and 'score' in previous_data:
                                    previous_score = previous_data['score']
                                    previous_total += previous_score
                                    
                                    # Track improvement/decline
                                    if current_score > previous_score:
                                        metrics['skills_improved'].append({
                                            'skill': skill,
                                            'improvement': current_score - previous_score
                                        })
                                    elif current_score < previous_score:
                                        metrics['skills_declined'].append({
                                            'skill': skill,
                                            'decline': previous_score - current_score
                                        })
                            else:
                                # New skill
                                metrics['new_skills'].append(skill)
                            
                            skill_count += 1
            
            if skill_count > 0:
                metrics['overall_improvement'] = (current_total - previous_total) / skill_count
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating progress metrics: {str(e)}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Initialize competency matrix
    cm = CompetencyMatrix()
    
    # Example framework data
    framework_data = {
        'categories': {
            'technical': ['Python', 'Data Analysis', 'Machine Learning', 'Cloud Computing'],
            'soft_skills': ['Communication', 'Leadership', 'Teamwork', 'Problem Solving'],
            'business': ['Project Management', 'Strategic Thinking', 'Financial Analysis']
        },
        'role_requirements': {
            'Data Scientist': {
                'technical': {
                    'Python': {'level': 4, 'difficulty': 'medium'},
                    'Data Analysis': {'level': 4, 'difficulty': 'medium'},
                    'Machine Learning': {'level': 3, 'difficulty': 'hard'}
                },
                'soft_skills': {
                    'Communication': {'level': 3, 'difficulty': 'medium'},
                    'Problem Solving': {'level': 4, 'difficulty': 'medium'}
                },
                'business': {
                    'Project Management': {'level': 2, 'difficulty': 'easy'}
                }
            }
        }
    }
    
    # Initialize framework
    cm.initialize_competency_framework(framework_data)
    
    # Example assessment data
    assessment_data = {
        'self_assessment': {
            'Python': 3.5,
            'Data Analysis': 3.0,
            'Machine Learning': 2.0,
            'Communication': 3.5,
            'Problem Solving': 4.0
        },
        'peer_feedback': {
            'Python': 3.0,
            'Data Analysis': 3.5,
            'Communication': 4.0
        },
        'performance_metrics': {
            'Python': 4.0,
            'Problem Solving': 3.5
        }
    }
    
    # Assess user competencies
    assessment = cm.assess_user_competencies('user123', assessment_data)
    print("Competency assessment completed for user:", assessment['user_id'])
    print("Overall level:", assessment['overall_level']['level'])
    
    # Analyze skill gaps for target role
    gap_analysis = cm.analyze_skill_gaps('user123', 'Data Scientist')
    print("Skill gap analysis completed")
    print("Overall readiness:", gap_analysis['overall_readiness'])
    print("Skill gaps identified:", len(gap_analysis['skill_gaps']))
    
    # Generate development plan
    development_plan = cm.generate_development_plan('user123', 'Data Scientist')
    print("Development plan generated")
    print("Development phases:", len(development_plan['development_phases']))
