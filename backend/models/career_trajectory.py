"""
Career Trajectory Model - Career Progression Prediction

This module implements a comprehensive career trajectory prediction system that
leverages competency data, learning paths, and market trends to predict career
progression and suggest optimal career moves.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import networkx as nx
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CareerLevel(Enum):
    """Career progression levels"""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID_LEVEL = "mid_level"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


@dataclass
class Role:
    """Represents a career role with its requirements"""
    title: str
    level: CareerLevel
    required_skills: Dict[str, int]  # skill -> required level
    experience_years: int
    salary_range: Tuple[int, int]
    growth_potential: float
    market_demand: float


@dataclass
class CareerPath:
    """Represents a career progression path"""
    current_role: str
    target_role: str
    steps: List[str]
    estimated_timeline: int  # months
    required_skills: Dict[str, int]
    confidence_score: float


class CareerTrajectory:
    """
    Career Trajectory Prediction System
    
    This class implements ML-based career progression prediction, considering
    competency levels, market trends, and individual learning patterns.
    """
    
    def __init__(self):
        """Initialize the career trajectory system"""
        self.logger = logging.getLogger(__name__)
        
        # ML models
        self.role_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.salary_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.timeline_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        
        # Data preprocessing
        self.scaler = StandardScaler()
        self.role_encoder = LabelEncoder()
        
        # Career data
        self.roles_database = {}
        self.career_graph = nx.DiGraph()
        self.market_trends = {}
        
        # Training data
        self.training_data = None
        self.is_trained = False
        
        self._initialize_roles_database()
        self._build_career_graph()
    
    def _initialize_roles_database(self):
        """Initialize the roles database with common career paths"""
        roles = {
            "Junior Data Analyst": Role(
                title="Junior Data Analyst",
                level=CareerLevel.JUNIOR,
                required_skills={
                    "Excel": 3,
                    "SQL": 2,
                    "Python": 2,
                    "Statistics": 2,
                    "Data Visualization": 2
                },
                experience_years=0-2,
                salary_range=(45000, 65000),
                growth_potential=0.8,
                market_demand=0.9
            ),
            "Data Analyst": Role(
                title="Data Analyst",
                level=CareerLevel.MID_LEVEL,
                required_skills={
                    "Excel": 4,
                    "SQL": 3,
                    "Python": 3,
                    "Statistics": 3,
                    "Data Visualization": 3,
                    "Business Acumen": 2
                },
                experience_years=2-4,
                salary_range=(65000, 85000),
                growth_potential=0.7,
                market_demand=0.8
            ),
            "Senior Data Analyst": Role(
                title="Senior Data Analyst",
                level=CareerLevel.SENIOR,
                required_skills={
                    "Excel": 4,
                    "SQL": 4,
                    "Python": 4,
                    "Statistics": 4,
                    "Data Visualization": 4,
                    "Business Acumen": 3,
                    "Machine Learning": 2
                },
                experience_years=4-6,
                salary_range=(85000, 110000),
                growth_potential=0.6,
                market_demand=0.7
            ),
            "Data Scientist": Role(
                title="Data Scientist",
                level=CareerLevel.SENIOR,
                required_skills={
                    "Python": 5,
                    "Machine Learning": 4,
                    "Statistics": 4,
                    "SQL": 3,
                    "Deep Learning": 3,
                    "Business Acumen": 3
                },
                experience_years=3-5,
                salary_range=(95000, 130000),
                growth_potential=0.8,
                market_demand=0.9
            ),
            "Senior Data Scientist": Role(
                title="Senior Data Scientist",
                level=CareerLevel.SENIOR,
                required_skills={
                    "Python": 5,
                    "Machine Learning": 5,
                    "Statistics": 5,
                    "Deep Learning": 4,
                    "Business Acumen": 4,
                    "Research": 3
                },
                experience_years=5-8,
                salary_range=(130000, 160000),
                growth_potential=0.7,
                market_demand=0.8
            ),
            "ML Engineer": Role(
                title="ML Engineer",
                level=CareerLevel.SENIOR,
                required_skills={
                    "Python": 5,
                    "Machine Learning": 4,
                    "Software Engineering": 4,
                    "Cloud Computing": 3,
                    "DevOps": 3,
                    "Deep Learning": 3
                },
                experience_years=3-6,
                salary_range=(100000, 140000),
                growth_potential=0.8,
                market_demand=0.9
            ),
            "Data Science Manager": Role(
                title="Data Science Manager",
                level=CareerLevel.MANAGER,
                required_skills={
                    "Leadership": 4,
                    "Project Management": 4,
                    "Machine Learning": 3,
                    "Business Acumen": 4,
                    "Communication": 4,
                    "Strategic Thinking": 3
                },
                experience_years=6-10,
                salary_range=(120000, 150000),
                growth_potential=0.6,
                market_demand=0.7
            )
        }
        
        self.roles_database = roles
    
    def _build_career_graph(self):
        """Build a directed graph representing career progression paths"""
        # Define career progression edges
        career_progressions = [
            ("Junior Data Analyst", "Data Analyst"),
            ("Data Analyst", "Senior Data Analyst"),
            ("Data Analyst", "Data Scientist"),
            ("Senior Data Analyst", "Data Scientist"),
            ("Data Scientist", "Senior Data Scientist"),
            ("Data Scientist", "ML Engineer"),
            ("Senior Data Scientist", "Data Science Manager"),
            ("Data Scientist", "Data Science Manager"),
            ("ML Engineer", "Senior Data Scientist"),
            ("Senior Data Scientist", "Data Science Manager")
        ]
        
        # Add nodes and edges to the graph
        for role_title, role in self.roles_database.items():
            self.career_graph.add_node(role_title, role=role)
        
        for from_role, to_role in career_progressions:
            if from_role in self.roles_database and to_role in self.roles_database:
                self.career_graph.add_edge(from_role, to_role)
    
    def predict_next_roles(self, current_role: str, user_skills: Dict[str, int], 
                          top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Predict the next best career roles based on current role and skills
        
        Args:
            current_role: Current job title
            user_skills: Dictionary of skill -> level
            top_k: Number of top recommendations to return
            
        Returns:
            List of (role_title, confidence_score) tuples
        """
        try:
            if current_role not in self.roles_database:
                self.logger.warning(f"Current role '{current_role}' not found in database")
                return []
            
            # Get possible next roles from career graph
            possible_roles = list(self.career_graph.successors(current_role))
            
            if not possible_roles:
                self.logger.info(f"No career progression paths found for '{current_role}'")
                return []
            
            # Calculate compatibility scores for each possible role
            role_scores = []
            for role_title in possible_roles:
                role = self.roles_database[role_title]
                score = self._calculate_role_compatibility(user_skills, role)
                role_scores.append((role_title, score))
            
            # Sort by score and return top_k
            role_scores.sort(key=lambda x: x[1], reverse=True)
            return role_scores[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error predicting next roles: {e}")
            return []
    
    def _calculate_role_compatibility(self, user_skills: Dict[str, int], 
                                   role: Role) -> float:
        """
        Calculate compatibility score between user skills and role requirements
        
        Args:
            user_skills: Dictionary of skill -> level
            role: Role object with requirements
            
        Returns:
            Compatibility score (0-1)
        """
        try:
            total_score = 0
            max_score = 0
            
            for skill, required_level in role.required_skills.items():
                user_level = user_skills.get(skill, 0)
                
                # Calculate skill match score
                if user_level >= required_level:
                    skill_score = 1.0
                elif user_level >= required_level - 1:
                    skill_score = 0.7
                elif user_level >= required_level - 2:
                    skill_score = 0.4
                else:
                    skill_score = 0.1
                
                total_score += skill_score
                max_score += 1.0
            
            # Normalize score
            if max_score > 0:
                base_score = total_score / max_score
            else:
                base_score = 0.0
            
            # Adjust for growth potential and market demand
            adjusted_score = base_score * (0.6 + 0.2 * role.growth_potential + 
                                         0.2 * role.market_demand)
            
            return adjusted_score
            
        except Exception as e:
            self.logger.error(f"Error calculating role compatibility: {e}")
            return 0.0
    
    def generate_career_path(self, current_role: str, target_role: str,
                           user_skills: Dict[str, int]) -> Optional[CareerPath]:
        """
        Generate a detailed career path from current to target role
        
        Args:
            current_role: Starting role
            target_role: Desired role
            user_skills: Current skill levels
            
        Returns:
            CareerPath object or None if no path found
        """
        try:
            # Find shortest path in career graph
            if current_role not in self.career_graph or target_role not in self.career_graph:
                self.logger.warning("One or both roles not found in career graph")
                return None
            
            try:
                path_nodes = nx.shortest_path(self.career_graph, current_role, target_role)
            except nx.NetworkXNoPath:
                self.logger.info(f"No career path found from '{current_role}' to '{target_role}'")
                return None
            
            # Calculate required skills for the entire path
            all_required_skills = {}
            for role_title in path_nodes[1:]:  # Skip current role
                role = self.roles_database[role_title]
                for skill, level in role.required_skills.items():
                    all_required_skills[skill] = max(all_required_skills.get(skill, 0), level)
            
            # Calculate skill gaps
            skill_gaps = {}
            for skill, required_level in all_required_skills.items():
                current_level = user_skills.get(skill, 0)
                if current_level < required_level:
                    skill_gaps[skill] = required_level - current_level
            
            # Estimate timeline (6 months per skill level gap, minimum 3 months)
            total_gap = sum(skill_gaps.values())
            estimated_months = max(3, total_gap * 6)
            
            # Calculate confidence score
            confidence = self._calculate_path_confidence(user_skills, path_nodes)
            
            return CareerPath(
                current_role=current_role,
                target_role=target_role,
                steps=path_nodes,
                estimated_timeline=estimated_months,
                required_skills=skill_gaps,
                confidence_score=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error generating career path: {e}")
            return None
    
    def _calculate_path_confidence(self, user_skills: Dict[str, int], 
                                 path_nodes: List[str]) -> float:
        """Calculate confidence score for a career path"""
        try:
            total_compatibility = 0
            for role_title in path_nodes[1:]:  # Skip current role
                role = self.roles_database[role_title]
                compatibility = self._calculate_role_compatibility(user_skills, role)
                total_compatibility += compatibility
            
            average_compatibility = total_compatibility / len(path_nodes[1:])
            return average_compatibility
            
        except Exception as e:
            self.logger.error(f"Error calculating path confidence: {e}")
            return 0.0
    
    def predict_salary_trajectory(self, career_path: CareerPath, 
                                current_salary: int) -> Dict[str, Any]:
        """
        Predict salary progression along a career path
        
        Args:
            career_path: Career path object
            current_salary: Current annual salary
            
        Returns:
            Dictionary with salary predictions for each step
        """
        try:
            salary_predictions = {}
            
            for i, role_title in enumerate(career_path.steps):
                if role_title in self.roles_database:
                    role = self.roles_database[role_title]
                    
                    # Use midpoint of salary range as base
                    base_salary = sum(role.salary_range) / 2
                    
                    # Adjust for experience and timeline
                    experience_factor = 1 + (i * 0.15)  # 15% increase per step
                    timeline_factor = 1 + (career_path.estimated_timeline / 12 * 0.05)  # 5% per year
                    
                    predicted_salary = base_salary * experience_factor * timeline_factor
                    
                    # Ensure it's higher than current salary for progression
                    if i > 0:
                        predicted_salary = max(predicted_salary, 
                                            list(salary_predictions.values())[-1] * 1.1)
                    
                    salary_predictions[role_title] = {
                        "predicted_salary": int(predicted_salary),
                        "salary_range": role.salary_range,
                        "years_experience": i * 2  # Estimate 2 years per step
                    }
            
            return salary_predictions
            
        except Exception as e:
            self.logger.error(f"Error predicting salary trajectory: {e}")
            return {}
    
    def analyze_skill_gaps_for_career(self, target_role: str, 
                                    user_skills: Dict[str, int]) -> Dict[str, Any]:
        """
        Analyze skill gaps for a specific target role
        
        Args:
            target_role: Desired role
            user_skills: Current skill levels
            
        Returns:
            Dictionary with skill gap analysis
        """
        try:
            if target_role not in self.roles_database:
                self.logger.warning(f"Target role '{target_role}' not found")
                return {}
            
            role = self.roles_database[target_role]
            
            skill_gaps = {}
            skill_matches = {}
            
            for skill, required_level in role.required_skills.items():
                current_level = user_skills.get(skill, 0)
                
                if current_level >= required_level:
                    skill_matches[skill] = {
                        "current": current_level,
                        "required": required_level,
                        "status": "met"
                    }
                else:
                    gap = required_level - current_level
                    skill_gaps[skill] = {
                        "current": current_level,
                        "required": required_level,
                        "gap": gap,
                        "priority": "high" if gap >= 3 else "medium" if gap >= 2 else "low"
                    }
            
            # Calculate overall readiness
            total_skills = len(role.required_skills)
            met_skills = len(skill_matches)
            readiness_score = met_skills / total_skills if total_skills > 0 else 0
            
            return {
                "target_role": target_role,
                "readiness_score": readiness_score,
                "skill_gaps": skill_gaps,
                "skill_matches": skill_matches,
                "total_gaps": len(skill_gaps),
                "critical_gaps": len([s for s in skill_gaps.values() if s["priority"] == "high"])
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing skill gaps: {e}")
            return {}
    
    def get_market_insights(self, role_title: str) -> Dict[str, Any]:
        """
        Get market insights for a specific role
        
        Args:
            role_title: Role to analyze
            
        Returns:
            Dictionary with market insights
        """
        try:
            if role_title not in self.roles_database:
                return {}
            
            role = self.roles_database[role_title]
            
            # Simulate market data (in real implementation, this would come from external APIs)
            market_data = {
                "role": role_title,
                "growth_potential": role.growth_potential,
                "market_demand": role.market_demand,
                "salary_range": role.salary_range,
                "experience_required": role.experience_years,
                "top_skills": sorted(role.required_skills.items(), 
                                   key=lambda x: x[1], reverse=True)[:5],
                "related_roles": list(self.career_graph.successors(role_title)) + 
                               list(self.career_graph.predecessors(role_title))
            }
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"Error getting market insights: {e}")
            return {}
    
    def visualize_career_path(self, career_path: CareerPath, 
                            save_path: Optional[str] = None):
        """
        Visualize a career path using matplotlib
        
        Args:
            career_path: Career path to visualize
            save_path: Optional path to save the visualization
        """
        try:
            plt.figure(figsize=(12, 8))
            
            # Create subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # Career progression timeline
            steps = career_path.steps
            years = list(range(len(steps)))
            
            ax1.plot(years, [1] * len(steps), 'o-', linewidth=2, markersize=8)
            ax1.set_title('Career Progression Timeline', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Career Steps')
            ax1.set_ylabel('Progression')
            ax1.set_ylim(0, 2)
            ax1.grid(True, alpha=0.3)
            
            # Add role labels
            for i, step in enumerate(steps):
                ax1.annotate(step, (i, 1), textcoords="offset points", 
                           xytext=(0, 20), ha='center', fontsize=10)
            
            # Skill requirements bar chart
            if career_path.required_skills:
                skills = list(career_path.required_skills.keys())
                gaps = list(career_path.required_skills.values())
                
                colors = ['red' if gap >= 3 else 'orange' if gap >= 2 else 'yellow' 
                         for gap in gaps]
                
                ax2.bar(skills, gaps, color=colors, alpha=0.7)
                ax2.set_title('Skill Development Requirements', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Skills')
                ax2.set_ylabel('Skill Levels to Develop')
                ax2.tick_params(axis='x', rotation=45)
                
                # Add value labels on bars
                for i, gap in enumerate(gaps):
                    ax2.text(i, gap + 0.1, str(gap), ha='center', va='bottom')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Career path visualization saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error visualizing career path: {e}")
    
    def generate_career_report(self, user_skills: Dict[str, int], 
                             current_role: str, target_role: str) -> Dict[str, Any]:
        """
        Generate a comprehensive career analysis report
        
        Args:
            user_skills: Current skill levels
            current_role: Current job title
            target_role: Desired job title
            
        Returns:
            Dictionary containing comprehensive career analysis
        """
        try:
            report = {
                "generated_at": datetime.now().isoformat(),
                "user_profile": {
                    "current_role": current_role,
                    "target_role": target_role,
                    "total_skills": len(user_skills),
                    "skill_summary": user_skills
                }
            }
            
            # Career path analysis
            career_path = self.generate_career_path(current_role, target_role, user_skills)
            if career_path:
                report["career_path"] = {
                    "steps": career_path.steps,
                    "estimated_timeline_months": career_path.estimated_timeline,
                    "confidence_score": career_path.confidence_score,
                    "required_skills": career_path.required_skills
                }
                
                # Salary predictions
                salary_trajectory = self.predict_salary_trajectory(career_path, 75000)
                report["salary_trajectory"] = salary_trajectory
            
            # Skill gap analysis
            skill_gaps = self.analyze_skill_gaps_for_career(target_role, user_skills)
            report["skill_gap_analysis"] = skill_gaps
            
            # Next role recommendations
            next_roles = self.predict_next_roles(current_role, user_skills, top_k=5)
            report["next_role_recommendations"] = next_roles
            
            # Market insights
            market_insights = self.get_market_insights(target_role)
            report["market_insights"] = market_insights
            
            # Overall assessment
            if career_path:
                report["overall_assessment"] = {
                    "readiness_score": skill_gaps.get("readiness_score", 0),
                    "path_feasibility": "high" if career_path.confidence_score > 0.7 else 
                                      "medium" if career_path.confidence_score > 0.4 else "low",
                    "estimated_time_to_target": f"{career_path.estimated_timeline} months",
                    "critical_skill_gaps": skill_gaps.get("critical_gaps", 0)
                }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating career report: {e}")
            return {"error": str(e)}


# Example usage and testing
if __name__ == "__main__":
    # Initialize the career trajectory system
    career_system = CareerTrajectory()
    
    # Example user profile
    user_skills = {
        "Python": 3,
        "SQL": 2,
        "Statistics": 2,
        "Excel": 3,
        "Machine Learning": 1,
        "Data Visualization": 2,
        "Business Acumen": 1
    }
    
    current_role = "Junior Data Analyst"
    target_role = "Data Scientist"
    
    print("=== Career Trajectory Analysis ===\n")
    
    # 1. Predict next roles
    print("1. Next Role Recommendations:")
    next_roles = career_system.predict_next_roles(current_role, user_skills, top_k=3)
    for role, score in next_roles:
        print(f"   {role}: {score:.2f}")
    print()
    
    # 2. Generate career path
    print("2. Career Path Generation:")
    career_path = career_system.generate_career_path(current_role, target_role, user_skills)
    if career_path:
        print(f"   Path: {' -> '.join(career_path.steps)}")
        print(f"   Estimated timeline: {career_path.estimated_timeline} months")
        print(f"   Confidence score: {career_path.confidence_score:.2f}")
        print(f"   Skill gaps to address: {len(career_path.required_skills)}")
    print()
    
    # 3. Skill gap analysis
    print("3. Skill Gap Analysis:")
    skill_gaps = career_system.analyze_skill_gaps_for_career(target_role, user_skills)
    print(f"   Readiness score: {skill_gaps.get('readiness_score', 0):.2f}")
    print(f"   Total skill gaps: {skill_gaps.get('total_gaps', 0)}")
    print(f"   Critical gaps: {skill_gaps.get('critical_gaps', 0)}")
    print()
    
    # 4. Market insights
    print("4. Market Insights:")
    market_insights = career_system.get_market_insights(target_role)
    if market_insights:
        print(f"   Growth potential: {market_insights.get('growth_potential', 0):.2f}")
        print(f"   Market demand: {market_insights.get('market_demand', 0):.2f}")
        print(f"   Salary range: ${market_insights.get('salary_range', [0, 0])[0]:,} - "
              f"${market_insights.get('salary_range', [0, 0])[1]:,}")
    print()
    
    # 5. Generate comprehensive report
    print("5. Generating Comprehensive Career Report...")
    report = career_system.generate_career_report(user_skills, current_role, target_role)
    
    if "error" not in report:
        print("   Report generated successfully!")
        print(f"   Overall readiness: {report['overall_assessment']['readiness_score']:.2f}")
        print(f"   Path feasibility: {report['overall_assessment']['path_feasibility']}")
        print(f"   Time to target: {report['overall_assessment']['estimated_time_to_target']}")
    else:
        print(f"   Error generating report: {report['error']}")
    
    print("\n=== Analysis Complete ===")
