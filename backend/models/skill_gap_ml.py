"""
Skill Gap Analysis - NLP for Question-Answer Analysis, Classification, Recommendation Systems
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, AutoModel
import torch
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import gensim
from gensim.models import Word2Vec
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SkillGapAnalysisSystem:
    """
    Comprehensive skill gap analysis with ML capabilities
    """
    
    def __init__(self):
        # Initialize NLP models
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = AutoModel.from_pretrained('bert-base-uncased')
        
        # Initialize classifiers
        self.skill_level_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.skill_category_classifier = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.answer_quality_classifier = SVC(kernel='rbf', probability=True)
        
        # Initialize vectorizers
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.skill_vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        
        # Initialize clustering
        self.user_segmentation_kmeans = KMeans(n_clusters=5, random_state=42)
        
        # Initialize sentiment analysis
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize word embeddings
        self.word2vec_model = None
        
        # Training data storage
        self.training_data = {
            'skill_levels': [],
            'skill_categories': [],
            'answer_qualities': [],
            'user_behaviors': []
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_answer_quality(self, question: str, answer: str, 
                              expected_skills: List[str]) -> Dict:
        """
        Analyze answer quality using multiple NLP techniques
        """
        try:
            # Text preprocessing
            processed_answer = self._preprocess_text(answer)
            
            # Feature extraction
            features = self._extract_answer_features(question, processed_answer, expected_skills)
            
            # Semantic similarity using BERT
            semantic_score = self._calculate_semantic_similarity(question, processed_answer)
            
            # Skill coverage analysis
            skill_coverage = self._analyze_skill_coverage(processed_answer, expected_skills)
            
            # Sentiment analysis
            sentiment_score = self.sentiment_analyzer.polarity_scores(processed_answer)
            
            # TextBlob analysis
            textblob_analysis = TextBlob(processed_answer)
            
            # Overall quality score
            quality_score = self._calculate_quality_score(
                semantic_score, skill_coverage, sentiment_score, textblob_analysis
            )
            
            # Classification
            quality_level = self._classify_answer_quality(features)
            
            # Generate feedback
            feedback = self._generate_answer_feedback(
                quality_score, skill_coverage, semantic_score
            )
            
            return {
                'quality_score': quality_score,
                'quality_level': quality_level,
                'semantic_similarity': semantic_score,
                'skill_coverage': skill_coverage,
                'sentiment_analysis': sentiment_score,
                'textblob_analysis': {
                    'polarity': textblob_analysis.sentiment.polarity,
                    'subjectivity': textblob_analysis.sentiment.subjectivity
                },
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Answer quality analysis error: {e}")
            return {'error': str(e)}
    
    def classify_skill_level(self, user_answers: List[Dict], 
                           skill_domain: str) -> Dict:
        """
        Classify user skill level using ensemble methods
        """
        try:
            # Prepare features
            features = self._prepare_skill_level_features(user_answers, skill_domain)
            
            # Make prediction
            if len(self.training_data['skill_levels']) > 0:
                skill_level = self.skill_level_classifier.predict([features])[0]
                skill_probabilities = self.skill_level_classifier.predict_proba([features])[0]
            else:
                # Default classification if no training data
                skill_level = self._default_skill_classification(features)
                skill_probabilities = [0.25, 0.25, 0.25, 0.25]  # Beginner, Intermediate, Advanced, Expert
            
            # Generate skill level report
            report = self._generate_skill_level_report(
                skill_level, skill_probabilities, user_answers, skill_domain
            )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Skill level classification error: {e}")
            return {'error': str(e)}
    
    def categorize_skills(self, user_responses: List[str]) -> Dict:
        """
        Categorize user skills using ML classification
        """
        try:
            # Text preprocessing
            processed_responses = [self._preprocess_text(response) for response in user_responses]
            
            # Feature extraction
            text_features = self.tfidf_vectorizer.fit_transform(processed_responses)
            
            # Make predictions
            if len(self.training_data['skill_categories']) > 0:
                categories = self.skill_category_classifier.predict(text_features)
                category_probabilities = self.skill_category_classifier.predict_proba(text_features)
            else:
                # Default categorization
                categories = self._default_skill_categorization(processed_responses)
                category_probabilities = [[0.2] * 5 for _ in processed_responses]  # 5 categories
            
            # Analyze skill distribution
            skill_distribution = self._analyze_skill_distribution(categories, category_probabilities)
            
            return {
                'skill_categories': categories.tolist(),
                'category_probabilities': category_probabilities.tolist(),
                'skill_distribution': skill_distribution,
                'dominant_skills': self._get_dominant_skills(skill_distribution),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Skill categorization error: {e}")
            return {'error': str(e)}
    
    def generate_learning_recommendations(self, user_profile: Dict, 
                                        skill_gaps: List[str]) -> Dict:
        """
        Generate personalized learning recommendations using recommendation systems
        """
        try:
            # User profile analysis
            user_features = self._extract_user_profile_features(user_profile)
            
            # Content-based filtering
            content_recommendations = self._content_based_filtering(skill_gaps, user_features)
            
            # Collaborative filtering (if enough data)
            collaborative_recommendations = self._collaborative_filtering(user_profile)
            
            # Knowledge graph-based recommendations
            knowledge_graph_recommendations = self._knowledge_graph_recommendations(skill_gaps)
            
            # Combine recommendations
            combined_recommendations = self._combine_recommendations([
                content_recommendations,
                collaborative_recommendations,
                knowledge_graph_recommendations
            ])
            
            # Prioritize recommendations
            prioritized_recommendations = self._prioritize_recommendations(
                combined_recommendations, user_profile
            )
            
            return {
                'recommendations': prioritized_recommendations,
                'learning_path': self._generate_learning_path(prioritized_recommendations),
                'estimated_completion_time': self._estimate_completion_time(prioritized_recommendations),
                'difficulty_progression': self._generate_difficulty_progression(prioritized_recommendations),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Learning recommendations error: {e}")
            return {'error': str(e)}
    
    def segment_users(self, user_data: List[Dict]) -> Dict:
        """
        Segment users using clustering algorithms
        """
        try:
            # Prepare user features
            user_features = self._prepare_user_segmentation_features(user_data)
            
            # Perform clustering
            if len(user_features) > 5:  # Minimum users for clustering
                clusters = self.user_segmentation_kmeans.fit_predict(user_features)
                cluster_centers = self.user_segmentation_kmeans.cluster_centers_
            else:
                clusters = [0] * len(user_features)
                cluster_centers = [[0] * user_features.shape[1]]
            
            # Analyze clusters
            cluster_analysis = self._analyze_user_clusters(clusters, user_data)
            
            return {
                'user_clusters': clusters.tolist(),
                'cluster_centers': cluster_centers.tolist(),
                'cluster_analysis': cluster_analysis,
                'segmentation_labels': self._generate_cluster_labels(cluster_analysis),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"User segmentation error: {e}")
            return {'error': str(e)}
    
    def track_learning_progress(self, user_id: str, 
                              learning_history: List[Dict]) -> Dict:
        """
        Track learning progress using time series analysis
        """
        try:
            # Prepare time series data
            progress_data = self._prepare_progress_data(learning_history)
            
            # Calculate progress metrics
            progress_metrics = self._calculate_progress_metrics(progress_data)
            
            # Predict future performance
            future_performance = self._predict_learning_performance(progress_data)
            
            # Identify learning patterns
            learning_patterns = self._identify_learning_patterns(progress_data)
            
            # Generate progress insights
            insights = self._generate_progress_insights(
                progress_metrics, future_performance, learning_patterns
            )
            
            return {
                'current_progress': progress_metrics,
                'predicted_performance': future_performance,
                'learning_patterns': learning_patterns,
                'insights': insights,
                'recommendations': self._generate_progress_recommendations(insights),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Learning progress tracking error: {e}")
            return {'error': str(e)}
    
    # Helper methods
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        import re
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_answer_features(self, question: str, answer: str, 
                               expected_skills: List[str]) -> np.ndarray:
        """Extract features from answer for classification"""
        features = []
        
        # Length features
        features.append(len(answer.split()))  # Word count
        features.append(len(answer))  # Character count
        
        # Semantic features
        semantic_similarity = self._calculate_semantic_similarity(question, answer)
        features.append(semantic_similarity)
        
        # Skill coverage
        skill_coverage = self._analyze_skill_coverage(answer, expected_skills)
        features.append(skill_coverage['coverage_percentage'])
        
        # Sentiment features
        sentiment = self.sentiment_analyzer.polarity_scores(answer)
        features.extend([sentiment['pos'], sentiment['neg'], sentiment['neu']])
        
        return np.array(features)
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using BERT"""
        try:
            # Tokenize texts
            inputs1 = self.tokenizer(text1, return_tensors='pt', truncation=True, padding=True)
            inputs2 = self.tokenizer(text2, return_tensors='pt', truncation=True, padding=True)
            
            # Get embeddings
            with torch.no_grad():
                embeddings1 = self.bert_model(**inputs1).last_hidden_state.mean(dim=1)
                embeddings2 = self.bert_model(**inputs2).last_hidden_state.mean(dim=1)
            
            # Calculate cosine similarity
            similarity = torch.cosine_similarity(embeddings1, embeddings2).item()
            return max(0.0, similarity)  # Ensure non-negative
            
        except Exception as e:
            self.logger.error(f"Semantic similarity calculation error: {e}")
            return 0.0
    
    def _analyze_skill_coverage(self, answer: str, expected_skills: List[str]) -> Dict:
        """Analyze how well answer covers expected skills"""
        covered_skills = []
        uncovered_skills = []
        
        answer_lower = answer.lower()
        
        for skill in expected_skills:
            if skill.lower() in answer_lower:
                covered_skills.append(skill)
            else:
                uncovered_skills.append(skill)
        
        coverage_percentage = (len(covered_skills) / len(expected_skills)) * 100 if expected_skills else 0
        
        return {
            'covered_skills': covered_skills,
            'uncovered_skills': uncovered_skills,
            'coverage_percentage': coverage_percentage
        }
    
    def _calculate_quality_score(self, semantic_score: float, skill_coverage: Dict,
                               sentiment_score: Dict, textblob_analysis) -> float:
        """Calculate overall answer quality score"""
        # Weight different components
        semantic_weight = 0.3
        skill_weight = 0.4
        sentiment_weight = 0.2
        subjectivity_weight = 0.1
        
        # Calculate weighted score
        semantic_component = semantic_score * semantic_weight
        skill_component = (skill_coverage['coverage_percentage'] / 100) * skill_weight
        sentiment_component = sentiment_score['pos'] * sentiment_weight
        subjectivity_component = (1 - abs(textblob_analysis.sentiment.subjectivity)) * subjectivity_weight
        
        total_score = semantic_component + skill_component + sentiment_component + subjectivity_component
        
        return min(1.0, max(0.0, total_score))
    
    def _classify_answer_quality(self, features: np.ndarray) -> str:
        """Classify answer quality level"""
        if len(self.training_data['answer_qualities']) > 0:
            return self.answer_quality_classifier.predict([features])[0]
        else:
            # Default classification based on feature values
            if features[2] > 0.7:  # High semantic similarity
                return 'excellent'
            elif features[2] > 0.5:
                return 'good'
            elif features[2] > 0.3:
                return 'average'
            else:
                return 'poor'
    
    def _generate_answer_feedback(self, quality_score: float, skill_coverage: Dict,
                                semantic_score: float) -> List[str]:
        """Generate feedback for answer improvement"""
        feedback = []
        
        if quality_score < 0.5:
            feedback.append("Consider providing more detailed and specific answers")
        
        if skill_coverage['coverage_percentage'] < 70:
            feedback.append(f"Try to include these skills: {', '.join(skill_coverage['uncovered_skills'])}")
        
        if semantic_score < 0.4:
            feedback.append("Your answer could be more relevant to the question asked")
        
        if quality_score > 0.8:
            feedback.append("Excellent answer! Well done!")
        
        return feedback
    
    def _prepare_skill_level_features(self, user_answers: List[Dict], 
                                    skill_domain: str) -> np.ndarray:
        """Prepare features for skill level classification"""
        features = []
        
        # Answer quality scores
        quality_scores = [answer.get('quality_score', 0) for answer in user_answers]
        features.extend([
            np.mean(quality_scores),  # Average quality
            np.std(quality_scores),   # Quality consistency
            max(quality_scores),       # Best performance
            min(quality_scores)        # Worst performance
        ])
        
        # Response time metrics
        response_times = [answer.get('response_time', 0) for answer in user_answers]
        features.extend([
            np.mean(response_times),   # Average response time
            np.std(response_times)     # Response time consistency
        ])
        
        # Skill coverage metrics
        skill_coverages = [answer.get('skill_coverage', {}).get('coverage_percentage', 0) 
                          for answer in user_answers]
        features.append(np.mean(skill_coverages))
        
        return np.array(features)
    
    def _default_skill_classification(self, features: np.ndarray) -> str:
        """Default skill level classification"""
        avg_quality = features[0]  # Average quality score
        
        if avg_quality > 0.8:
            return 'expert'
        elif avg_quality > 0.6:
            return 'advanced'
        elif avg_quality > 0.4:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _generate_skill_level_report(self, skill_level: str, probabilities: List[float],
                                   user_answers: List[Dict], skill_domain: str) -> Dict:
        """Generate comprehensive skill level report"""
        return {
            'skill_level': skill_level,
            'confidence_scores': {
                'beginner': probabilities[0],
                'intermediate': probabilities[1],
                'advanced': probabilities[2],
                'expert': probabilities[3]
            },
            'skill_domain': skill_domain,
            'total_answers': len(user_answers),
            'average_quality': np.mean([a.get('quality_score', 0) for a in user_answers]),
            'recommendations': self._generate_skill_level_recommendations(skill_level),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_skill_level_recommendations(self, skill_level: str) -> List[str]:
        """Generate recommendations based on skill level"""
        recommendations = {
            'beginner': [
                "Focus on fundamental concepts and terminology",
                "Practice basic exercises to build confidence",
                "Consider introductory courses and tutorials"
            ],
            'intermediate': [
                "Work on more complex problem-solving",
                "Explore advanced topics within the domain",
                "Practice real-world applications"
            ],
            'advanced': [
                "Tackle expert-level challenges",
                "Mentor others to reinforce knowledge",
                "Explore cutting-edge developments"
            ],
            'expert': [
                "Contribute to the field through research or innovation",
                "Develop new methodologies or approaches",
                "Share knowledge through teaching or writing"
            ]
        }
        
        return recommendations.get(skill_level, [])
    
    def _default_skill_categorization(self, responses: List[str]) -> List[str]:
        """Default skill categorization"""
        categories = []
        for response in responses:
            # Simple keyword-based categorization
            if any(word in response.lower() for word in ['code', 'programming', 'software']):
                categories.append('technical')
            elif any(word in response.lower() for word in ['team', 'communication', 'collaboration']):
                categories.append('soft_skills')
            elif any(word in response.lower() for word in ['manage', 'lead', 'organize']):
                categories.append('management')
            elif any(word in response.lower() for word in ['design', 'creative', 'innovate']):
                categories.append('creative')
            else:
                categories.append('general')
        
        return categories
    
    def _analyze_skill_distribution(self, categories: List[str], 
                                 probabilities: List[List[float]]) -> Dict:
        """Analyze distribution of skills across categories"""
        category_counts = {}
        category_confidences = {}
        
        for i, category in enumerate(categories):
            if category not in category_counts:
                category_counts[category] = 0
                category_confidences[category] = []
            
            category_counts[category] += 1
            category_confidences[category].append(max(probabilities[i]))
        
        # Calculate average confidence per category
        for category in category_confidences:
            category_confidences[category] = np.mean(category_confidences[category])
        
        return {
            'category_counts': category_counts,
            'category_confidences': category_confidences,
            'total_categories': len(category_counts),
            'dominant_category': max(category_counts, key=category_counts.get)
        }
    
    def _get_dominant_skills(self, skill_distribution: Dict) -> List[str]:
        """Get dominant skills from distribution analysis"""
        dominant_skills = []
        
        # Sort categories by count and confidence
        sorted_categories = sorted(
            skill_distribution['category_counts'].items(),
            key=lambda x: (x[1], skill_distribution['category_confidences'].get(x[0], 0)),
            reverse=True
        )
        
        # Return top 3 dominant skills
        for category, count in sorted_categories[:3]:
            confidence = skill_distribution['category_confidences'].get(category, 0)
            dominant_skills.append({
                'skill': category,
                'frequency': count,
                'confidence': confidence
            })
        
        return dominant_skills
    
    def _extract_user_profile_features(self, user_profile: Dict) -> np.ndarray:
        """Extract features from user profile for recommendations"""
        features = []
        
        # Demographic features
        features.append(user_profile.get('age', 25))
        features.append(1 if user_profile.get('education_level') == 'bachelor' else 0)
        features.append(1 if user_profile.get('education_level') == 'master' else 0)
        features.append(1 if user_profile.get('education_level') == 'phd' else 0)
        
        # Experience features
        features.append(user_profile.get('years_of_experience', 0))
        features.append(user_profile.get('previous_courses_count', 0))
        
        # Performance features
        features.append(user_profile.get('average_score', 0))
        features.append(user_profile.get('completion_rate', 0))
        
        return np.array(features)
    
    def _content_based_filtering(self, skill_gaps: List[str], 
                               user_features: np.ndarray) -> List[Dict]:
        """Content-based filtering for recommendations"""
        recommendations = []
        
        # Simple content-based recommendations based on skill gaps
        for skill_gap in skill_gaps:
            recommendation = {
                'type': 'content_based',
                'skill': skill_gap,
                'recommendation': f"Learn {skill_gap} fundamentals",
                'confidence': 0.8,
                'difficulty': 'beginner'
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _collaborative_filtering(self, user_profile: Dict) -> List[Dict]:
        """Collaborative filtering for recommendations"""
        # Placeholder for collaborative filtering
        # In practice, this would use user similarity and item ratings
        return []
    
    def _knowledge_graph_recommendations(self, skill_gaps: List[str]) -> List[Dict]:
        """Knowledge graph-based recommendations"""
        recommendations = []
        
        # Simple knowledge graph relationships
        skill_relationships = {
            'javascript': ['react', 'node.js', 'typescript'],
            'python': ['django', 'flask', 'data_science'],
            'react': ['javascript', 'redux', 'css'],
            'node.js': ['javascript', 'express', 'mongodb']
        }
        
        for skill_gap in skill_gaps:
            related_skills = skill_relationships.get(skill_gap.lower(), [])
            for related_skill in related_skills:
                recommendation = {
                    'type': 'knowledge_graph',
                    'skill': related_skill,
                    'recommendation': f"Learn {related_skill} as it relates to {skill_gap}",
                    'confidence': 0.7,
                    'difficulty': 'intermediate'
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _combine_recommendations(self, recommendation_lists: List[List[Dict]]) -> List[Dict]:
        """Combine recommendations from different sources"""
        combined = []
        
        for recommendations in recommendation_lists:
            combined.extend(recommendations)
        
        # Remove duplicates and sort by confidence
        unique_recommendations = []
        seen_skills = set()
        
        for rec in combined:
            skill_key = (rec['skill'], rec['type'])
            if skill_key not in seen_skills:
                unique_recommendations.append(rec)
                seen_skills.add(skill_key)
        
        # Sort by confidence
        unique_recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return unique_recommendations
    
    def _prioritize_recommendations(self, recommendations: List[Dict], 
                                  user_profile: Dict) -> List[Dict]:
        """Prioritize recommendations based on user profile"""
        # Simple prioritization based on user experience level
        experience_level = user_profile.get('years_of_experience', 0)
        
        prioritized = []
        for rec in recommendations:
            # Adjust difficulty based on experience
            if experience_level < 2:
                rec['priority'] = rec['confidence'] * 1.2 if rec['difficulty'] == 'beginner' else rec['confidence'] * 0.8
            elif experience_level < 5:
                rec['priority'] = rec['confidence']
            else:
                rec['priority'] = rec['confidence'] * 1.2 if rec['difficulty'] == 'advanced' else rec['confidence'] * 0.8
            
            prioritized.append(rec)
        
        # Sort by priority
        prioritized.sort(key=lambda x: x['priority'], reverse=True)
        
        return prioritized
    
    def _generate_learning_path(self, recommendations: List[Dict]) -> List[Dict]:
        """Generate structured learning path"""
        learning_path = []
        
        # Group recommendations by difficulty
        beginner_recs = [r for r in recommendations if r['difficulty'] == 'beginner']
        intermediate_recs = [r for r in recommendations if r['difficulty'] == 'intermediate']
        advanced_recs = [r for r in recommendations if r['difficulty'] == 'advanced']
        
        # Create learning path stages
        if beginner_recs:
            learning_path.append({
                'stage': 'Foundation',
                'recommendations': beginner_recs[:3],  # Top 3 beginner recommendations
                'estimated_duration': '2-4 weeks'
            })
        
        if intermediate_recs:
            learning_path.append({
                'stage': 'Intermediate',
                'recommendations': intermediate_recs[:3],
                'estimated_duration': '4-8 weeks'
            })
        
        if advanced_recs:
            learning_path.append({
                'stage': 'Advanced',
                'recommendations': advanced_recs[:3],
                'estimated_duration': '8-12 weeks'
            })
        
        return learning_path
    
    def _estimate_completion_time(self, recommendations: List[Dict]) -> str:
        """Estimate total completion time"""
        difficulty_multipliers = {
            'beginner': 1.0,
            'intermediate': 1.5,
            'advanced': 2.0
        }
        
        total_weeks = 0
        for rec in recommendations:
            base_weeks = 2  # Base time per recommendation
            multiplier = difficulty_multipliers.get(rec['difficulty'], 1.0)
            total_weeks += base_weeks * multiplier
        
        return f"{int(total_weeks)} weeks"
    
    def _generate_difficulty_progression(self, recommendations: List[Dict]) -> List[str]:
        """Generate difficulty progression description"""
        difficulties = [r['difficulty'] for r in recommendations]
        
        if difficulties.count('beginner') > 0:
            progression = ["Start with foundational concepts"]
        else:
            progression = ["Build on existing knowledge"]
        
        if difficulties.count('intermediate') > 0:
            progression.append("Progress to intermediate applications")
        
        if difficulties.count('advanced') > 0:
            progression.append("Master advanced techniques")
        
        return progression
    
    def _prepare_user_segmentation_features(self, user_data: List[Dict]) -> np.ndarray:
        """Prepare features for user segmentation"""
        features = []
        
        for user in user_data:
            user_features = [
                user.get('age', 25),
                user.get('years_of_experience', 0),
                user.get('average_score', 0),
                user.get('completion_rate', 0),
                user.get('courses_completed', 0),
                user.get('time_spent_learning', 0)
            ]
            features.append(user_features)
        
        return np.array(features)
    
    def _analyze_user_clusters(self, clusters: List[int], user_data: List[Dict]) -> Dict:
        """Analyze user clusters"""
        cluster_analysis = {}
        
        for cluster_id in set(clusters):
            cluster_users = [user_data[i] for i, c in enumerate(clusters) if c == cluster_id]
            
            if cluster_users:
                avg_age = np.mean([u.get('age', 25) for u in cluster_users])
                avg_experience = np.mean([u.get('years_of_experience', 0) for u in cluster_users])
                avg_score = np.mean([u.get('average_score', 0) for u in cluster_users])
                
                cluster_analysis[cluster_id] = {
                    'user_count': len(cluster_users),
                    'average_age': avg_age,
                    'average_experience': avg_experience,
                    'average_score': avg_score,
                    'characteristics': self._describe_cluster_characteristics(
                        avg_age, avg_experience, avg_score
                    )
                }
        
        return cluster_analysis
    
    def _describe_cluster_characteristics(self, avg_age: float, 
                                        avg_experience: float, avg_score: float) -> str:
        """Describe cluster characteristics"""
        if avg_experience < 2 and avg_score < 60:
            return "Beginner learners needing foundational support"
        elif avg_experience < 5 and avg_score > 70:
            return "Intermediate learners with good performance"
        elif avg_experience >= 5 and avg_score > 80:
            return "Experienced high-performers"
        else:
            return "Mixed experience learners"
    
    def _generate_cluster_labels(self, cluster_analysis: Dict) -> Dict:
        """Generate descriptive labels for clusters"""
        labels = {}
        
        for cluster_id, analysis in cluster_analysis.items():
            characteristics = analysis['characteristics']
            
            if 'Beginner' in characteristics:
                labels[cluster_id] = "New Learners"
            elif 'Intermediate' in characteristics:
                labels[cluster_id] = "Developing Professionals"
            elif 'Experienced' in characteristics:
                labels[cluster_id] = "Expert Practitioners"
            else:
                labels[cluster_id] = "Diverse Learners"
        
        return labels
    
    def _prepare_progress_data(self, learning_history: List[Dict]) -> pd.DataFrame:
        """Prepare learning progress data for analysis"""
        data = []
        
        for entry in learning_history:
            data.append({
                'date': entry.get('date'),
                'score': entry.get('score', 0),
                'time_spent': entry.get('time_spent', 0),
                'lessons_completed': entry.get('lessons_completed', 0),
                'skill_level': entry.get('skill_level', 'beginner')
            })
        
        return pd.DataFrame(data)
    
    def _calculate_progress_metrics(self, progress_data: pd.DataFrame) -> Dict:
        """Calculate progress metrics"""
        if progress_data.empty:
            return {}
        
        metrics = {
            'total_sessions': len(progress_data),
            'average_score': progress_data['score'].mean(),
            'score_trend': self._calculate_trend(progress_data['score']),
            'total_time_spent': progress_data['time_spent'].sum(),
            'average_session_time': progress_data['time_spent'].mean(),
            'lessons_completed_total': progress_data['lessons_completed'].sum(),
            'learning_velocity': self._calculate_learning_velocity(progress_data)
        }
        
        return metrics
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend in a time series"""
        if len(series) < 2:
            return 'stable'
        
        # Simple linear trend calculation
        x = np.arange(len(series))
        slope = np.polyfit(x, series, 1)[0]
        
        if slope > 0.1:
            return 'improving'
        elif slope < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_learning_velocity(self, progress_data: pd.DataFrame) -> float:
        """Calculate learning velocity (score improvement per unit time)"""
        if len(progress_data) < 2:
            return 0.0
        
        # Calculate score improvement over time
        score_change = progress_data['score'].iloc[-1] - progress_data['score'].iloc[0]
        time_change = progress_data['time_spent'].sum()
        
        return score_change / time_change if time_change > 0 else 0.0
    
    def _predict_learning_performance(self, progress_data: pd.DataFrame) -> Dict:
        """Predict future learning performance"""
        if progress_data.empty:
            return {}
        
        # Simple linear prediction
        scores = progress_data['score'].values
        if len(scores) < 3:
            return {'predicted_score': np.mean(scores), 'confidence': 0.5}
        
        # Linear regression for prediction
        x = np.arange(len(scores))
        coeffs = np.polyfit(x, scores, 1)
        
        # Predict next 3 sessions
        future_x = np.arange(len(scores), len(scores) + 3)
        predicted_scores = np.polyval(coeffs, future_x)
        
        return {
            'predicted_scores': predicted_scores.tolist(),
            'confidence': min(0.9, len(scores) / 10),  # Confidence based on data amount
            'trend': 'improving' if coeffs[0] > 0 else 'declining' if coeffs[0] < 0 else 'stable'
        }
    
    def _identify_learning_patterns(self, progress_data: pd.DataFrame) -> Dict:
        """Identify learning patterns from progress data"""
        patterns = {}
        
        if not progress_data.empty:
            # Session frequency pattern
            if 'date' in progress_data.columns:
                progress_data['date'] = pd.to_datetime(progress_data['date'])
                progress_data['days_between'] = progress_data['date'].diff().dt.days
                avg_days_between = progress_data['days_between'].mean()
                
                if avg_days_between < 2:
                    patterns['frequency'] = 'daily'
                elif avg_days_between < 7:
                    patterns['frequency'] = 'weekly'
                else:
                    patterns['frequency'] = 'sporadic'
            
            # Performance pattern
            score_std = progress_data['score'].std()
            if score_std < 10:
                patterns['consistency'] = 'consistent'
            elif score_std < 20:
                patterns['consistency'] = 'moderate'
            else:
                patterns['consistency'] = 'variable'
        
        return patterns
    
    def _generate_progress_insights(self, progress_metrics: Dict, 
                                  future_performance: Dict, 
                                  learning_patterns: Dict) -> List[str]:
        """Generate insights from progress analysis"""
        insights = []
        
        # Performance insights
        avg_score = progress_metrics.get('average_score', 0)
        if avg_score > 80:
            insights.append("Excellent performance! You're mastering the material.")
        elif avg_score > 60:
            insights.append("Good progress with room for improvement.")
        else:
            insights.append("Consider reviewing fundamentals to improve performance.")
        
        # Trend insights
        trend = future_performance.get('trend', 'stable')
        if trend == 'improving':
            insights.append("Your performance is consistently improving!")
        elif trend == 'declining':
            insights.append("Performance is declining - consider taking a break or reviewing material.")
        
        # Frequency insights
        frequency = learning_patterns.get('frequency', 'unknown')
        if frequency == 'daily':
            insights.append("Daily practice is showing great results!")
        elif frequency == 'weekly':
            insights.append("Weekly practice is maintaining steady progress.")
        else:
            insights.append("More consistent practice could improve results.")
        
        return insights
    
    def _generate_progress_recommendations(self, insights: List[str]) -> List[str]:
        """Generate recommendations based on progress insights"""
        recommendations = []
        
        for insight in insights:
            if 'excellent' in insight.lower():
                recommendations.append("Consider advanced topics to challenge yourself further.")
            elif 'room for improvement' in insight.lower():
                recommendations.append("Focus on weak areas and practice more regularly.")
            elif 'declining' in insight.lower():
                recommendations.append("Take a short break and return with fresh perspective.")
            elif 'consistent' in insight.lower():
                recommendations.append("Maintain your current learning schedule.")
            elif 'sporadic' in insight.lower():
                recommendations.append("Establish a more regular learning routine.")
        
        return recommendations

# Initialize global skill gap analysis system
skill_gap_system = SkillGapAnalysisSystem()
