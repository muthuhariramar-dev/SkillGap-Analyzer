"""
Personalized Learning Path Generation Model
Uses ML to create adaptive learning paths based on user skills, goals, and learning preferences
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import networkx as nx
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from .google_api import GoogleSearchAPI

class LearningPathGenerator:
    """
    Advanced Learning Path Generation System
    Features: Skill dependency mapping, Personalized recommendations, 
             Progress tracking, Adaptive difficulty adjustment
    """
    
    def __init__(self, google_api_key=None, google_cse_id=None):
        self.scaler = StandardScaler()
        self.path_recommender = RandomForestRegressor(n_estimators=100, random_state=42)
        self.difficulty_predictor = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.learning_style_classifier = KMeans(n_clusters=3, random_state=42)
        
        # Learning path graph
        self.skill_graph = nx.DiGraph()
        self.learning_paths = {}
        
        # Learning parameters
        self.learning_rates = {}
        self.difficulty_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        self.content_types = ['video', 'article', 'practice', 'project', 'quiz']
        
        # User profiles
        self.user_profiles = {}
        self.progress_tracking = {}
        
        # Google API integration
        self.google_api = None
        if google_api_key and google_cse_id:
            self.google_api = GoogleSearchAPI(google_api_key, google_cse_id)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def initialize_skill_graph(self, skills_data: Dict) -> None:
        """Initialize skill dependency graph"""
        try:
            self.logger.info("Initializing skill dependency graph...")
            
            # Add nodes (skills)
            for skill, data in skills_data.items():
                self.skill_graph.add_node(
                    skill,
                    difficulty=data.get('difficulty', 1),
                    category=data.get('category', 'general'),
                    estimated_time=data.get('estimated_time', 60),
                    prerequisites=data.get('prerequisites', [])
                )
            
            # Add edges (dependencies)
            for skill, data in skills_data.items():
                for prereq in data.get('prerequisites', []):
                    if prereq in self.skill_graph.nodes:
                        self.skill_graph.add_edge(prereq, skill)
            
            self.logger.info(f"Skill graph created with {len(self.skill_graph.nodes)} nodes and {len(self.skill_graph.edges)} edges")
            
        except Exception as e:
            self.logger.error(f"Error initializing skill graph: {str(e)}")
            raise

    def create_user_profile(self, user_id: str, user_data: Dict) -> Dict:
        """Create personalized user learning profile"""
        try:
            profile = {
                'user_id': user_id,
                'current_skills': user_data.get('current_skills', {}),
                'learning_goals': user_data.get('learning_goals', []),
                'learning_style': self._analyze_learning_style(user_data),
                'time_availability': user_data.get('time_availability', 5),  # hours per week
                'preferred_content_types': user_data.get('preferred_content', self.content_types),
                'skill_gaps': user_data.get('skill_gaps', {}),
                'created_at': datetime.now().isoformat()
            }
            
            self.user_profiles[user_id] = profile
            return profile
            
        except Exception as e:
            self.logger.error(f"Error creating user profile: {str(e)}")
            return {}

    def _analyze_learning_style(self, user_data: Dict) -> str:
        """Analyze user's learning style based on preferences and behavior"""
        try:
            preferences = user_data.get('content_preferences', {})
            
            # Simple learning style classification
            if preferences.get('visual', 0) > preferences.get('textual', 0):
                if preferences.get('interactive', 0) > 0.5:
                    return 'visual_kinesthetic'
                else:
                    return 'visual'
            else:
                if preferences.get('interactive', 0) > 0.5:
                    return 'reading_kinesthetic'
                else:
                    return 'reading'
                    
        except Exception as e:
            self.logger.error(f"Error analyzing learning style: {str(e)}")
            return 'balanced'

    def generate_learning_path(self, user_id: str, target_skills: List[str], constraints: Optional[Dict] = None) -> Dict:
        """Generate personalized learning path"""
        try:
            if user_id not in self.user_profiles:
                raise ValueError(f"User profile not found for {user_id}")
            
            profile = self.user_profiles[user_id]
            constraints = constraints or {}
            
            # Find optimal path through skill graph
            path = self._find_optimal_path(profile, target_skills, constraints)
            
            # Generate learning modules for each skill
            learning_modules = []
            for i, skill in enumerate(path):
                module = self._create_learning_module(skill, profile, i)
                learning_modules.append(module)
            
            # Calculate estimated timeline
            timeline = self._calculate_timeline(learning_modules, profile['time_availability'])
            
            learning_path = {
                'path_id': f"path_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'user_id': user_id,
                'target_skills': target_skills,
                'learning_path': path,
                'modules': learning_modules,
                'estimated_duration': timeline['total_weeks'],
                'milestones': timeline['milestones'],
                'created_at': datetime.now().isoformat(),
                'constraints': constraints
            }
            
            self.learning_paths[learning_path['path_id']] = learning_path
            return learning_path
            
        except Exception as e:
            self.logger.error(f"Error generating learning path: {str(e)}")
            return {}

    def _find_optimal_path(self, profile: Dict, target_skills: List[str], constraints: Dict) -> List[str]:
        """Find optimal learning path using graph algorithms"""
        try:
            current_skills = set(profile['current_skills'].keys())
            
            # Find all required skills including prerequisites
            all_required_skills = set(target_skills)
            for skill in target_skills:
                if skill in self.skill_graph.nodes:
                    all_required_skills.update(nx.ancestors(self.skill_graph, skill))
            
            # Remove already mastered skills
            skills_to_learn = all_required_skills - current_skills
            
            if not skills_to_learn:
                return []
            
            # Create subgraph with required skills
            subgraph = self.skill_graph.subgraph(skills_to_learn)
            
            # Find topological order respecting dependencies
            try:
                path = list(nx.topological_sort(subgraph))
            except nx.NetworkXError:
                # If cycle exists, use heuristic approach
                path = self._resolve_dependencies_heuristic(skills_to_learn, profile)
            
            # Apply constraints (time, difficulty, etc.)
            path = self._apply_constraints(path, profile, constraints)
            
            return path
            
        except Exception as e:
            self.logger.error(f"Error finding optimal path: {str(e)}")
            return target_skills

    def _resolve_dependencies_heuristic(self, skills: set, profile: Dict) -> List[str]:
        """Resolve skill dependencies using heuristic approach"""
        try:
            resolved = []
            remaining = skills.copy()
            current_skills = set(profile['current_skills'].keys())
            
            while remaining:
                # Find skills with all prerequisites satisfied
                ready_skills = []
                for skill in remaining:
                    prereqs = set(self.skill_graph.nodes[skill].get('prerequisites', []))
                    if prereqs.issubset(current_skills.union(set(resolved))):
                        ready_skills.append(skill)
                
                if not ready_skills:
                    # Break cycle by picking skill with minimum prerequisites
                    ready_skills = [min(remaining, key=lambda s: len(self.skill_graph.nodes[s].get('prerequisites', [])))]
                
                # Select next skill based on user preferences
                next_skill = self._select_next_skill(ready_skills, profile)
                resolved.append(next_skill)
                remaining.remove(next_skill)
            
            return resolved
            
        except Exception as e:
            self.logger.error(f"Error resolving dependencies: {str(e)}")
            return list(skills)

    def _select_next_skill(self, ready_skills: List[str], profile: Dict) -> str:
        """Select next skill based on user preferences and skill properties"""
        try:
            # Score each skill based on multiple factors
            skill_scores = []
            for skill in ready_skills:
                score = 0
                
                # Priority based on learning goals
                if skill in profile['learning_goals']:
                    score += 10
                
                # Difficulty preference (prefer gradual progression)
                skill_difficulty = self.skill_graph.nodes[skill].get('difficulty', 1)
                current_level = self._estimate_user_level(profile)
                if abs(skill_difficulty - current_level) <= 1:
                    score += 5
                
                # Time preference
                estimated_time = self.skill_graph.nodes[skill].get('estimated_time', 60)
                if estimated_time <= profile['time_availability'] * 60:  # Convert to minutes
                    score += 3
                
                skill_scores.append((score, skill))
            
            # Return skill with highest score
            return max(skill_scores, key=lambda x: x[0])[1]
            
        except Exception as e:
            self.logger.error(f"Error selecting next skill: {str(e)}")
            return ready_skills[0]

    def _estimate_user_level(self, profile: Dict) -> int:
        """Estimate user's current skill level"""
        try:
            if not profile['current_skills']:
                return 1
            
            skill_levels = []
            for skill, level in profile['current_skills'].items():
                if isinstance(level, (int, float)):
                    skill_levels.append(level)
                elif isinstance(level, str):
                    skill_levels.append(self.difficulty_levels.get(level.lower(), 1))
            
            if skill_levels:
                avg_level = np.mean(skill_levels)
                return int(round(avg_level))
            
            return 1
            
        except Exception as e:
            self.logger.error(f"Error estimating user level: {str(e)}")
            return 1

    def _apply_constraints(self, path: List[str], profile: Dict, constraints: Dict) -> List[str]:
        """Apply user constraints to learning path"""
        try:
            filtered_path = path.copy()
            
            # Time constraint
            max_time = constraints.get('max_time_weeks', 52)
            total_time = sum(self.skill_graph.nodes[skill].get('estimated_time', 60) for skill in filtered_path)
            max_total_time = max_time * profile['time_availability'] * 60  # Convert to minutes
            
            if total_time > max_total_time:
                # Filter skills to fit time constraint
                filtered_path = self._filter_by_time(filtered_path, max_total_time, profile)
            
            # Difficulty constraint
            max_difficulty = constraints.get('max_difficulty', 4)
            filtered_path = [skill for skill in filtered_path 
                           if self.skill_graph.nodes[skill].get('difficulty', 1) <= max_difficulty]
            
            # Category constraint
            preferred_categories = constraints.get('preferred_categories', [])
            if preferred_categories:
                filtered_path = [skill for skill in filtered_path 
                               if self.skill_graph.nodes[skill].get('category') in preferred_categories]
            
            return filtered_path
            
        except Exception as e:
            self.logger.error(f"Error applying constraints: {str(e)}")
            return path

    def _filter_by_time(self, path: List[str], max_time: int, profile: Dict) -> List[str]:
        """Filter path to fit within time constraints"""
        try:
            filtered_path = []
            current_time = 0
            
            # Prioritize skills based on goals and gaps
            prioritized_skills = self._prioritize_skills(path, profile)
            
            for skill in prioritized_skills:
                skill_time = self.skill_graph.nodes[skill].get('estimated_time', 60)
                if current_time + skill_time <= max_time:
                    filtered_path.append(skill)
                    current_time += skill_time
            
            return filtered_path
            
        except Exception as e:
            self.logger.error(f"Error filtering by time: {str(e)}")
            return path[:len(path)//2]  # Return half as fallback

    def _prioritize_skills(self, skills: List[str], profile: Dict) -> List[str]:
        """Prioritize skills based on user goals and gaps"""
        try:
            skill_scores = []
            learning_goals = set(profile['learning_goals'])
            skill_gaps = set(profile['skill_gaps'].keys())
            
            for skill in skills:
                score = 0
                
                # High priority for learning goals
                if skill in learning_goals:
                    score += 10
                
                # Medium priority for skill gaps
                if skill in skill_gaps:
                    score += 5
                
                # Lower priority for general improvement
                score += 1
                
                skill_scores.append((score, skill))
            
            # Sort by score (descending)
            skill_scores.sort(key=lambda x: x[0], reverse=True)
            return [skill for _, skill in skill_scores]
            
        except Exception as e:
            self.logger.error(f"Error prioritizing skills: {str(e)}")
            return skills

    def _create_learning_module(self, skill: str, profile: Dict, position: int) -> Dict:
        """Create learning module for a specific skill"""
        try:
            skill_data = self.skill_graph.nodes[skill]
            
            module = {
                'skill': skill,
                'position': position,
                'difficulty': skill_data.get('difficulty', 1),
                'category': skill_data.get('category', 'general'),
                'estimated_time': skill_data.get('estimated_time', 60),
                'prerequisites': skill_data.get('prerequisites', []),
                'learning_objectives': self._generate_learning_objectives(skill),
                'content_recommendations': self._recommend_content(skill, profile),
                'assessment_methods': self._recommend_assessments(skill),
                'resources': self._find_resources(skill),
                'success_criteria': self._define_success_criteria(skill)
            }
            
            return module
            
        except Exception as e:
            self.logger.error(f"Error creating learning module for {skill}: {str(e)}")
            return {}

    def _generate_learning_objectives(self, skill: str) -> List[str]:
        """Generate learning objectives for a skill"""
        try:
            # Template-based objective generation
            objectives = [
                f"Understand fundamental concepts of {skill}",
                f"Apply {skill} in practical scenarios",
                f"Analyze problems using {skill} techniques",
                f"Evaluate solutions based on {skill} principles"
            ]
            
            # Add skill-specific objectives based on category
            category = self.skill_graph.nodes[skill].get('category', 'general')
            if category == 'technical':
                objectives.append(f"Implement {skill} in real-world projects")
            elif category == 'soft_skill':
                objectives.append(f"Demonstrate {skill} in team environments")
            
            return objectives
            
        except Exception as e:
            self.logger.error(f"Error generating learning objectives: {str(e)}")
            return [f"Master {skill}"]

    def _recommend_content(self, skill: str, profile: Dict) -> List[Dict]:
        """Recommend learning content based on user preferences"""
        try:
            recommendations = []
            preferred_types = profile.get('preferred_content_types', self.content_types)
            learning_style = profile.get('learning_style', 'balanced')
            
            # Try to get external resources from Google API
            external_resources = []
            if self.google_api:
                try:
                    external_resources = self.google_api.get_learning_path(skill)
                    self.logger.info(f"Retrieved {len(external_resources)} external resources for {skill}")
                except Exception as e:
                    self.logger.warning(f"Failed to fetch external resources for {skill}: {e}")
            
            # Process external resources
            for resource in external_resources[:3]:  # Limit to top 3
                content = {
                    'type': 'external_resource',
                    'title': resource.get('title', f"{skill} - External Resource"),
                    'description': resource.get('snippet', f"External learning resource for {skill}"),
                    'url': resource.get('link', ''),
                    'duration': self._estimate_content_duration('article'),
                    'difficulty': self.skill_graph.nodes[skill].get('difficulty', 1),
                    'style_match': self._calculate_style_match('article', learning_style),
                    'source': 'external'
                }
                recommendations.append(content)
            
            # Add internal recommendations
            for content_type in preferred_types:
                content = {
                    'type': content_type,
                    'title': f"{skill} - {content_type.title()} Tutorial",
                    'description': f"Learn {skill} through {content_type}",
                    'duration': self._estimate_content_duration(content_type),
                    'difficulty': self.skill_graph.nodes[skill].get('difficulty', 1),
                    'style_match': self._calculate_style_match(content_type, learning_style),
                    'source': 'internal'
                }
                recommendations.append(content)
            
            # Sort by style match and prioritize external resources
            recommendations.sort(key=lambda x: (x['source'] == 'external', x['style_match']), reverse=True)
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            self.logger.error(f"Error recommending content: {str(e)}")
            return []

    def _estimate_content_duration(self, content_type: str) -> int:
        """Estimate content duration in minutes"""
        durations = {
            'video': 30,
            'article': 15,
            'practice': 45,
            'project': 120,
            'quiz': 20
        }
        return durations.get(content_type, 30)

    def _calculate_style_match(self, content_type: str, learning_style: str) -> float:
        """Calculate how well content type matches learning style"""
        try:
            style_matches = {
                'visual': {'video': 1.0, 'article': 0.6, 'practice': 0.8, 'project': 0.9, 'quiz': 0.5},
                'reading': {'video': 0.6, 'article': 1.0, 'practice': 0.7, 'project': 0.8, 'quiz': 0.7},
                'visual_kinesthetic': {'video': 0.9, 'article': 0.5, 'practice': 1.0, 'project': 1.0, 'quiz': 0.6},
                'reading_kinesthetic': {'video': 0.5, 'article': 0.9, 'practice': 1.0, 'project': 0.9, 'quiz': 0.8},
                'balanced': {'video': 0.8, 'article': 0.8, 'practice': 0.8, 'project': 0.8, 'quiz': 0.7}
            }
            
            return style_matches.get(learning_style, {}).get(content_type, 0.5)
            
        except Exception as e:
            self.logger.error(f"Error calculating style match: {str(e)}")
            return 0.5

    def _recommend_assessments(self, skill: str) -> List[Dict]:
        """Recommend assessment methods for skill evaluation"""
        try:
            difficulty = self.skill_graph.nodes[skill].get('difficulty', 1)
            category = self.skill_graph.nodes[skill].get('category', 'general')
            
            assessments = [
                {
                    'type': 'quiz',
                    'title': f"{skill} Knowledge Check",
                    'description': f"Test your understanding of {skill} concepts",
                    'duration': 20,
                    'questions': 10 + difficulty * 5
                }
            ]
            
            if category == 'technical':
                assessments.append({
                    'type': 'practical',
                    'title': f"{skill} Practical Exercise",
                    'description': f"Apply {skill} in a hands-on exercise",
                    'duration': 45,
                    'tasks': 3 + difficulty
                })
            
            if difficulty >= 3:  # Advanced skills
                assessments.append({
                    'type': 'project',
                    'title': f"{skill} Capstone Project",
                    'description': f"Complete a comprehensive project using {skill}",
                    'duration': 120,
                    'deliverables': 2
                })
            
            return assessments
            
        except Exception as e:
            self.logger.error(f"Error recommending assessments: {str(e)}")
            return []

    def _find_resources(self, skill: str) -> List[Dict]:
        """Find learning resources for skill"""
        try:
            resources = []
            
            # Try to get external resources from Google API first
            if self.google_api:
                try:
                    external_resources = self.google_api.get_learning_path(skill)
                    for resource in external_resources[:5]:  # Limit to top 5
                        resources.append({
                            'type': 'external_course',
                            'title': resource.get('title', f"{skill} - External Resource"),
                            'description': resource.get('snippet', f"External learning resource for {skill}"),
                            'url': resource.get('link', ''),
                            'access_level': 'external'
                        })
                    self.logger.info(f"Retrieved {len(external_resources)} external resources for {skill}")
                except Exception as e:
                    self.logger.warning(f"Failed to fetch external resources for {skill}: {e}")
            
            # Add fallback internal resources if no external resources found
            if not resources:
                resources = [
                    {
                        'type': 'tutorial',
                        'title': f"{skill} Interactive Tutorial",
                        'url': f"https://tutorial.example.com/{skill.lower()}",
                        'access_level': 'free'
                    },
                    {
                        'type': 'course',
                        'title': f"Complete {skill} Course",
                        'url': f"https://course.example.com/{skill.lower()}",
                        'access_level': 'premium'
                    }
                ]
            
            return resources
            
        except Exception as e:
            self.logger.error(f"Error finding resources: {str(e)}")
            return []

    def _define_success_criteria(self, skill: str) -> List[str]:
        """Define success criteria for skill mastery"""
        try:
            criteria = [
                f"Complete all learning objectives for {skill}",
                f"Score 80% or higher in {skill} assessments",
                f"Successfully apply {skill} in practical exercises"
            ]
            
            difficulty = self.skill_graph.nodes[skill].get('difficulty', 1)
            if difficulty >= 3:
                criteria.append(f"Complete a {skill} project meeting industry standards")
            
            return criteria
            
        except Exception as e:
            self.logger.error(f"Error defining success criteria: {str(e)}")
            return [f"Master {skill}"]

    def _calculate_timeline(self, modules: List[Dict], time_availability: int) -> Dict:
        """Calculate learning timeline with milestones"""
        try:
            total_time = sum(module['estimated_time'] for module in modules)
            total_weeks = max(1, total_time // (time_availability * 60))  # Convert to weeks
            
            # Create milestones
            milestones = []
            milestone_interval = max(1, len(modules) // 4)  # 4 major milestones
            
            for i in range(0, len(modules), milestone_interval):
                milestone_modules = modules[i:i + milestone_interval]
                milestone_time = sum(m['estimated_time'] for m in milestone_modules)
                milestone_week = (i * total_weeks) // len(modules)
                
                milestone = {
                    'week': milestone_week + 1,
                    'title': f"Milestone {len(milestones) + 1}: {milestone_modules[0]['skill']} Mastery",
                    'modules': [m['skill'] for m in milestone_modules],
                    'estimated_time': milestone_time,
                    'assessment': f"Complete assessments for {', '.join([m['skill'] for m in milestone_modules])}"
                }
                milestones.append(milestone)
            
            return {
                'total_weeks': total_weeks,
                'milestones': milestones,
                'total_hours': total_time // 60
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating timeline: {str(e)}")
            return {'total_weeks': 4, 'milestones': [], 'total_hours': 10}

    def update_progress(self, user_id: str, skill: str, progress_data: Dict) -> bool:
        """Update user learning progress"""
        try:
            if user_id not in self.progress_tracking:
                self.progress_tracking[user_id] = {}
            
            if skill not in self.progress_tracking[user_id]:
                self.progress_tracking[user_id][skill] = {
                    'started_at': datetime.now().isoformat(),
                    'modules_completed': [],
                    'assessments_passed': [],
                    'time_spent': 0,
                    'current_level': 1
                }
            
            # Update progress
            progress = self.progress_tracking[user_id][skill]
            progress.update(progress_data)
            progress['last_updated'] = datetime.now().isoformat()
            
            # Check if skill is mastered
            if self._check_skill_mastery(skill, progress):
                progress['status'] = 'completed'
                progress['completed_at'] = datetime.now().isoformat()
                
                # Update user profile
                if user_id in self.user_profiles:
                    self.user_profiles[user_id]['current_skills'][skill] = progress.get('current_level', 3)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating progress: {str(e)}")
            return False

    def _check_skill_mastery(self, skill: str, progress: Dict) -> bool:
        """Check if user has mastered the skill"""
        try:
            # Check completion criteria
            modules_completed = len(progress.get('modules_completed', []))
            assessments_passed = len(progress.get('assessments_passed', []))
            
            # Basic mastery criteria
            if modules_completed >= 3 and assessments_passed >= 2:
                return True
            
            # Time-based criteria (minimum time investment)
            min_time_required = self.skill_graph.nodes[skill].get('estimated_time', 60) * 0.8
            if progress.get('time_spent', 0) >= min_time_required:
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking skill mastery: {str(e)}")
            return False

    def get_recommendations(self, user_id: str) -> Dict:
        """Get personalized learning recommendations"""
        try:
            if user_id not in self.user_profiles:
                return {}
            
            profile = self.user_profiles[user_id]
            progress = self.progress_tracking.get(user_id, {})
            
            recommendations = {
                'next_skills': self._recommend_next_skills(profile, progress),
                'content_suggestions': self._suggest_content(profile),
                'study_schedule': self._generate_study_schedule(profile),
                'improvement_areas': self._identify_improvement_areas(profile, progress)
            }
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting recommendations: {str(e)}")
            return {}

    def _recommend_next_skills(self, profile: Dict, progress: Dict) -> List[str]:
        """Recommend next skills to learn"""
        try:
            current_skills = set(profile['current_skills'].keys())
            completed_skills = set(progress.keys())
            
            # Find skills that have prerequisites satisfied
            next_skills = []
            for skill in self.skill_graph.nodes:
                if skill not in current_skills and skill not in completed_skills:
                    prereqs = set(self.skill_graph.nodes[skill].get('prerequisites', []))
                    if prereqs.issubset(current_skills.union(completed_skills)):
                        next_skills.append(skill)
            
            # Prioritize based on learning goals
            learning_goals = set(profile['learning_goals'])
            prioritized = [skill for skill in next_skills if skill in learning_goals]
            prioritized.extend([skill for skill in next_skills if skill not in learning_goals])
            
            return prioritized[:5]  # Return top 5 recommendations
            
        except Exception as e:
            self.logger.error(f"Error recommending next skills: {str(e)}")
            return []

    def _suggest_content(self, profile: Dict) -> List[Dict]:
        """Suggest content based on current progress"""
        try:
            suggestions = []
            
            # Suggest review content for current skills
            for skill, level in profile['current_skills'].items():
                if level < 3:  # Not yet mastered
                    content = {
                        'skill': skill,
                        'type': 'review',
                        'title': f"{skill} Refresher Course",
                        'reason': "Strengthen foundational knowledge"
                    }
                    suggestions.append(content)
            
            return suggestions[:3]  # Return top 3 suggestions
            
        except Exception as e:
            self.logger.error(f"Error suggesting content: {str(e)}")
            return []

    def _generate_study_schedule(self, profile: Dict) -> Dict:
        """Generate personalized study schedule"""
        try:
            time_availability = profile.get('time_availability', 5)  # hours per week
            
            schedule = {
                'weekly_hours': time_availability,
                'study_sessions': self._create_study_sessions(time_availability),
                'break_intervals': self._calculate_break_intervals(time_availability),
                'optimal_times': self._suggest_optimal_times(profile)
            }
            
            return schedule
            
        except Exception as e:
            self.logger.error(f"Error generating study schedule: {str(e)}")
            return {}

    def _create_study_sessions(self, weekly_hours: int) -> List[Dict]:
        """Create study sessions based on availability"""
        try:
            sessions = []
            sessions_per_week = min(7, max(2, weekly_hours // 2))  # 2-7 sessions per week
            session_duration = (weekly_hours * 60) // sessions_per_week  # minutes
            
            for day in range(sessions_per_week):
                session = {
                    'day': day,
                    'duration': session_duration,
                    'type': 'learning' if day % 2 == 0 else 'practice'
                }
                sessions.append(session)
            
            return sessions
            
        except Exception as e:
            self.logger.error(f"Error creating study sessions: {str(e)}")
            return []

    def _calculate_break_intervals(self, weekly_hours: int) -> Dict:
        """Calculate optimal break intervals"""
        try:
            if weekly_hours <= 5:
                return {'study_duration': 25, 'break_duration': 5, 'long_break_frequency': 4}
            elif weekly_hours <= 10:
                return {'study_duration': 45, 'break_duration': 10, 'long_break_frequency': 3}
            else:
                return {'study_duration': 60, 'break_duration': 15, 'long_break_frequency': 2}
                
        except Exception as e:
            self.logger.error(f"Error calculating break intervals: {str(e)}")
            return {'study_duration': 25, 'break_duration': 5, 'long_break_frequency': 4}

    def _suggest_optimal_times(self, profile: Dict) -> List[str]:
        """Suggest optimal study times based on preferences"""
        try:
            # Default suggestions
            optimal_times = ['Morning (9-11 AM)', 'Evening (7-9 PM)']
            
            # Could be enhanced with user preference data
            return optimal_times
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimal times: {str(e)}")
            return ['Evening (7-9 PM)']

    def _identify_improvement_areas(self, profile: Dict, progress: Dict) -> List[Dict]:
        """Identify areas needing improvement"""
        try:
            improvement_areas = []
            
            # Check skill gaps
            for skill, gap_data in profile.get('skill_gaps', {}).items():
                if skill not in progress or progress[skill].get('status') != 'completed':
                    area = {
                        'skill': skill,
                        'gap_level': gap_data.get('level', 'medium'),
                        'priority': 'high' if skill in profile.get('learning_goals', []) else 'medium',
                        'suggestion': f"Focus on {skill} to close critical skill gap"
                    }
                    improvement_areas.append(area)
            
            return improvement_areas[:3]  # Return top 3 areas
            
        except Exception as e:
            self.logger.error(f"Error identifying improvement areas: {str(e)}")
            return []

    def export_learning_path(self, path_id: str, format: str = 'json') -> Dict:
        """Export learning path in specified format"""
        try:
            if path_id not in self.learning_paths:
                return {}
            
            path = self.learning_paths[path_id]
            
            if format == 'json':
                return path
            elif format == 'summary':
                return self._create_path_summary(path)
            else:
                return path
                
        except Exception as e:
            self.logger.error(f"Error exporting learning path: {str(e)}")
            return {}

    def _create_path_summary(self, path: Dict) -> Dict:
        """Create summary of learning path"""
        try:
            summary = {
                'path_id': path['path_id'],
                'user_id': path['user_id'],
                'target_skills': path['target_skills'],
                'total_skills': len(path['learning_path']),
                'estimated_weeks': path['estimated_duration'],
                'difficulty_distribution': self._analyze_difficulty_distribution(path),
                'category_distribution': self._analyze_category_distribution(path),
                'milestones': len(path['milestones'])
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating path summary: {str(e)}")
            return {}

    def _analyze_difficulty_distribution(self, path: Dict) -> Dict:
        """Analyze difficulty distribution in learning path"""
        try:
            difficulties = [module['difficulty'] for module in path['modules']]
            
            distribution = {
                'beginner': difficulties.count(1),
                'intermediate': difficulties.count(2),
                'advanced': difficulties.count(3),
                'expert': difficulties.count(4)
            }
            
            return distribution
            
        except Exception as e:
            self.logger.error(f"Error analyzing difficulty distribution: {str(e)}")
            return {}

    def _analyze_category_distribution(self, path: Dict) -> Dict:
        """Analyze category distribution in learning path"""
        try:
            categories = [module['category'] for module in path['modules']]
            category_counts = {}
            
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return category_counts
            
        except Exception as e:
            self.logger.error(f"Error analyzing category distribution: {str(e)}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the learning path generator with Google API integration
    # Note: You need to provide your actual Google API key and CSE ID
    google_api_key = "your_google_api_key_here"  # Replace with actual API key
    google_cse_id = "your_cse_id_here"  # Replace with actual CSE ID
    
    # Initialize with or without Google API
    lpg = LearningPathGenerator(google_api_key, google_cse_id) if google_api_key != "your_google_api_key_here" else LearningPathGenerator()
    
    # Example skill data
    skills_data = {
        'Python': {
            'difficulty': 1,
            'category': 'technical',
            'estimated_time': 120,
            'prerequisites': []
        },
        'Data Analysis': {
            'difficulty': 2,
            'category': 'technical',
            'estimated_time': 180,
            'prerequisites': ['Python']
        },
        'Machine Learning': {
            'difficulty': 3,
            'category': 'technical',
            'estimated_time': 240,
            'prerequisites': ['Python', 'Data Analysis']
        },
        'Communication': {
            'difficulty': 1,
            'category': 'soft_skill',
            'estimated_time': 60,
            'prerequisites': []
        }
    }
    
    # Initialize skill graph
    lpg.initialize_skill_graph(skills_data)
    
    # Create user profile
    user_data = {
        'current_skills': {'Python': 2},
        'learning_goals': ['Machine Learning'],
        'time_availability': 10,
        'preferred_content': ['video', 'practice'],
        'skill_gaps': {'Data Analysis': {'level': 'medium'}}
    }
    
    profile = lpg.create_user_profile('user123', user_data)
    print("User profile created:", profile['user_id'])
    
    # Generate learning path
    learning_path = lpg.generate_learning_path('user123', ['Machine Learning'])
    print("Learning path generated:", learning_path.get('path_id'))
    print("Skills to learn:", learning_path.get('learning_path', []))
    print("Estimated duration:", learning_path.get('estimated_duration'), "weeks")
