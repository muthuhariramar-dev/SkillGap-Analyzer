"""
Performance Optimization System for Skills Gap Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

class PerformanceOptimizationSystem:
    """
    Advanced Performance Optimization System for Skills Gap Analysis
    Features: Performance Prediction, Optimization Recommendations, 
              Learning Path Optimization, Resource Allocation, Performance Analytics
    """

    def __init__(self):
        self.performance_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.optimization_recommender = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.learning_path_optimizer = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        self.resource_allocator = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Performance metrics
        self.performance_metrics = {
            'accuracy': 'Accuracy Score',
            'efficiency': 'Time Efficiency',
            'engagement': 'Engagement Level',
            'completion': 'Completion Rate',
            'satisfaction': 'Satisfaction Score',
            'skill_gain': 'Skill Improvement'
        }

    def analyze_performance(self, performance_data):
        """Analyze user performance comprehensively"""
        try:
            # Validate input data
            if not performance_data:
                return {'status': 'error', 'message': 'No performance data provided'}
            
            # Extract features
            features = self._extract_performance_features(performance_data)
            
            # Calculate performance metrics
            metrics = self._calculate_performance_metrics(performance_data)
            
            # Predict future performance
            prediction = self._predict_performance(features)
            
            # Generate optimization recommendations
            recommendations = self._generate_recommendations(features, metrics)
            
            # Optimize learning path
            learning_path = self._optimize_learning_path(features)
            
            # Resource allocation analysis
            resource_allocation = self._analyze_resource_allocation(features)
            
            # Performance trends
            trends = self._analyze_performance_trends(performance_data)
            
            # Benchmarking
            benchmarking = self._benchmark_performance(metrics)
            
            return {
                'status': 'success',
                'user_id': performance_data.get('user_id'),
                'analysis_timestamp': datetime.now().isoformat(),
                'performance_metrics': metrics,
                'performance_prediction': prediction,
                'optimization_recommendations': recommendations,
                'learning_path_optimization': learning_path,
                'resource_allocation': resource_allocation,
                'performance_trends': trends,
                'benchmarking': benchmarking,
                'performance_score': self._calculate_overall_score(metrics)
            }
        except Exception as e:
            print(f"Error analyzing performance: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _extract_performance_features(self, performance_data):
        """Extract features for performance analysis"""
        try:
            features = {}
            
            # Basic performance indicators
            features['total_activities'] = performance_data.get('total_activities', 0)
            features['completed_activities'] = performance_data.get('completed_activities', 0)
            features['average_score'] = performance_data.get('average_score', 0)
            features['time_spent'] = performance_data.get('time_spent', 0)
            features['engagement_score'] = performance_data.get('engagement_score', 0)
            
            # Learning behavior features
            features['learning_frequency'] = performance_data.get('learning_frequency', 0)
            features['preferred_difficulty'] = performance_data.get('preferred_difficulty', 0)
            features['learning_style_score'] = performance_data.get('learning_style_score', 0)
            features['collaboration_score'] = performance_data.get('collaboration_score', 0)
            
            # Skill-related features
            features['skill_diversity'] = performance_data.get('skill_diversity', 0)
            features['skill_improvement_rate'] = performance_data.get('skill_improvement_rate', 0)
            features['skill_gap_reduction'] = performance_data.get('skill_gap_reduction', 0)
            
            # Temporal features
            features['recent_performance'] = performance_data.get('recent_performance', 0)
            features['performance_trend'] = performance_data.get('performance_trend', 0)
            features['consistency_score'] = performance_data.get('consistency_score', 0)
            
            # Resource utilization
            features['resource_utilization'] = performance_data.get('resource_utilization', 0)
            features['help_seeking_frequency'] = performance_data.get('help_seeking_frequency', 0)
            
            return features
        except Exception as e:
            print(f"Error extracting performance features: {str(e)}")
            return {}

    def _calculate_performance_metrics(self, performance_data):
        """Calculate detailed performance metrics"""
        try:
            metrics = {}
            
            # Completion metrics
            total_activities = performance_data.get('total_activities', 1)
            completed_activities = performance_data.get('completed_activities', 0)
            metrics['completion_rate'] = completed_activities / total_activities
            
            # Accuracy metrics
            scores = performance_data.get('scores', [])
            if scores:
                metrics['average_score'] = np.mean(scores)
                metrics['score_variance'] = np.var(scores)
                metrics['score_trend'] = self._calculate_trend(scores)
            else:
                metrics['average_score'] = 0
                metrics['score_variance'] = 0
                metrics['score_trend'] = 0
            
            # Efficiency metrics
            time_spent = performance_data.get('time_spent', 0)
            activities_completed = performance_data.get('completed_activities', 1)
            metrics['time_efficiency'] = activities_completed / max(1, time_spent)
            
            # Engagement metrics
            engagement_data = performance_data.get('engagement_data', {})
            metrics['engagement_level'] = engagement_data.get('level', 0)
            metrics['interaction_frequency'] = engagement_data.get('frequency', 0)
            metrics['participation_score'] = engagement_data.get('participation', 0)
            
            # Learning metrics
            learning_data = performance_data.get('learning_data', {})
            metrics['learning_velocity'] = learning_data.get('velocity', 0)
            metrics['knowledge_retention'] = learning_data.get('retention', 0)
            metrics['skill_acquisition_rate'] = learning_data.get('acquisition_rate', 0)
            
            # Quality metrics
            quality_data = performance_data.get('quality_data', {})
            metrics['quality_score'] = quality_data.get('score', 0)
            metrics['improvement_rate'] = quality_data.get('improvement_rate', 0)
            metrics['mastery_level'] = quality_data.get('mastery', 0)
            
            return metrics
        except Exception as e:
            print(f"Error calculating performance metrics: {str(e)}")
            return {}

    def _calculate_trend(self, values):
        """Calculate trend in a series of values"""
        try:
            if len(values) < 2:
                return 0
            
            x = np.arange(len(values))
            slope = np.polyfit(x, values, 1)[0]
            
            # Normalize trend
            return np.tanh(slope)  # Keep between -1 and 1
        except Exception as e:
            print(f"Error calculating trend: {str(e)}")
            return 0

    def _predict_performance(self, features):
        """Predict future performance"""
        try:
            if not self.is_trained:
                # Simple rule-based prediction
                return self._rule_based_prediction(features)
            
            # Prepare features for prediction
            feature_vector = self._prepare_feature_vector(features)
            
            # Predict performance
            predicted_score = self.performance_predictor.predict([feature_vector])[0]
            
            # Predict performance trajectory
            trajectory = self._predict_trajectory(features)
            
            # Confidence in prediction
            confidence = self._calculate_prediction_confidence(features)
            
            return {
                'predicted_score': max(0, min(100, predicted_score)),
                'performance_trajectory': trajectory,
                'confidence': confidence,
                'prediction_horizon': '30_days',
                'key_factors': self._identify_key_factors(features)
            }
        except Exception as e:
            print(f"Error predicting performance: {str(e)}")
            return {'predicted_score': 50, 'confidence': 0.5}

    def _rule_based_prediction(self, features):
        """Rule-based performance prediction"""
        try:
            base_score = 50
            
            # Adjust based on current performance
            avg_score = features.get('average_score', 50)
            base_score += (avg_score - 50) * 0.6
            
            # Adjust based on improvement rate
            improvement_rate = features.get('skill_improvement_rate', 0)
            base_score += improvement_rate * 20
            
            # Adjust based on engagement
            engagement = features.get('engagement_score', 0)
            base_score += (engagement - 50) * 0.3
            
            # Adjust based on consistency
            consistency = features.get('consistency_score', 0)
            base_score += (consistency - 50) * 0.2
            
            predicted_score = max(0, min(100, base_score))
            
            return {
                'predicted_score': predicted_score,
                'performance_trajectory': 'stable',
                'confidence': 0.7,
                'prediction_horizon': '30_days',
                'key_factors': ['current_performance', 'improvement_rate', 'engagement']
            }
        except Exception as e:
            print(f"Error in rule-based prediction: {str(e)}")
            return {'predicted_score': 50, 'confidence': 0.5}

    def _prepare_feature_vector(self, features):
        """Prepare feature vector for ML models"""
        try:
            feature_order = [
                'total_activities', 'completed_activities', 'average_score', 'time_spent',
                'engagement_score', 'learning_frequency', 'preferred_difficulty',
                'learning_style_score', 'collaboration_score', 'skill_diversity',
                'skill_improvement_rate', 'skill_gap_reduction', 'recent_performance',
                'performance_trend', 'consistency_score', 'resource_utilization',
                'help_seeking_frequency'
            ]
            
            feature_vector = []
            for feature in feature_order:
                feature_vector.append(features.get(feature, 0))
            
            return feature_vector
        except Exception as e:
            print(f"Error preparing feature vector: {str(e)}")
            return [0] * 17

    def _predict_trajectory(self, features):
        """Predict performance trajectory"""
        try:
            current_trend = features.get('performance_trend', 0)
            improvement_rate = features.get('skill_improvement_rate', 0)
            consistency = features.get('consistency_score', 50)
            
            if current_trend > 0.2 and improvement_rate > 0.1:
                trajectory = 'improving'
            elif current_trend < -0.2 and improvement_rate < -0.1:
                trajectory = 'declining'
            elif consistency > 70:
                trajectory = 'stable'
            else:
                trajectory = 'fluctuating'
            
            return trajectory
        except Exception as e:
            print(f"Error predicting trajectory: {str(e)}")
            return 'stable'

    def _calculate_prediction_confidence(self, features):
        """Calculate confidence in performance prediction"""
        try:
            # More data points = higher confidence
            total_activities = features.get('total_activities', 0)
            data_confidence = min(1.0, total_activities / 50)
            
            # Consistency increases confidence
            consistency = features.get('consistency_score', 50) / 100
            
            # Recent performance relevance
            recent_performance = features.get('recent_performance', 0)
            relevance_confidence = abs(recent_performance - 50) / 50
            
            # Overall confidence
            confidence = (data_confidence + consistency + relevance_confidence) / 3
            
            return max(0.1, min(1.0, confidence))
        except Exception as e:
            print(f"Error calculating prediction confidence: {str(e)}")
            return 0.5

    def _identify_key_factors(self, features):
        """Identify key factors affecting performance"""
        try:
            factor_scores = {}
            
            # Calculate factor importance
            factor_scores['current_performance'] = features.get('average_score', 0) / 100
            factor_scores['engagement'] = features.get('engagement_score', 0) / 100
            factor_scores['consistency'] = features.get('consistency_score', 0) / 100
            factor_scores['improvement_rate'] = min(1.0, features.get('skill_improvement_rate', 0) * 10)
            factor_scores['learning_frequency'] = min(1.0, features.get('learning_frequency', 0) / 10)
            
            # Sort by importance
            sorted_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)
            
            return [factor[0] for factor in sorted_factors[:5]]
        except Exception as e:
            print(f"Error identifying key factors: {str(e)}")
            return []

    def _generate_recommendations(self, features, metrics):
        """Generate optimization recommendations"""
        try:
            recommendations = []
            
            # Performance-based recommendations
            avg_score = metrics.get('average_score', 0)
            if avg_score < 60:
                recommendations.append({
                    'type': 'performance_improvement',
                    'priority': 'high',
                    'action': 'Focus on foundational concepts',
                    'description': 'Your scores indicate need for stronger foundation',
                    'expected_impact': '15-20 points improvement'
                })
            
            # Engagement-based recommendations
            engagement = metrics.get('engagement_level', 0)
            if engagement < 50:
                recommendations.append({
                    'type': 'engagement_boost',
                    'priority': 'medium',
                    'action': 'Try interactive learning activities',
                    'description': 'Increase engagement through interactive content',
                    'expected_impact': '10-15% engagement increase'
                })
            
            # Efficiency-based recommendations
            efficiency = metrics.get('time_efficiency', 0)
            if efficiency < 0.5:
                recommendations.append({
                    'type': 'efficiency_improvement',
                    'priority': 'medium',
                    'action': 'Optimize study time management',
                    'description': 'Improve time efficiency for better learning outcomes',
                    'expected_impact': '20-30% efficiency gain'
                })
            
            # Learning path recommendations
            completion_rate = metrics.get('completion_rate', 0)
            if completion_rate < 0.7:
                recommendations.append({
                    'type': 'completion_optimization',
                    'priority': 'high',
                    'action': 'Break down complex topics',
                    'description': 'Improve completion rate with smaller, manageable tasks',
                    'expected_impact': '15-25% completion increase'
                })
            
            # Skill-specific recommendations
            skill_improvement = metrics.get('skill_acquisition_rate', 0)
            if skill_improvement < 0.3:
                recommendations.append({
                    'type': 'skill_acceleration',
                    'priority': 'medium',
                    'action': 'Focus on high-impact skills',
                    'description': 'Prioritize skills with highest ROI',
                    'expected_impact': '25-35% faster skill acquisition'
                })
            
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []

    def _optimize_learning_path(self, features):
        """Optimize learning path based on performance"""
        try:
            optimization = {}
            
            # Difficulty optimization
            current_difficulty = features.get('preferred_difficulty', 0.5)
            performance_score = features.get('average_score', 50)
            
            if performance_score > 80:
                recommended_difficulty = min(1.0, current_difficulty + 0.2)
                optimization['difficulty_adjustment'] = 'increase'
            elif performance_score < 60:
                recommended_difficulty = max(0.1, current_difficulty - 0.2)
                optimization['difficulty_adjustment'] = 'decrease'
            else:
                recommended_difficulty = current_difficulty
                optimization['difficulty_adjustment'] = 'maintain'
            
            optimization['recommended_difficulty'] = recommended_difficulty
            
            # Pace optimization
            learning_frequency = features.get('learning_frequency', 0)
            if learning_frequency < 3:
                optimization['recommended_pace'] = 'increase_frequency'
                optimization['target_frequency'] = 5
            elif learning_frequency > 10:
                optimization['recommended_pace'] = 'decrease_frequency'
                optimization['target_frequency'] = 7
            else:
                optimization['recommended_pace'] = 'maintain'
                optimization['target_frequency'] = learning_frequency
            
            # Content type optimization
            learning_style = features.get('learning_style_score', 0)
            if learning_style > 0.7:
                optimization['recommended_content_type'] = 'visual'
            elif learning_style < 0.3:
                optimization['recommended_content_type'] = 'textual'
            else:
                optimization['recommended_content_type'] = 'mixed'
            
            # Collaboration optimization
            collaboration_score = features.get('collaboration_score', 0)
            if collaboration_score > 0.7:
                optimization['collaboration_level'] = 'high'
            elif collaboration_score < 0.3:
                optimization['collaboration_level'] = 'low'
            else:
                optimization['collaboration_level'] = 'moderate'
            
            return optimization
        except Exception as e:
            print(f"Error optimizing learning path: {str(e)}")
            return {}

    def _analyze_resource_allocation(self, features):
        """Analyze optimal resource allocation"""
        try:
            allocation = {}
            
            # Time allocation
            total_time = features.get('time_spent', 100)
            performance_score = features.get('average_score', 50)
            
            if performance_score < 60:
                allocation['study_time'] = total_time * 1.3
                allocation['practice_time'] = total_time * 0.8
                allocation['review_time'] = total_time * 1.2
            elif performance_score > 80:
                allocation['study_time'] = total_time * 0.8
                allocation['practice_time'] = total_time * 1.2
                allocation['review_time'] = total_time * 0.9
            else:
                allocation['study_time'] = total_time
                allocation['practice_time'] = total_time
                allocation['review_time'] = total_time
            
            # Resource type allocation
            skill_diversity = features.get('skill_diversity', 0)
            if skill_diversity > 0.7:
                allocation['resource_diversity'] = 'high'
                allocation['specialized_resources'] = 0.3
                allocation['general_resources'] = 0.7
            else:
                allocation['resource_diversity'] = 'focused'
                allocation['specialized_resources'] = 0.7
                allocation['general_resources'] = 0.3
            
            # Help resource allocation
            help_seeking = features.get('help_seeking_frequency', 0)
            if help_seeking < 0.2:
                allocation['help_resources'] = 'increase'
                allocation['recommended_help_frequency'] = 0.4
            elif help_seeking > 0.8:
                allocation['help_resources'] = 'decrease'
                allocation['recommended_help_frequency'] = 0.5
            else:
                allocation['help_resources'] = 'maintain'
                allocation['recommended_help_frequency'] = help_seeking
            
            return allocation
        except Exception as e:
            print(f"Error analyzing resource allocation: {str(e)}")
            return {}

    def _analyze_performance_trends(self, performance_data):
        """Analyze performance trends over time"""
        try:
            trends = {}
            
            # Score trends
            scores = performance_data.get('scores', [])
            if len(scores) >= 3:
                trends['score_trend'] = self._calculate_trend(scores)
                trends['score_volatility'] = np.std(scores)
                trends['recent_average'] = np.mean(scores[-3:])
                trends['overall_average'] = np.mean(scores)
            else:
                trends['score_trend'] = 0
                trends['score_volatility'] = 0
                trends['recent_average'] = np.mean(scores) if scores else 0
                trends['overall_average'] = np.mean(scores) if scores else 0
            
            # Engagement trends
            engagement_history = performance_data.get('engagement_history', [])
            if len(engagement_history) >= 3:
                trends['engagement_trend'] = self._calculate_trend(engagement_history)
                trends['engagement_volatility'] = np.std(engagement_history)
            else:
                trends['engagement_trend'] = 0
                trends['engagement_volatility'] = 0
            
            # Time spent trends
            time_history = performance_data.get('time_history', [])
            if len(time_history) >= 3:
                trends['time_trend'] = self._calculate_trend(time_history)
                trends['time_efficiency_trend'] = self._calculate_time_efficiency_trend(time_history, scores)
            else:
                trends['time_trend'] = 0
                trends['time_efficiency_trend'] = 0
            
            # Overall trend classification
            trends['overall_trend'] = self._classify_overall_trend(trends)
            
            return trends
        except Exception as e:
            print(f"Error analyzing performance trends: {str(e)}")
            return {}

    def _calculate_time_efficiency_trend(self, time_history, scores):
        """Calculate time efficiency trend"""
        try:
            if len(time_history) != len(scores) or len(time_history) < 2:
                return 0
            
            efficiency_scores = []
            for time, score in zip(time_history, scores):
                if time > 0:
                    efficiency = score / time
                    efficiency_scores.append(efficiency)
            
            if len(efficiency_scores) >= 2:
                return self._calculate_trend(efficiency_scores)
            
            return 0
        except Exception as e:
            print(f"Error calculating time efficiency trend: {str(e)}")
            return 0

    def _classify_overall_trend(self, trends):
        """Classify overall performance trend"""
        try:
            score_trend = trends.get('score_trend', 0)
            engagement_trend = trends.get('engagement_trend', 0)
            efficiency_trend = trends.get('time_efficiency_trend', 0)
            
            avg_trend = (score_trend + engagement_trend + efficiency_trend) / 3
            
            if avg_trend > 0.1:
                return 'improving'
            elif avg_trend < -0.1:
                return 'declining'
            else:
                return 'stable'
        except Exception as e:
            print(f"Error classifying overall trend: {str(e)}")
            return 'stable'

    def _benchmark_performance(self, metrics):
        """Benchmark performance against standards"""
        try:
            benchmarks = {}
            
            # Define benchmark standards
            standards = {
                'completion_rate': {'excellent': 0.9, 'good': 0.75, 'average': 0.6, 'poor': 0.4},
                'average_score': {'excellent': 90, 'good': 80, 'average': 70, 'poor': 60},
                'time_efficiency': {'excellent': 1.0, 'good': 0.8, 'average': 0.6, 'poor': 0.4},
                'engagement_level': {'excellent': 80, 'good': 70, 'average': 60, 'poor': 50},
                'learning_velocity': {'excellent': 0.8, 'good': 0.6, 'average': 0.4, 'poor': 0.2},
                'quality_score': {'excellent': 85, 'good': 75, 'average': 65, 'poor': 55}
            }
            
            # Compare against standards
            for metric, value in metrics.items():
                if metric in standards:
                    level_standards = standards[metric]
                    
                    if value >= level_standards['excellent']:
                        level = 'excellent'
                        percentile = 90 + (value - level_standards['excellent']) * 10
                    elif value >= level_standards['good']:
                        level = 'good'
                        percentile = 70 + (value - level_standards['good']) * 20
                    elif value >= level_standards['average']:
                        level = 'average'
                        percentile = 50 + (value - level_standards['average']) * 20
                    else:
                        level = 'poor'
                        percentile = max(10, value / level_standards['poor'] * 40)
                    
                    benchmarks[metric] = {
                        'value': value,
                        'level': level,
                        'percentile': min(99, percentile),
                        'standard': level_standards
                    }
            
            # Overall benchmark
            if benchmarks:
                avg_percentile = np.mean([b['percentile'] for b in benchmarks.values()])
                benchmarks['overall'] = {
                    'percentile': avg_percentile,
                    'level': self._percentile_to_level(avg_percentile),
                    'metrics_count': len(benchmarks) - 1
                }
            
            return benchmarks
        except Exception as e:
            print(f"Error benchmarking performance: {str(e)}")
            return {}

    def _percentile_to_level(self, percentile):
        """Convert percentile to performance level"""
        if percentile >= 90:
            return 'excellent'
        elif percentile >= 70:
            return 'good'
        elif percentile >= 50:
            return 'average'
        else:
            return 'poor'

    def _calculate_overall_score(self, metrics):
        """Calculate overall performance score"""
        try:
            if not metrics:
                return 50
            
            # Weight different metrics
            weights = {
                'completion_rate': 0.2,
                'average_score': 0.25,
                'time_efficiency': 0.15,
                'engagement_level': 0.15,
                'learning_velocity': 0.15,
                'quality_score': 0.1
            }
            
            weighted_score = 0
            total_weight = 0
            
            for metric, weight in weights.items():
                if metric in metrics:
                    value = metrics[metric]
                    # Normalize to 0-100 scale
                    if metric == 'completion_rate':
                        normalized_value = value * 100
                    elif metric == 'time_efficiency':
                        normalized_value = min(100, value * 100)
                    else:
                        normalized_value = min(100, value)
                    
                    weighted_score += normalized_value * weight
                    total_weight += weight
            
            if total_weight > 0:
                overall_score = weighted_score / total_weight
            else:
                overall_score = 50
            
            return max(0, min(100, overall_score))
        except Exception as e:
            print(f"Error calculating overall score: {str(e)}")
            return 50

    def train_models(self, training_data):
        """Train performance optimization models"""
        try:
            # Prepare training data
            X = []
            y_performance = []
            y_optimization = []
            y_learning_path = []
            y_resource_allocation = []
            
            for item in training_data:
                features = self._extract_performance_features(item)
                if features:
                    feature_vector = self._prepare_feature_vector(features)
                    X.append(feature_vector)
                    
                    y_performance.append(item.get('future_performance', 50))
                    y_optimization.append(item.get('optimization_score', 50))
                    y_learning_path.append(item.get('learning_path_score', 50))
                    y_resource_allocation.append(item.get('resource_score', 50))
            
            if len(X) < 20:
                return {'status': 'error', 'message': 'Insufficient training data'}
            
            X = np.array(X)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train models
            self.performance_predictor.fit(X_scaled, y_performance)
            self.optimization_recommender.fit(X_scaled, y_optimization)
            self.learning_path_optimizer.fit(X_scaled, y_learning_path)
            self.resource_allocator.fit(X_scaled, y_resource_allocation)
            
            self.is_trained = True
            
            return {
                'status': 'success',
                'training_samples': len(X),
                'models_trained': ['performance_predictor', 'optimization_recommender', 'learning_path_optimizer', 'resource_allocator']
            }
        except Exception as e:
            print(f"Error training models: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def save_model(self, filepath):
        """Save trained models"""
        try:
            model_data = {
                'performance_predictor': self.performance_predictor,
                'optimization_recommender': self.optimization_recommender,
                'learning_path_optimizer': self.learning_path_optimizer,
                'resource_allocator': self.resource_allocator,
                'scaler': self.scaler,
                'performance_metrics': self.performance_metrics,
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
            
            self.performance_predictor = model_data['performance_predictor']
            self.optimization_recommender = model_data['optimization_recommender']
            self.learning_path_optimizer = model_data['learning_path_optimizer']
            self.resource_allocator = model_data['resource_allocator']
            self.scaler = model_data['scaler']
            self.performance_metrics = model_data['performance_metrics']
            self.is_trained = model_data['is_trained']
            
            return {'status': 'success', 'message': f'Model loaded from {filepath}'}
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the performance optimization system
    performance_optimizer = PerformanceOptimizationSystem()
    
    # Sample performance data
    sample_performance = {
        'user_id': 'user_123',
        'total_activities': 25,
        'completed_activities': 20,
        'average_score': 75,
        'time_spent': 120,
        'engagement_score': 70,
        'learning_frequency': 5,
        'preferred_difficulty': 0.6,
        'learning_style_score': 0.7,
        'collaboration_score': 0.8,
        'skill_diversity': 0.6,
        'skill_improvement_rate': 0.15,
        'skill_gap_reduction': 0.2,
        'recent_performance': 78,
        'performance_trend': 0.1,
        'consistency_score': 75,
        'resource_utilization': 0.7,
        'help_seeking_frequency': 0.3,
        'scores': [65, 70, 72, 75, 78, 80],
        'engagement_history': [60, 65, 68, 70, 72],
        'time_history': [25, 22, 20, 18, 20]
    }
    
    # Analyze performance
    analysis_result = performance_optimizer.analyze_performance(sample_performance)
    print("Performance Analysis Result:", json.dumps(analysis_result, indent=2, default=str))
