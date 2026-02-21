"""
User Behavior Analytics System for Skills Gap Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, silhouette_score
import joblib
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

class UserBehaviorAnalytics:
    """
    Advanced User Behavior Analytics System for Skills Gap Analysis
    Features: Predictive Modeling, User Clustering, Time Series Analysis,
              Engagement Patterns, Learning Path Prediction
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.user_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.performance_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.user_clustering = KMeans(n_clusters=5, random_state=42)
        self.density_clustering = DBSCAN(eps=0.5, min_samples=5)
        self.is_trained = False

    def preprocess_user_data(self, user_data):
        """Preprocess user behavior data for analysis"""
        try:
            df = pd.DataFrame(user_data)
            
            # Handle missing values
            df.fillna(0, inplace=True)
            
            # Encode categorical variables
            if 'user_type' in df.columns:
                df['user_type_encoded'] = self.label_encoder.fit_transform(df['user_type'])
            
            # Create time-based features
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour_of_day'] = df['timestamp'].dt.hour
                df['day_of_week'] = df['timestamp'].dt.dayofweek
            
            return df
        except Exception as e:
            print(f"Error preprocessing user data: {str(e)}")
            return None

    def extract_behavioral_features(self, df):
        """Extract behavioral features from user data"""
        try:
            features = []
            
            for _, user_group in df.groupby('user_id'):
                user_features = {}
                
                # Time-based features
                user_features['avg_session_duration'] = user_group['session_duration'].mean()
                user_features['total_sessions'] = len(user_group)
                user_features['sessions_per_week'] = len(user_group) / max(1, (user_group['timestamp'].max() - user_group['timestamp'].min()).days / 7)
                
                # Engagement features
                user_features['avg_interaction_rate'] = user_group['interactions'].mean()
                user_features['completion_rate'] = user_group['completed'].mean()
                user_features['bounce_rate'] = (user_group['session_duration'] < 60).mean()
                
                # Performance features
                user_features['avg_score'] = user_group['score'].mean()
                user_features['score_variance'] = user_group['score'].var()
                user_features['improvement_rate'] = self._calculate_improvement_rate(user_group)
                
                # Activity patterns
                user_features['peak_activity_hour'] = user_group.groupby(user_group['timestamp'].dt.hour).size().idxmax()
                user_features['activity_regularity'] = self._calculate_activity_regularity(user_group)
                
                features.append(user_features)
            
            return pd.DataFrame(features)
        except Exception as e:
            print(f"Error extracting behavioral features: {str(e)}")
            return None

    def _calculate_improvement_rate(self, user_data):
        """Calculate learning improvement rate"""
        try:
            sorted_data = user_data.sort_values('timestamp')
            if len(sorted_data) < 2:
                return 0
            
            scores = sorted_data['score'].values
            return np.mean(np.diff(scores))
        except:
            return 0

    def _calculate_activity_regularity(self, user_data):
        """Calculate activity regularity score"""
        try:
            daily_activity = user_data.groupby(user_data['timestamp'].dt.date).size()
            if len(daily_activity) < 2:
                return 0
            
            return 1 - (daily_activity.std() / max(1, daily_activity.mean()))
        except:
            return 0

    def train_user_classifier(self, features_df, labels):
        """Train user behavior classifier"""
        try:
            # Prepare features
            feature_columns = [col for col in features_df.columns if col not in ['user_id', 'timestamp']]
            X = features_df[feature_columns].fillna(0)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train classifier
            self.user_classifier.fit(X_scaled, labels)
            self.is_trained = True
            
            return {
                'status': 'success',
                'accuracy': self.user_classifier.score(X_scaled, labels),
                'feature_importance': dict(zip(feature_columns, self.user_classifier.feature_importances_))
            }
        except Exception as e:
            print(f"Error training user classifier: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def predict_user_behavior(self, user_features):
        """Predict user behavior patterns"""
        try:
            if not self.is_trained:
                return {'status': 'error', 'message': 'Model not trained'}
            
            # Prepare features
            feature_df = pd.DataFrame([user_features])
            feature_columns = [col for col in feature_df.columns if col not in ['user_id', 'timestamp']]
            X = feature_df[feature_columns].fillna(0)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make predictions
            prediction = self.user_classifier.predict(X_scaled)[0]
            probabilities = self.user_classifier.predict_proba(X_scaled)[0]
            
            return {
                'status': 'success',
                'predicted_behavior': prediction,
                'confidence': max(probabilities),
                'probabilities': dict(zip(self.user_classifier.classes_, probabilities))
            }
        except Exception as e:
            print(f"Error predicting user behavior: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def cluster_users(self, features_df):
        """Cluster users based on behavior patterns"""
        try:
            # Prepare features
            feature_columns = [col for col in features_df.columns if col not in ['user_id', 'timestamp']]
            X = features_df[feature_columns].fillna(0)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # K-means clustering
            kmeans_labels = self.user_clustering.fit_predict(X_scaled)
            kmeans_score = silhouette_score(X_scaled, kmeans_labels)
            
            # DBSCAN clustering
            dbscan_labels = self.density_clustering.fit_predict(X_scaled)
            n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
            
            return {
                'status': 'success',
                'kmeans_clusters': kmeans_labels.tolist(),
                'kmeans_silhouette_score': kmeans_score,
                'dbscan_clusters': dbscan_labels.tolist(),
                'dbscan_n_clusters': n_clusters_dbscan,
                'cluster_centers': self.user_clustering.cluster_centers_.tolist()
            }
        except Exception as e:
            print(f"Error clustering users: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def analyze_engagement_patterns(self, user_data):
        """Analyze user engagement patterns over time"""
        try:
            df = pd.DataFrame(user_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Time-based analysis
            hourly_engagement = df.groupby(df['timestamp'].dt.hour)['engagement_score'].mean()
            daily_engagement = df.groupby(df['timestamp'].dt.date)['engagement_score'].mean()
            weekly_engagement = df.groupby(df['timestamp'].dt.isocalendar().week)['engagement_score'].mean()
            
            # Pattern detection
            patterns = {
                'peak_hours': hourly_engagement.nlargest(3).index.tolist(),
                'low_hours': hourly_engagement.nsmallest(3).index.tolist(),
                'peak_days': self._get_peak_days(df),
                'engagement_trend': self._calculate_trend(daily_engagement),
                'seasonal_patterns': self._detect_seasonal_patterns(df)
            }
            
            return {
                'status': 'success',
                'hourly_patterns': hourly_engagement.to_dict(),
                'daily_patterns': daily_engagement.to_dict(),
                'weekly_patterns': weekly_engagement.to_dict(),
                'insights': patterns
            }
        except Exception as e:
            print(f"Error analyzing engagement patterns: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _get_peak_days(self, df):
        """Get peak engagement days"""
        try:
            daily_engagement = df.groupby(df['timestamp'].dt.day_name())['engagement_score'].mean()
            return daily_engagement.nlargest(3).index.tolist()
        except:
            return []

    def _calculate_trend(self, series):
        """Calculate trend direction"""
        try:
            if len(series) < 2:
                return 'stable'
            
            correlation = np.corrcoef(range(len(series)), series)[0, 1]
            if correlation > 0.1:
                return 'increasing'
            elif correlation < -0.1:
                return 'decreasing'
            else:
                return 'stable'
        except:
            return 'stable'

    def _detect_seasonal_patterns(self, df):
        """Detect seasonal patterns in engagement"""
        try:
            patterns = {}
            
            # Monthly patterns
            monthly_engagement = df.groupby(df['timestamp'].dt.month)['engagement_score'].mean()
            patterns['monthly_peak'] = monthly_engagement.idxmax()
            patterns['monthly_low'] = monthly_engagement.idxmin()
            
            # Weekly patterns
            weekly_engagement = df.groupby(df['timestamp'].dt.dayofweek)['engagement_score'].mean()
            patterns['weekend_vs_weekday'] = {
                'weekend_avg': weekly_engagement[[5, 6]].mean(),
                'weekday_avg': weekly_engagement[[0, 1, 2, 3, 4]].mean()
            }
            
            return patterns
        except:
            return {}

    def predict_learning_path(self, user_data, skill_data):
        """Predict optimal learning path for user"""
        try:
            user_df = pd.DataFrame(user_data)
            skill_df = pd.DataFrame(skill_data)
            
            # Analyze user strengths and weaknesses
            user_profile = self._analyze_user_profile(user_df)
            
            # Match skills to user profile
            recommended_skills = self._recommend_skills(user_profile, skill_df)
            
            # Generate learning path
            learning_path = self._generate_learning_path(recommended_skills, user_profile)
            
            return {
                'status': 'success',
                'user_profile': user_profile,
                'recommended_skills': recommended_skills,
                'learning_path': learning_path,
                'estimated_completion_time': self._estimate_completion_time(learning_path)
            }
        except Exception as e:
            print(f"Error predicting learning path: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _analyze_user_profile(self, user_df):
        """Analyze user learning profile"""
        try:
            profile = {
                'learning_style': self._determine_learning_style(user_df),
                'skill_level': user_df['skill_level'].mean(),
                'preferred_difficulty': user_df['difficulty_preference'].mode().iloc[0] if not user_df['difficulty_preference'].mode().empty else 'medium',
                'completion_rate': user_df['completed'].mean(),
                'avg_time_per_skill': user_df['time_spent'].mean(),
                'strength_areas': self._identify_strength_areas(user_df),
                'improvement_areas': self._identify_improvement_areas(user_df)
            }
            return profile
        except Exception as e:
            print(f"Error analyzing user profile: {str(e)}")
            return {}

    def _determine_learning_style(self, user_df):
        """Determine user learning style"""
        try:
            # Simple heuristic based on interaction patterns
            visual_score = user_df['visual_interactions'].mean()
            textual_score = user_df['textual_interactions'].mean()
            interactive_score = user_df['interactive_interactions'].mean()
            
            max_score = max(visual_score, textual_score, interactive_score)
            
            if max_score == visual_score:
                return 'visual'
            elif max_score == interactive_score:
                return 'interactive'
            else:
                return 'textual'
        except:
            return 'mixed'

    def _identify_strength_areas(self, user_df):
        """Identify user strength areas"""
        try:
            strength_scores = user_df.groupby('skill_category')['score'].mean()
            return strength_scores.nlargest(3).to_dict()
        except:
            return {}

    def _identify_improvement_areas(self, user_df):
        """Identify areas needing improvement"""
        try:
            improvement_scores = user_df.groupby('skill_category')['score'].mean()
            return improvement_scores.nsmallest(3).to_dict()
        except:
            return {}

    def _recommend_skills(self, user_profile, skill_df):
        """Recommend skills based on user profile"""
        try:
            # Filter skills based on user level and preferences
            suitable_skills = skill_df[
                (skill_df['difficulty'] == user_profile['preferred_difficulty']) |
                (skill_df['difficulty'] == 'medium')
            ]
            
            # Sort by relevance and user profile match
            suitable_skills = suitable_skills.sort_values('relevance_score', ascending=False)
            
            return suitable_skills.head(10).to_dict('records')
        except:
            return []

    def _generate_learning_path(self, skills, user_profile):
        """Generate optimized learning path"""
        try:
            # Sort skills by prerequisites and difficulty
            learning_path = []
            
            for skill in skills:
                path_item = {
                    'skill_id': skill['id'],
                    'skill_name': skill['name'],
                    'difficulty': skill['difficulty'],
                    'estimated_time': skill['estimated_time'],
                    'prerequisites': skill.get('prerequisites', []),
                    'learning_resources': skill.get('resources', []),
                    'adaptations': self._generate_adaptations(skill, user_profile)
                }
                learning_path.append(path_item)
            
            return learning_path
        except:
            return []

    def _generate_adaptations(self, skill, user_profile):
        """Generate personalized adaptations for skill"""
        try:
            adaptations = {}
            
            # Learning style adaptations
            if user_profile['learning_style'] == 'visual':
                adaptations['content_type'] = 'video-heavy'
            elif user_profile['learning_style'] == 'interactive':
                adaptations['content_type'] = 'hands-on'
            else:
                adaptations['content_type'] = 'text-heavy'
            
            # Difficulty adaptations
            if user_profile['skill_level'] < skill['difficulty_level']:
                adaptations['difficulty_adjustment'] = 'easier'
            elif user_profile['skill_level'] > skill['difficulty_level']:
                adaptations['difficulty_adjustment'] = 'harder'
            else:
                adaptations['difficulty_adjustment'] = 'matched'
            
            return adaptations
        except:
            return {}

    def _estimate_completion_time(self, learning_path):
        """Estimate total completion time"""
        try:
            total_time = sum(item['estimated_time'] for item in learning_path)
            
            # Adjust based on user profile
            # Faster learners might complete 20% faster
            # Slower learners might take 30% more time
            
            return {
                'estimated_hours': total_time,
                'estimated_days': total_time / 8,  # Assuming 8 hours per day
                'confidence_interval': [total_time * 0.8, total_time * 1.3]
            }
        except:
            return {'estimated_hours': 0, 'estimated_days': 0, 'confidence_interval': [0, 0]}

    def analyze_time_series_patterns(self, user_data):
        """Analyze time series patterns in user behavior"""
        try:
            df = pd.DataFrame(user_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Resample data by different time periods
            daily_data = df.set_index('timestamp').resample('D').agg({
                'engagement_score': 'mean',
                'sessions': 'sum',
                'time_spent': 'sum'
            })
            
            weekly_data = df.set_index('timestamp').resample('W').agg({
                'engagement_score': 'mean',
                'sessions': 'sum',
                'time_spent': 'sum'
            })
            
            # Calculate trends and seasonality
            patterns = {
                'daily_trend': self._calculate_trend(daily_data['engagement_score']),
                'weekly_trend': self._calculate_trend(weekly_data['engagement_score']),
                'seasonality': self._detect_seasonality(daily_data),
                'anomalies': self._detect_anomalies(daily_data),
                'forecast': self._simple_forecast(daily_data)
            }
            
            return {
                'status': 'success',
                'daily_data': daily_data.to_dict(),
                'weekly_data': weekly_data.to_dict(),
                'patterns': patterns
            }
        except Exception as e:
            print(f"Error analyzing time series patterns: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _detect_seasonality(self, data):
        """Detect seasonal patterns"""
        try:
            if len(data) < 14:  # Need at least 2 weeks
                return {}
            
            # Simple weekly seasonality detection
            data['day_of_week'] = data.index.dayofweek
            weekly_pattern = data.groupby('day_of_week')['engagement_score'].mean()
            
            return {
                'weekly_pattern': weekly_pattern.to_dict(),
                'seasonality_strength': weekly_pattern.std() / max(1, weekly_pattern.mean())
            }
        except:
            return {}

    def _detect_anomalies(self, data):
        """Detect anomalies in time series data"""
        try:
            if len(data) < 5:
                return []
            
            # Simple anomaly detection using z-score
            engagement_scores = data['engagement_score'].dropna()
            if len(engagement_scores) < 3:
                return []
            
            mean_score = engagement_scores.mean()
            std_score = engagement_scores.std()
            
            anomalies = []
            for date, score in engagement_scores.items():
                z_score = abs((score - mean_score) / max(1, std_score))
                if z_score > 2:  # Threshold for anomaly
                    anomalies.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'score': score,
                        'z_score': z_score,
                        'type': 'high' if score > mean_score else 'low'
                    })
            
            return anomalies
        except:
            return []

    def _simple_forecast(self, data, periods=7):
        """Simple forecast for next periods"""
        try:
            if len(data) < 3:
                return []
            
            # Simple moving average forecast
            engagement_scores = data['engagement_score'].dropna()
            if len(engagement_scores) < 3:
                return []
            
            recent_avg = engagement_scores.tail(3).mean()
            trend = self._calculate_trend(engagement_scores)
            
            forecast = []
            for i in range(periods):
                if trend == 'increasing':
                    forecast_value = recent_avg * (1 + 0.05 * (i + 1))
                elif trend == 'decreasing':
                    forecast_value = recent_avg * (1 - 0.05 * (i + 1))
                else:
                    forecast_value = recent_avg
                
                forecast.append({
                    'period': i + 1,
                    'predicted_score': max(0, min(100, forecast_value))
                })
            
            return forecast
        except:
            return []

    def generate_behavior_report(self, user_id, user_data):
        """Generate comprehensive behavior analysis report"""
        try:
            # Preprocess data
            processed_data = self.preprocess_user_data(user_data)
            if processed_data is None:
                return {'status': 'error', 'message': 'Data preprocessing failed'}
            
            # Extract features
            features_df = self.extract_behavioral_features(processed_data)
            if features_df is None:
                return {'status': 'error', 'message': 'Feature extraction failed'}
            
            # Analyze engagement patterns
            engagement_analysis = self.analyze_engagement_patterns(user_data)
            
            # Time series analysis
            time_series_analysis = self.analyze_time_series_patterns(user_data)
            
            # Learning path prediction
            learning_path_prediction = self.predict_learning_path(user_data, [])
            
            # Compile report
            report = {
                'user_id': user_id,
                'analysis_date': datetime.now().isoformat(),
                'behavioral_features': features_df.to_dict('records')[0] if len(features_df) > 0 else {},
                'engagement_patterns': engagement_analysis,
                'time_series_patterns': time_series_analysis,
                'learning_path': learning_path_prediction,
                'recommendations': self._generate_recommendations(features_df, engagement_analysis)
            }
            
            return {
                'status': 'success',
                'report': report
            }
        except Exception as e:
            print(f"Error generating behavior report: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _generate_recommendations(self, features_df, engagement_analysis):
        """Generate personalized recommendations"""
        try:
            recommendations = []
            
            if len(features_df) > 0:
                features = features_df.iloc[0]
                
                # Engagement recommendations
                if features.get('completion_rate', 0) < 0.7:
                    recommendations.append({
                        'type': 'engagement',
                        'priority': 'high',
                        'message': 'Consider breaking down tasks into smaller, manageable chunks to improve completion rates.'
                    })
                
                # Time-based recommendations
                if features.get('sessions_per_week', 0) < 3:
                    recommendations.append({
                        'type': 'frequency',
                        'priority': 'medium',
                        'message': 'Increase session frequency to at least 3 times per week for better learning retention.'
                    })
                
                # Performance recommendations
                if features.get('avg_score', 0) < 70:
                    recommendations.append({
                        'type': 'performance',
                        'priority': 'high',
                        'message': 'Focus on foundational concepts before advancing to more complex topics.'
                    })
            
            # Pattern-based recommendations
            if engagement_analysis.get('status') == 'success':
                insights = engagement_analysis.get('insights', {})
                
                if insights.get('engagement_trend') == 'decreasing':
                    recommendations.append({
                        'type': 'motivation',
                        'priority': 'high',
                        'message': 'Your engagement is decreasing. Try new learning formats or take a short break to refresh.'
                    })
            
            return recommendations
        except:
            return []

    def save_model(self, filepath):
        """Save trained models"""
        try:
            model_data = {
                'scaler': self.scaler,
                'label_encoder': self.label_encoder,
                'user_classifier': self.user_classifier,
                'performance_predictor': self.performance_predictor,
                'user_clustering': self.user_clustering,
                'density_clustering': self.density_clustering,
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
            self.label_encoder = model_data['label_encoder']
            self.user_classifier = model_data['user_classifier']
            self.performance_predictor = model_data['performance_predictor']
            self.user_clustering = model_data['user_clustering']
            self.density_clustering = model_data['density_clustering']
            self.is_trained = model_data['is_trained']
            
            return {'status': 'success', 'message': f'Model loaded from {filepath}'}
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the analytics system
    analytics = UserBehaviorAnalytics()
    
    # Sample user data for testing
    sample_user_data = [
        {
            'user_id': 1,
            'timestamp': '2024-01-01 10:00:00',
            'session_duration': 45,
            'interactions': 15,
            'completed': True,
            'score': 85,
            'engagement_score': 0.8,
            'skill_level': 3,
            'difficulty_preference': 'medium',
            'time_spent': 45,
            'visual_interactions': 8,
            'textual_interactions': 5,
            'interactive_interactions': 2,
            'skill_category': 'technical',
            'sessions': 1
        },
        {
            'user_id': 1,
            'timestamp': '2024-01-02 14:00:00',
            'session_duration': 30,
            'interactions': 10,
            'completed': False,
            'score': 70,
            'engagement_score': 0.6,
            'skill_level': 3,
            'difficulty_preference': 'medium',
            'time_spent': 30,
            'visual_interactions': 5,
            'textual_interactions': 3,
            'interactive_interactions': 2,
            'skill_category': 'technical',
            'sessions': 1
        }
    ]
    
    # Generate behavior report
    report = analytics.generate_behavior_report(1, sample_user_data)
    print("Behavior Report:", json.dumps(report, indent=2, default=str))
