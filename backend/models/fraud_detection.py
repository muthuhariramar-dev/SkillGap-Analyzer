"""
Fraud Detection System for Skills Gap Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

class FraudDetectionSystem:
    """
    Advanced Fraud Detection System for Skills Gap Analysis
    Features: Anomaly Detection, Ensemble Methods, Deep Learning,
              Pattern Recognition, Behavioral Analysis, Real-time Monitoring
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.one_class_svm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.1)
        self.ensemble_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.neural_detector = MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
        self.is_trained = False
        
        # Fraud patterns database
        self.fraud_patterns = {
            'answer_patterns': [],
            'time_patterns': [],
            'behavioral_patterns': [],
            'network_patterns': []
        }
        
        # Risk scoring weights
        self.risk_weights = {
            'time_anomaly': 0.3,
            'answer_similarity': 0.25,
            'behavioral_anomaly': 0.2,
            'network_anomaly': 0.15,
            'historical_risk': 0.1
        }

    def analyze_user_session(self, session_data):
        """Analyze user session for fraud indicators"""
        try:
            # Preprocess session data
            processed_data = self._preprocess_session_data(session_data)
            
            # Extract features
            features = self._extract_fraud_features(processed_data)
            
            # Anomaly detection
            anomaly_scores = self._detect_anomalies(features)
            
            # Pattern matching
            pattern_matches = self._match_fraud_patterns(processed_data)
            
            # Behavioral analysis
            behavioral_risk = self._analyze_behavioral_patterns(processed_data)
            
            # Network analysis
            network_risk = self._analyze_network_patterns(session_data)
            
            # Calculate overall risk score
            risk_assessment = self._calculate_risk_score(
                anomaly_scores, pattern_matches, behavioral_risk, network_risk
            )
            
            # Generate alerts
            alerts = self._generate_fraud_alerts(risk_assessment, processed_data)
            
            return {
                'status': 'success',
                'session_id': session_data.get('session_id'),
                'risk_assessment': risk_assessment,
                'anomaly_scores': anomaly_scores,
                'pattern_matches': pattern_matches,
                'behavioral_risk': behavioral_risk,
                'network_risk': network_risk,
                'alerts': alerts,
                'recommendations': self._generate_recommendations(risk_assessment)
            }
        except Exception as e:
            print(f"Error analyzing user session: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _preprocess_session_data(self, session_data):
        """Preprocess session data for analysis"""
        try:
            df = pd.DataFrame(session_data.get('responses', []))
            
            if df.empty:
                return pd.DataFrame()
            
            # Convert timestamps
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['response_time_seconds'] = df['timestamp'].astype(int) / 1e9
            
            # Calculate time differences between responses
            if 'timestamp' in df.columns:
                df = df.sort_values('timestamp')
                df['time_between_responses'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
            
            # Add session-level features
            df['session_id'] = session_data.get('session_id')
            df['user_id'] = session_data.get('user_id')
            df['ip_address'] = session_data.get('ip_address', '')
            df['device_info'] = session_data.get('device_info', {})
            
            return df
        except Exception as e:
            print(f"Error preprocessing session data: {str(e)}")
            return pd.DataFrame()

    def _extract_fraud_features(self, df):
        """Extract features for fraud detection"""
        try:
            if df.empty:
                return np.array([])
            
            features = []
            
            # Time-based features
            features.extend([
                df['time_between_responses'].mean(),
                df['time_between_responses'].std(),
                df['time_between_responses'].min(),
                df['time_between_responses'].max(),
                self._calculate_time_variance(df),
                self._detect_rapid_responses(df)
            ])
            
            # Answer pattern features
            features.extend([
                self._calculate_answer_consistency(df),
                self._detect_repetition_patterns(df),
                self._calculate_answer_distribution(df),
                self._detect_copying_patterns(df)
            ])
            
            # Behavioral features
            features.extend([
                self._calculate_typing_rhythm(df),
                self._detect_mouse_patterns(df),
                self._calculate_interaction_frequency(df),
                self._detect_automation_signs(df)
            ])
            
            # Session features
            features.extend([
                len(df),  # Total responses
                df['response_time_seconds'].max() - df['response_time_seconds'].min(),  # Session duration
                self._calculate_session_regularity(df)
            ])
            
            return np.array(features)
        except Exception as e:
            print(f"Error extracting fraud features: {str(e)}")
            return np.array([])

    def _calculate_time_variance(self, df):
        """Calculate variance in response times"""
        try:
            if 'time_between_responses' not in df.columns or len(df) < 2:
                return 0.0
            
            times = df['time_between_responses'].values
            return np.var(times)
        except:
            return 0.0

    def _detect_rapid_responses(self, df):
        """Detect unusually rapid responses"""
        try:
            if 'time_between_responses' not in df.columns:
                return 0.0
            
            # Count responses under 2 seconds
            rapid_count = (df['time_between_responses'] < 2.0).sum()
            return rapid_count / len(df)
        except:
            return 0.0

    def _calculate_answer_consistency(self, df):
        """Calculate answer consistency"""
        try:
            if 'answer' not in df.columns:
                return 0.0
            
            answers = df['answer'].astype(str)
            if len(answers) < 2:
                return 1.0
            
            # Calculate similarity between consecutive answers
            similarities = []
            for i in range(len(answers) - 1):
                similarity = self._string_similarity(answers.iloc[i], answers.iloc[i + 1])
                similarities.append(similarity)
            
            return np.mean(similarities) if similarities else 0.0
        except:
            return 0.0

    def _string_similarity(self, s1, s2):
        """Calculate string similarity"""
        try:
            if s1 == s2:
                return 1.0
            
            # Simple character-based similarity
            common_chars = set(s1) & set(s2)
            total_chars = set(s1) | set(s2)
            
            return len(common_chars) / len(total_chars) if total_chars else 0.0
        except:
            return 0.0

    def _detect_repetition_patterns(self, df):
        """Detect repetitive answer patterns"""
        try:
            if 'answer' not in df.columns:
                return 0.0
            
            answers = df['answer'].astype(str)
            unique_answers = answers.nunique()
            total_answers = len(answers)
            
            # High repetition indicator
            return 1.0 - (unique_answers / total_answers)
        except:
            return 0.0

    def _calculate_answer_distribution(self, df):
        """Calculate distribution of answer types"""
        try:
            if 'answer' not in df.columns:
                return 0.0
            
            answers = df['answer'].astype(str)
            answer_counts = answers.value_counts()
            
            # Calculate entropy (higher entropy = more diverse answers)
            probabilities = answer_counts / len(answers)
            entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
            
            # Normalize entropy
            max_entropy = np.log2(len(answer_counts))
            return entropy / max_entropy if max_entropy > 0 else 0.0
        except:
            return 0.0

    def _detect_copying_patterns(self, df):
        """Detect potential copying patterns"""
        try:
            if 'answer' not in df.columns or len(df) < 3:
                return 0.0
            
            answers = df['answer'].astype(str)
            
            # Look for identical consecutive answers
            identical_consecutive = 0
            for i in range(len(answers) - 1):
                if answers.iloc[i] == answers.iloc[i + 1]:
                    identical_consecutive += 1
            
            return identical_consecutive / (len(answers) - 1)
        except:
            return 0.0

    def _calculate_typing_rhythm(self, df):
        """Calculate typing rhythm consistency"""
        try:
            if 'time_between_responses' not in df.columns or len(df) < 3:
                return 0.0
            
            times = df['time_between_responses'].values
            
            # Calculate coefficient of variation
            mean_time = np.mean(times)
            std_time = np.std(times)
            
            cv = std_time / mean_time if mean_time > 0 else float('inf')
            
            # Lower CV indicates more consistent rhythm (potentially automated)
            return max(0, 1 - cv / 2)  # Normalize to 0-1
        except:
            return 0.0

    def _detect_mouse_patterns(self, df):
        """Detect mouse movement patterns"""
        try:
            # This would typically use actual mouse tracking data
            # For now, return a placeholder
            return 0.0
        except:
            return 0.0

    def _calculate_interaction_frequency(self, df):
        """Calculate interaction frequency"""
        try:
            if 'timestamp' not in df.columns:
                return 0.0
            
            session_duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
            interactions = len(df)
            
            return interactions / max(1, session_duration)
        except:
            return 0.0

    def _detect_automation_signs(self, df):
        """Detect signs of automation"""
        try:
            automation_score = 0.0
            
            # Perfect timing consistency
            if 'time_between_responses' in df.columns:
                times = df['time_between_responses'].values
                if len(times) > 2:
                    time_std = np.std(times)
                    if time_std < 0.1:  # Very consistent timing
                        automation_score += 0.3
            
            # Instant responses
            rapid_score = self._detect_rapid_responses(df)
            if rapid_score > 0.5:
                automation_score += 0.4
            
            # Identical answers
            repetition_score = self._detect_repetition_patterns(df)
            if repetition_score > 0.7:
                automation_score += 0.3
            
            return min(1.0, automation_score)
        except:
            return 0.0

    def _calculate_session_regularity(self, df):
        """Calculate session regularity"""
        try:
            if 'timestamp' not in df.columns:
                return 0.0
            
            # Check if responses are at regular intervals
            times = df['timestamp'].values
            if len(times) < 3:
                return 0.0
            
            intervals = np.diff(times.astype(int) / 1e9)  # Convert to seconds
            interval_std = np.std(intervals)
            interval_mean = np.mean(intervals)
            
            # Lower relative standard deviation indicates more regularity
            regularity = 1 - (interval_std / interval_mean) if interval_mean > 0 else 0
            return max(0, min(1, regularity))
        except:
            return 0.0

    def _detect_anomalies(self, features):
        """Detect anomalies using multiple methods"""
        try:
            if len(features) == 0:
                return {'isolation_forest': 0.0, 'one_class_svm': 0.0, 'ensemble': 0.0}
            
            features_reshaped = features.reshape(1, -1)
            
            # Isolation Forest
            if self.is_trained:
                iso_score = self.isolation_forest.decision_function(features_reshaped)[0]
                iso_anomaly = 1 - (iso_score + 1) / 2  # Convert to 0-1 scale
            else:
                iso_anomaly = 0.0
            
            # One-Class SVM
            if self.is_trained:
                svm_score = self.one_class_svm.decision_function(features_reshaped)[0]
                svm_anomaly = 1 - (1 / (1 + np.exp(svm_score)))  # Convert to 0-1 scale
            else:
                svm_anomaly = 0.0
            
            # Ensemble score
            ensemble_anomaly = (iso_anomaly + svm_anomaly) / 2
            
            return {
                'isolation_forest': iso_anomaly,
                'one_class_svm': svm_anomaly,
                'ensemble': ensemble_anomaly
            }
        except Exception as e:
            print(f"Error detecting anomalies: {str(e)}")
            return {'isolation_forest': 0.0, 'one_class_svm': 0.0, 'ensemble': 0.0}

    def _match_fraud_patterns(self, df):
        """Match against known fraud patterns"""
        try:
            if df.empty:
                return {'matches': [], 'confidence': 0.0}
            
            matches = []
            total_confidence = 0.0
            
            # Pattern 1: Rapid fire responses
            rapid_responses = self._detect_rapid_responses(df)
            if rapid_responses > 0.7:
                matches.append({
                    'pattern': 'rapid_fire_responses',
                    'confidence': rapid_responses,
                    'description': 'Unusually rapid response pattern detected'
                })
                total_confidence += rapid_responses
            
            # Pattern 2: Identical answers
            identical_answers = self._detect_copying_patterns(df)
            if identical_answers > 0.5:
                matches.append({
                    'pattern': 'identical_answers',
                    'confidence': identical_answers,
                    'description': 'Multiple identical consecutive answers'
                })
                total_confidence += identical_answers
            
            # Pattern 3: Perfect timing
            timing_regularity = self._calculate_session_regularity(df)
            if timing_regularity > 0.9:
                matches.append({
                    'pattern': 'perfect_timing',
                    'confidence': timing_regularity,
                    'description': 'Suspiciously regular response timing'
                })
                total_confidence += timing_regularity
            
            # Pattern 4: Automation signs
            automation_score = self._detect_automation_signs(df)
            if automation_score > 0.6:
                matches.append({
                    'pattern': 'automation_signs',
                    'confidence': automation_score,
                    'description': 'Signs of automated response generation'
                })
                total_confidence += automation_score
            
            return {
                'matches': matches,
                'confidence': min(1.0, total_confidence / len(matches)) if matches else 0.0
            }
        except Exception as e:
            print(f"Error matching fraud patterns: {str(e)}")
            return {'matches': [], 'confidence': 0.0}

    def _analyze_behavioral_patterns(self, df):
        """Analyze behavioral patterns for fraud indicators"""
        try:
            if df.empty:
                return {'risk_score': 0.0, 'indicators': []}
            
            indicators = []
            risk_score = 0.0
            
            # Indicator 1: Unusual response time distribution
            if 'time_between_responses' in df.columns:
                times = df['time_between_responses']
                q1, q3 = times.quantile([0.25, 0.75])
                iqr = q3 - q1
                
                # Check for outliers
                outliers = ((times < (q1 - 1.5 * iqr)) | (times > (q3 + 1.5 * iqr))).sum()
                outlier_ratio = outliers / len(times)
                
                if outlier_ratio > 0.2:
                    indicators.append({
                        'type': 'time_distribution_anomaly',
                        'severity': 'medium',
                        'description': f'{outlier_ratio:.1%} of responses have unusual timing'
                    })
                    risk_score += 0.3
            
            # Indicator 2: Answer pattern analysis
            answer_consistency = self._calculate_answer_consistency(df)
            if answer_consistency > 0.8:
                indicators.append({
                    'type': 'high_answer_similarity',
                    'severity': 'medium',
                    'description': 'Answers show unusually high similarity'
                })
                risk_score += 0.25
            
            # Indicator 3: Interaction frequency
            interaction_freq = self._calculate_interaction_frequency(df)
            if interaction_freq > 10:  # More than 10 interactions per second
                indicators.append({
                    'type': 'high_interaction_frequency',
                    'severity': 'high',
                    'description': 'Unusually high interaction frequency'
                })
                risk_score += 0.4
            
            # Indicator 4: Session duration anomaly
            if 'timestamp' in df.columns:
                session_duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
                if session_duration < 60 and len(df) > 10:  # Very fast completion
                    indicators.append({
                        'type': 'rapid_completion',
                        'severity': 'high',
                        'description': 'Session completed unusually quickly'
                    })
                    risk_score += 0.35
            
            return {
                'risk_score': min(1.0, risk_score),
                'indicators': indicators
            }
        except Exception as e:
            print(f"Error analyzing behavioral patterns: {str(e)}")
            return {'risk_score': 0.0, 'indicators': []}

    def _analyze_network_patterns(self, session_data):
        """Analyze network-based fraud indicators"""
        try:
            network_risk = 0.0
            indicators = []
            
            # IP address analysis
            ip_address = session_data.get('ip_address', '')
            if ip_address:
                # Check for VPN/proxy indicators (simplified)
                if self._is_suspicious_ip(ip_address):
                    indicators.append({
                        'type': 'suspicious_ip',
                        'severity': 'medium',
                        'description': 'IP address associated with suspicious activity'
                    })
                    network_risk += 0.3
            
            # Device fingerprinting
            device_info = session_data.get('device_info', {})
            if device_info:
                # Check for common automation tools
                user_agent = device_info.get('user_agent', '').lower()
                automation_tools = ['selenium', 'webdriver', 'phantomjs', 'headless']
                
                for tool in automation_tools:
                    if tool in user_agent:
                        indicators.append({
                            'type': 'automation_tool_detected',
                            'severity': 'high',
                            'description': f'Automation tool "{tool}" detected'
                        })
                        network_risk += 0.5
                        break
            
            # Geographic analysis (placeholder)
            # In real implementation, would check for impossible travel times
            # multiple locations in short time period, etc.
            
            return {
                'risk_score': min(1.0, network_risk),
                'indicators': indicators
            }
        except Exception as e:
            print(f"Error analyzing network patterns: {str(e)}")
            return {'risk_score': 0.0, 'indicators': []}

    def _is_suspicious_ip(self, ip_address):
        """Check if IP address is suspicious"""
        try:
            # Simplified check - in real implementation would use threat intelligence
            suspicious_ranges = [
                '10.0.0.',     # Private network
                '192.168.',    # Private network
                '172.16.',     # Private network
            ]
            
            for range_prefix in suspicious_ranges:
                if ip_address.startswith(range_prefix):
                    return True
            
            return False
        except:
            return False

    def _calculate_risk_score(self, anomaly_scores, pattern_matches, behavioral_risk, network_risk):
        """Calculate overall fraud risk score"""
        try:
            # Weighted combination of different risk factors
            risk_components = {
                'anomaly_score': anomaly_scores.get('ensemble', 0.0) * self.risk_weights['time_anomaly'],
                'pattern_matching': pattern_matches.get('confidence', 0.0) * self.risk_weights['answer_similarity'],
                'behavioral_risk': behavioral_risk.get('risk_score', 0.0) * self.risk_weights['behavioral_anomaly'],
                'network_risk': network_risk.get('risk_score', 0.0) * self.risk_weights['network_anomaly']
            }
            
            total_risk = sum(risk_components.values())
            
            # Risk level classification
            if total_risk >= 0.8:
                risk_level = 'critical'
            elif total_risk >= 0.6:
                risk_level = 'high'
            elif total_risk >= 0.4:
                risk_level = 'medium'
            elif total_risk >= 0.2:
                risk_level = 'low'
            else:
                risk_level = 'minimal'
            
            return {
                'overall_score': min(1.0, total_risk),
                'risk_level': risk_level,
                'components': risk_components,
                'confidence': self._calculate_risk_confidence(risk_components)
            }
        except Exception as e:
            print(f"Error calculating risk score: {str(e)}")
            return {'overall_score': 0.0, 'risk_level': 'minimal', 'components': {}, 'confidence': 0.0}

    def _calculate_risk_confidence(self, risk_components):
        """Calculate confidence in risk assessment"""
        try:
            # Higher confidence when multiple indicators agree
            non_zero_components = sum(1 for v in risk_components.values() if v > 0.1)
            max_components = len(risk_components)
            
            base_confidence = non_zero_components / max_components
            
            # Adjust based on overall risk level
            overall_risk = sum(risk_components.values())
            if overall_risk > 0.7 or overall_risk < 0.1:
                base_confidence += 0.2  # More confident at extremes
            
            return min(1.0, base_confidence)
        except:
            return 0.5

    def _generate_fraud_alerts(self, risk_assessment, df):
        """Generate fraud alerts based on risk assessment"""
        try:
            alerts = []
            risk_level = risk_assessment.get('risk_level', 'minimal')
            
            if risk_level in ['critical', 'high']:
                alerts.append({
                    'type': 'high_risk_detected',
                    'severity': 'high',
                    'message': f'High fraud risk detected (score: {risk_assessment.get("overall_score", 0):.2f})',
                    'action_required': 'immediate_review'
                })
            elif risk_level == 'medium':
                alerts.append({
                    'type': 'medium_risk_detected',
                    'severity': 'medium',
                    'message': f'Medium fraud risk detected (score: {risk_assessment.get("overall_score", 0):.2f})',
                    'action_required': 'monitor_closely'
                })
            
            # Specific pattern alerts
            components = risk_assessment.get('components', {})
            
            if components.get('anomaly_score', 0) > 0.7:
                alerts.append({
                    'type': 'anomaly_detected',
                    'severity': 'medium',
                    'message': 'Unusual response patterns detected',
                    'action_required': 'investigate_patterns'
                })
            
            if components.get('pattern_matching', 0) > 0.7:
                alerts.append({
                    'type': 'pattern_match',
                    'severity': 'high',
                    'message': 'Response matches known fraud patterns',
                    'action_required': 'detailed_analysis'
                })
            
            return alerts
        except Exception as e:
            print(f"Error generating fraud alerts: {str(e)}")
            return []

    def _generate_recommendations(self, risk_assessment):
        """Generate recommendations based on risk assessment"""
        try:
            recommendations = []
            risk_level = risk_assessment.get('risk_level', 'minimal')
            
            if risk_level == 'critical':
                recommendations.extend([
                    {
                        'type': 'immediate_action',
                        'priority': 'urgent',
                        'title': 'Immediate Review Required',
                        'description': 'Session requires immediate manual review due to high fraud risk.'
                    },
                    {
                        'type': 'user_verification',
                        'priority': 'urgent',
                        'title': 'Verify User Identity',
                        'description': 'Require additional identity verification for this user.'
                    }
                ])
            elif risk_level == 'high':
                recommendations.extend([
                    {
                        'type': 'enhanced_monitoring',
                        'priority': 'high',
                        'title': 'Enhanced Monitoring',
                        'description': 'Place user under enhanced monitoring for future sessions.'
                    },
                    {
                        'type': 'additional_checks',
                        'priority': 'medium',
                        'title': 'Additional Verification',
                        'description': 'Implement additional verification steps for this user.'
                    }
                ])
            elif risk_level == 'medium':
                recommendations.append({
                    'type': 'increased_scrutiny',
                    'priority': 'medium',
                    'title': 'Increased Scrutiny',
                    'description': 'Monitor this user more closely in future sessions.'
                })
            else:
                recommendations.append({
                    'type': 'standard_monitoring',
                    'priority': 'low',
                    'title': 'Standard Monitoring',
                    'description': 'Continue with standard monitoring procedures.'
                })
            
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []

    def train_models(self, training_data):
        """Train fraud detection models"""
        try:
            # Preprocess training data
            features_list = []
            labels_list = []
            
            for session in training_data:
                processed_data = self._preprocess_session_data(session)
                features = self._extract_fraud_features(processed_data)
                
                if len(features) > 0:
                    features_list.append(features)
                    labels_list.append(session.get('is_fraud', 0))
            
            if len(features_list) < 10:
                return {'status': 'error', 'message': 'Insufficient training data'}
            
            X = np.array(features_list)
            y = np.array(labels_list)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train models
            self.isolation_forest.fit(X_scaled)
            self.one_class_svm.fit(X_scaled)
            
            # Train ensemble classifier
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            self.ensemble_classifier.fit(X_train, y_train)
            
            # Train neural network
            self.neural_detector.fit(X_train, y_train)
            
            self.is_trained = True
            
            # Evaluate models
            train_score = self.ensemble_classifier.score(X_train, y_train)
            test_score = self.ensemble_classifier.score(X_test, y_test)
            
            return {
                'status': 'success',
                'training_samples': len(features_list),
                'train_accuracy': train_score,
                'test_accuracy': test_score,
                'model_performance': {
                    'isolation_forest': 'trained',
                    'one_class_svm': 'trained',
                    'ensemble_classifier': 'trained',
                    'neural_detector': 'trained'
                }
            }
        except Exception as e:
            print(f"Error training models: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def save_model(self, filepath):
        """Save trained models"""
        try:
            model_data = {
                'scaler': self.scaler,
                'isolation_forest': self.isolation_forest,
                'one_class_svm': self.one_class_svm,
                'ensemble_classifier': self.ensemble_classifier,
                'neural_detector': self.neural_detector,
                'fraud_patterns': self.fraud_patterns,
                'risk_weights': self.risk_weights,
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
            self.isolation_forest = model_data['isolation_forest']
            self.one_class_svm = model_data['one_class_svm']
            self.ensemble_classifier = model_data['ensemble_classifier']
            self.neural_detector = model_data['neural_detector']
            self.fraud_patterns = model_data['fraud_patterns']
            self.risk_weights = model_data['risk_weights']
            self.is_trained = model_data['is_trained']
            
            return {'status': 'success', 'message': f'Model loaded from {filepath}'}
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the fraud detection system
    fraud_detector = FraudDetectionSystem()
    
    # Sample session data
    sample_session = {
        'session_id': 'session_123',
        'user_id': 'user_456',
        'ip_address': '192.168.1.100',
        'device_info': {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'responses': [
            {
                'question_id': 'q1',
                'answer': 'A',
                'timestamp': '2024-01-01T10:00:00',
                'response_time': 15
            },
            {
                'question_id': 'q2',
                'answer': 'B',
                'timestamp': '2024-01-01T10:00:30',
                'response_time': 25
            },
            {
                'question_id': 'q3',
                'answer': 'A',
                'timestamp': '2024-01-01T10:01:00',
                'response_time': 20
            }
        ]
    }
    
    # Analyze session for fraud
    analysis_result = fraud_detector.analyze_user_session(sample_session)
    print("Fraud Analysis Result:", json.dumps(analysis_result, indent=2, default=str))
