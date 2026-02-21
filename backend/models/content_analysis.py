"""
Content Analysis System for Skills Gap Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, silhouette_score
import re
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

class ContentAnalysisSystem:
    """
    Advanced Content Analysis System for Skills Gap Analysis
    Features: Text Classification, Sentiment Analysis, Topic Modeling,
              Content Quality Assessment, Keyword Extraction, Semantic Analysis
    """

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.count_vectorizer = CountVectorizer(max_features=5000, stop_words='english')
        self.text_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.sentiment_classifier = MultinomialNB()
        self.topic_model = LatentDirichletAllocation(n_components=10, random_state=42)
        self.content_quality_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.clustering_model = KMeans(n_clusters=5, random_state=42)
        self.is_trained = False
        
        # Sentiment lexicon (simplified)
        self.positive_words = {
            'excellent', 'great', 'amazing', 'wonderful', 'fantastic', 'good', 'nice',
            'helpful', 'useful', 'effective', 'valuable', 'important', 'clear', 'well',
            'perfect', 'outstanding', 'superb', 'brilliant', 'awesome', 'impressive'
        }
        
        self.negative_words = {
            'poor', 'bad', 'terrible', 'awful', 'horrible', 'useless', 'ineffective',
            'confusing', 'unclear', 'difficult', 'hard', 'boring', 'disappointing',
            'frustrating', 'annoying', 'wrong', 'incorrect', 'inadequate', 'insufficient'
        }

    def analyze_text_content(self, content_data):
        """Analyze text content comprehensively"""
        try:
            # Extract text from content data
            text_content = self._extract_text(content_data)
            
            if not text_content.strip():
                return {'status': 'error', 'message': 'No text content to analyze'}
            
            # Text preprocessing
            processed_text = self._preprocess_text(text_content)
            
            # Feature extraction
            text_features = self._extract_text_features(processed_text)
            
            # Classification
            classification_result = self._classify_content(processed_text)
            
            # Sentiment analysis
            sentiment_result = self._analyze_sentiment(processed_text)
            
            # Topic modeling
            topic_result = self._extract_topics(processed_text)
            
            # Quality assessment
            quality_result = self._assess_content_quality(processed_text, text_features)
            
            # Keyword extraction
            keywords = self._extract_keywords(processed_text)
            
            # Readability analysis
            readability = self._analyze_readability(text_content)
            
            # Semantic analysis
            semantic_result = self._analyze_semantics(processed_text)
            
            return {
                'status': 'success',
                'content_id': content_data.get('content_id'),
                'analysis_timestamp': datetime.now().isoformat(),
                'classification': classification_result,
                'sentiment': sentiment_result,
                'topics': topic_result,
                'quality_assessment': quality_result,
                'keywords': keywords,
                'readability': readability,
                'semantic_analysis': semantic_result,
                'text_statistics': self._calculate_text_statistics(text_content)
            }
        except Exception as e:
            print(f"Error analyzing text content: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _extract_text(self, content_data):
        """Extract text from various content formats"""
        try:
            text_parts = []
            
            # Direct text content
            if 'text' in content_data:
                text_parts.append(content_data['text'])
            
            # Title
            if 'title' in content_data:
                text_parts.append(content_data['title'])
            
            # Description
            if 'description' in content_data:
                text_parts.append(content_data['description'])
            
            # Questions and answers
            if 'questions' in content_data:
                for qa in content_data['questions']:
                    if 'question' in qa:
                        text_parts.append(qa['question'])
                    if 'answer' in qa:
                        text_parts.append(qa['answer'])
            
            # User responses
            if 'responses' in content_data:
                for response in content_data['responses']:
                    if 'answer' in response:
                        text_parts.append(response['answer'])
            
            return ' '.join(text_parts)
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ''

    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters and numbers (keep letters and spaces)
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        except Exception as e:
            print(f"Error preprocessing text: {str(e)}")
            return text

    def _extract_text_features(self, text):
        """Extract numerical features from text"""
        try:
            features = {}
            
            # Basic statistics
            features['char_count'] = len(text)
            features['word_count'] = len(text.split())
            features['sentence_count'] = text.count('.') + text.count('!') + text.count('?')
            features['avg_word_length'] = sum(len(word) for word in text.split()) / max(1, features['word_count'])
            features['avg_sentence_length'] = features['word_count'] / max(1, features['sentence_count'])
            
            # Vocabulary richness
            unique_words = set(text.split())
            features['vocabulary_richness'] = len(unique_words) / max(1, features['word_count'])
            
            # Punctuation usage
            features['exclamation_count'] = text.count('!')
            features['question_count'] = text.count('?')
            features['comma_count'] = text.count(',')
            
            # Readability indicators
            features['complex_words'] = sum(1 for word in text.split() if len(word) > 6)
            features['complex_word_ratio'] = features['complex_words'] / max(1, features['word_count'])
            
            return features
        except Exception as e:
            print(f"Error extracting text features: {str(e)}")
            return {}

    def _classify_content(self, text):
        """Classify content type and category"""
        try:
            if not self.is_trained:
                # Simple rule-based classification when model not trained
                return self._rule_based_classification(text)
            
            # Vectorize text
            text_vector = self.tfidf_vectorizer.transform([text])
            
            # Predict category
            category = self.text_classifier.predict(text_vector)[0]
            probabilities = self.text_classifier.predict_proba(text_vector)[0]
            
            # Get confidence
            confidence = max(probabilities)
            
            return {
                'predicted_category': category,
                'confidence': confidence,
                'probabilities': dict(zip(self.text_classifier.classes_, probabilities))
            }
        except Exception as e:
            print(f"Error classifying content: {str(e)}")
            return {'predicted_category': 'unknown', 'confidence': 0.0}

    def _rule_based_classification(self, text):
        """Rule-based content classification"""
        try:
            text_lower = text.lower()
            
            # Define keywords for different categories
            categories = {
                'technical': ['code', 'programming', 'algorithm', 'software', 'database', 'api', 'system'],
                'business': ['management', 'strategy', 'marketing', 'sales', 'finance', 'revenue', 'profit'],
                'education': ['learning', 'teaching', 'student', 'curriculum', 'knowledge', 'skill', 'training'],
                'science': ['research', 'experiment', 'theory', 'hypothesis', 'data', 'analysis', 'method'],
                'creative': ['design', 'art', 'creative', 'innovation', 'imagination', 'aesthetic', 'style']
            }
            
            # Score each category
            category_scores = {}
            for category, keywords in categories.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                category_scores[category] = score
            
            # Get best category
            if category_scores:
                best_category = max(category_scores, key=category_scores.get)
                score = category_scores[best_category]
                confidence = min(1.0, score / 5)  # Normalize to 0-1
            else:
                best_category = 'general'
                confidence = 0.5
            
            return {
                'predicted_category': best_category,
                'confidence': confidence,
                'probabilities': category_scores
            }
        except Exception as e:
            print(f"Error in rule-based classification: {str(e)}")
            return {'predicted_category': 'general', 'confidence': 0.0}

    def _analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            words = text.lower().split()
            
            # Count positive and negative words
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            
            total_sentiment_words = positive_count + negative_count
            
            if total_sentiment_words == 0:
                sentiment_score = 0.5  # Neutral
            else:
                sentiment_score = positive_count / total_sentiment_words
            
            # Classify sentiment
            if sentiment_score > 0.6:
                sentiment_label = 'positive'
            elif sentiment_score < 0.4:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
            
            # Additional sentiment metrics
            emotion_indicators = self._detect_emotions(text)
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'positive_words': positive_count,
                'negative_words': negative_count,
                'total_words': len(words),
                'emotion_indicators': emotion_indicators,
                'confidence': max(0.1, abs(sentiment_score - 0.5) * 2)  # Higher confidence for extreme sentiments
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {'sentiment_score': 0.5, 'sentiment_label': 'neutral', 'confidence': 0.0}

    def _detect_emotions(self, text):
        """Detect emotional indicators in text"""
        try:
            text_lower = text.lower()
            
            emotions = {
                'joy': ['happy', 'excited', 'pleased', 'delighted', 'thrilled', 'joyful'],
                'anger': ['angry', 'furious', 'irritated', 'frustrated', 'annoyed', 'mad'],
                'fear': ['scared', 'afraid', 'fearful', 'anxious', 'worried', 'nervous'],
                'sadness': ['sad', 'depressed', 'unhappy', 'miserable', 'gloomy', 'down'],
                'surprise': ['surprised', 'amazed', 'shocked', 'astonished', 'stunned']
            }
            
            emotion_scores = {}
            for emotion, keywords in emotions.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                emotion_scores[emotion] = score
            
            # Get dominant emotion
            if emotion_scores:
                dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                max_score = emotion_scores[dominant_emotion]
            else:
                dominant_emotion = 'neutral'
                max_score = 0
            
            return {
                'emotion_scores': emotion_scores,
                'dominant_emotion': dominant_emotion if max_score > 0 else 'neutral',
                'emotion_intensity': min(1.0, max_score / 3)  # Normalize intensity
            }
        except Exception as e:
            print(f"Error detecting emotions: {str(e)}")
            return {'emotion_scores': {}, 'dominant_emotion': 'neutral', 'emotion_intensity': 0.0}

    def _extract_topics(self, text):
        """Extract topics from text using topic modeling"""
        try:
            if not self.is_trained:
                # Simple keyword-based topic extraction
                return self._simple_topic_extraction(text)
            
            # Vectorize text
            text_vector = self.count_vectorizer.transform([text])
            
            # Get topic distribution
            topic_distribution = self.topic_model.transform(text_vector)[0]
            
            # Get top topics
            top_topics = []
            for i, prob in enumerate(topic_distribution):
                if prob > 0.1:  # Threshold for topic relevance
                    top_topics.append({
                        'topic_id': i,
                        'probability': prob,
                        'keywords': self._get_topic_keywords(i)
                    })
            
            # Sort by probability
            top_topics.sort(key=lambda x: x['probability'], reverse=True)
            
            return {
                'topics': top_topics[:5],  # Top 5 topics
                'dominant_topic': top_topics[0] if top_topics else None,
                'topic_diversity': len(top_topics)
            }
        except Exception as e:
            print(f"Error extracting topics: {str(e)}")
            return {'topics': [], 'dominant_topic': None, 'topic_diversity': 0}

    def _simple_topic_extraction(self, text):
        """Simple topic extraction using keyword frequency"""
        try:
            words = text.lower().split()
            word_freq = {}
            
            for word in words:
                if len(word) > 3:  # Filter short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords as topics
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            topics = []
            for i, (keyword, freq) in enumerate(top_keywords):
                topics.append({
                    'topic_id': i,
                    'probability': freq / len(words),
                    'keywords': [keyword]
                })
            
            return {
                'topics': topics,
                'dominant_topic': topics[0] if topics else None,
                'topic_diversity': len(topics)
            }
        except Exception as e:
            print(f"Error in simple topic extraction: {str(e)}")
            return {'topics': [], 'dominant_topic': None, 'topic_diversity': 0}

    def _get_topic_keywords(self, topic_id):
        """Get keywords for a specific topic"""
        try:
            # Get feature names
            feature_names = self.count_vectorizer.get_feature_names_out()
            
            # Get topic word distribution
            topic_word_dist = self.topic_model.components_[topic_id]
            
            # Get top words for this topic
            top_word_indices = np.argsort(topic_word_dist)[-10:][::-1]
            top_words = [feature_names[i] for i in top_word_indices]
            
            return top_words
        except Exception as e:
            print(f"Error getting topic keywords: {str(e)}")
            return []

    def _assess_content_quality(self, text, text_features):
        """Assess the quality of content"""
        try:
            if not self.is_trained:
                # Rule-based quality assessment
                return self._rule_based_quality_assessment(text_features)
            
            # Prepare features for quality model
            quality_features = self._prepare_quality_features(text_features)
            
            # Predict quality
            quality_score = self.content_quality_model.predict([quality_features])[0]
            quality_probabilities = self.content_quality_model.predict_proba([quality_features])[0]
            
            # Quality level
            if quality_score >= 0.8:
                quality_level = 'excellent'
            elif quality_score >= 0.6:
                quality_level = 'good'
            elif quality_score >= 0.4:
                quality_level = 'fair'
            else:
                quality_level = 'poor'
            
            return {
                'quality_score': quality_score,
                'quality_level': quality_level,
                'confidence': max(quality_probabilities),
                'quality_aspects': self._assess_quality_aspects(text_features)
            }
        except Exception as e:
            print(f"Error assessing content quality: {str(e)}")
            return {'quality_score': 0.5, 'quality_level': 'fair', 'confidence': 0.0}

    def _rule_based_quality_assessment(self, text_features):
        """Rule-based content quality assessment"""
        try:
            quality_score = 0.5  # Base score
            
            # Length assessment
            word_count = text_features.get('word_count', 0)
            if word_count >= 100:
                quality_score += 0.1
            elif word_count < 20:
                quality_score -= 0.2
            
            # Vocabulary richness
            vocab_richness = text_features.get('vocabulary_richness', 0)
            quality_score += vocab_richness * 0.2
            
            # Sentence structure
            avg_sentence_length = text_features.get('avg_sentence_length', 0)
            if 10 <= avg_sentence_length <= 25:
                quality_score += 0.1
            elif avg_sentence_length > 40:
                quality_score -= 0.1
            
            # Complexity
            complex_word_ratio = text_features.get('complex_word_ratio', 0)
            if 0.1 <= complex_word_ratio <= 0.3:
                quality_score += 0.1
            elif complex_word_ratio > 0.5:
                quality_score -= 0.1
            
            # Normalize score
            quality_score = max(0.0, min(1.0, quality_score))
            
            # Quality level
            if quality_score >= 0.8:
                quality_level = 'excellent'
            elif quality_score >= 0.6:
                quality_level = 'good'
            elif quality_score >= 0.4:
                quality_level = 'fair'
            else:
                quality_level = 'poor'
            
            return {
                'quality_score': quality_score,
                'quality_level': quality_level,
                'confidence': 0.7,  # Moderate confidence for rule-based
                'quality_aspects': self._assess_quality_aspects(text_features)
            }
        except Exception as e:
            print(f"Error in rule-based quality assessment: {str(e)}")
            return {'quality_score': 0.5, 'quality_level': 'fair', 'confidence': 0.0}

    def _prepare_quality_features(self, text_features):
        """Prepare features for quality model"""
        try:
            features = [
                text_features.get('char_count', 0),
                text_features.get('word_count', 0),
                text_features.get('sentence_count', 0),
                text_features.get('avg_word_length', 0),
                text_features.get('avg_sentence_length', 0),
                text_features.get('vocabulary_richness', 0),
                text_features.get('complex_word_ratio', 0)
            ]
            
            return features
        except Exception as e:
            print(f"Error preparing quality features: {str(e)}")
            return [0] * 7

    def _assess_quality_aspects(self, text_features):
        """Assess specific aspects of content quality"""
        try:
            aspects = {}
            
            # Clarity
            avg_sentence_length = text_features.get('avg_sentence_length', 0)
            if avg_sentence_length <= 20:
                aspects['clarity'] = 'high'
            elif avg_sentence_length <= 30:
                aspects['clarity'] = 'medium'
            else:
                aspects['clarity'] = 'low'
            
            # Complexity
            complex_word_ratio = text_features.get('complex_word_ratio', 0)
            if complex_word_ratio <= 0.2:
                aspects['complexity'] = 'simple'
            elif complex_word_ratio <= 0.4:
                aspects['complexity'] = 'moderate'
            else:
                aspects['complexity'] = 'complex'
            
            # Richness
            vocab_richness = text_features.get('vocabulary_richness', 0)
            if vocab_richness >= 0.7:
                aspects['vocabulary_richness'] = 'high'
            elif vocab_richness >= 0.5:
                aspects['vocabulary_richness'] = 'medium'
            else:
                aspects['vocabulary_richness'] = 'low'
            
            # Length adequacy
            word_count = text_features.get('word_count', 0)
            if word_count >= 100:
                aspects['length_adequacy'] = 'adequate'
            elif word_count >= 50:
                aspects['length_adequacy'] = 'minimal'
            else:
                aspects['length_adequacy'] = 'inadequate'
            
            return aspects
        except Exception as e:
            print(f"Error assessing quality aspects: {str(e)}")
            return {}

    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        try:
            # Simple frequency-based keyword extraction
            words = text.lower().split()
            word_freq = {}
            
            # Filter out common stop words (simplified list)
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
            
            for word in words:
                if word not in stop_words and len(word) > 3:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
            
            return {
                'keywords': [{'word': word, 'frequency': freq} for word, freq in top_keywords],
                'total_unique_words': len(word_freq),
                'keyword_density': sum(freq for _, freq in top_keywords) / max(1, len(words))
            }
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return {'keywords': [], 'total_unique_words': 0, 'keyword_density': 0.0}

    def _analyze_readability(self, text):
        """Analyze text readability"""
        try:
            # Basic readability metrics
            sentences = text.split('.')
            words = text.split()
            
            # Average sentence length
            avg_sentence_length = len(words) / max(1, len(sentences))
            
            # Average word length
            avg_word_length = sum(len(word) for word in words) / max(1, len(words))
            
            # Syllable count (simplified)
            syllable_count = sum(self._count_syllables(word) for word in words)
            
            # Flesch Reading Ease (simplified version)
            if len(sentences) > 0 and len(words) > 0:
                flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (syllable_count / len(words)))
            else:
                flesch_score = 0
            
            # Reading level
            if flesch_score >= 90:
                reading_level = 'very_easy'
            elif flesch_score >= 80:
                reading_level = 'easy'
            elif flesch_score >= 70:
                reading_level = 'fairly_easy'
            elif flesch_score >= 60:
                reading_level = 'standard'
            elif flesch_score >= 50:
                reading_level = 'fairly_difficult'
            elif flesch_score >= 30:
                reading_level = 'difficult'
            else:
                reading_level = 'very_difficult'
            
            return {
                'flesch_score': max(0, min(100, flesch_score)),
                'reading_level': reading_level,
                'avg_sentence_length': avg_sentence_length,
                'avg_word_length': avg_word_length,
                'total_sentences': len(sentences),
                'total_words': len(words),
                'total_syllables': syllable_count
            }
        except Exception as e:
            print(f"Error analyzing readability: {str(e)}")
            return {'flesch_score': 0, 'reading_level': 'standard', 'avg_sentence_length': 0, 'avg_word_length': 0}

    def _count_syllables(self, word):
        """Count syllables in a word (simplified)"""
        try:
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllable_count += 1
                prev_was_vowel = is_vowel
            
            # Adjust for silent 'e'
            if word.endswith('e') and syllable_count > 1:
                syllable_count -= 1
            
            return max(1, syllable_count)
        except:
            return 1

    def _analyze_semantics(self, text):
        """Analyze semantic aspects of text"""
        try:
            # Semantic richness indicators
            unique_words = set(text.lower().split())
            total_words = len(text.split())
            
            # Semantic diversity
            semantic_diversity = len(unique_words) / max(1, total_words)
            
            # Content words vs function words
            content_words = {'noun', 'verb', 'adjective', 'adverb'}  # Simplified
            # In real implementation, would use POS tagging
            
            # Information density (simplified)
            information_density = semantic_diversity
            
            # Coherence indicators (simplified)
            coherence_score = self._calculate_coherence(text)
            
            return {
                'semantic_diversity': semantic_diversity,
                'information_density': information_density,
                'coherence_score': coherence_score,
                'semantic_complexity': self._assess_semantic_complexity(text),
                'topic_coherence': self._assess_topic_coherence(text)
            }
        except Exception as e:
            print(f"Error analyzing semantics: {str(e)}")
            return {'semantic_diversity': 0, 'information_density': 0, 'coherence_score': 0}

    def _calculate_coherence(self, text):
        """Calculate text coherence (simplified)"""
        try:
            sentences = text.split('.')
            
            if len(sentences) < 2:
                return 1.0
            
            # Simple coherence based on word overlap between sentences
            coherence_scores = []
            
            for i in range(len(sentences) - 1):
                sent1_words = set(sentences[i].lower().split())
                sent2_words = set(sentences[i + 1].lower().split())
                
                # Calculate Jaccard similarity
                intersection = len(sent1_words & sent2_words)
                union = len(sent1_words | sent2_words)
                
                if union > 0:
                    similarity = intersection / union
                    coherence_scores.append(similarity)
            
            return np.mean(coherence_scores) if coherence_scores else 0.5
        except Exception as e:
            print(f"Error calculating coherence: {str(e)}")
            return 0.5

    def _assess_semantic_complexity(self, text):
        """Assess semantic complexity"""
        try:
            words = text.split()
            
            # Complex words (longer than 6 characters)
            complex_words = sum(1 for word in words if len(word) > 6)
            complexity_ratio = complex_words / max(1, len(words))
            
            if complexity_ratio > 0.3:
                complexity_level = 'high'
            elif complexity_ratio > 0.15:
                complexity_level = 'medium'
            else:
                complexity_level = 'low'
            
            return {
                'complexity_level': complexity_level,
                'complex_word_ratio': complexity_ratio,
                'avg_word_length': np.mean([len(word) for word in words]) if words else 0
            }
        except Exception as e:
            print(f"Error assessing semantic complexity: {str(e)}")
            return {'complexity_level': 'medium', 'complex_word_ratio': 0, 'avg_word_length': 0}

    def _assess_topic_coherence(self, text):
        """Assess topic coherence"""
        try:
            # Simplified topic coherence based on keyword clustering
            keywords = self._extract_keywords(text)
            top_keywords = [kw['word'] for kw in keywords['keywords'][:10]]
            
            if len(top_keywords) < 3:
                return 0.5
            
            # Check for related keywords (simplified)
            coherence_score = 0.0
            pairs_checked = 0
            
            for i in range(len(top_keywords)):
                for j in range(i + 1, len(top_keywords)):
                    # Simple relatedness check (shared characters)
                    word1, word2 = top_keywords[i], top_keywords[j]
                    shared_chars = set(word1) & set(word2)
                    similarity = len(shared_chars) / max(len(set(word1)), len(set(word2)))
                    coherence_score += similarity
                    pairs_checked += 1
            
            return coherence_score / max(1, pairs_checked)
        except Exception as e:
            print(f"Error assessing topic coherence: {str(e)}")
            return 0.5

    def _calculate_text_statistics(self, text):
        """Calculate comprehensive text statistics"""
        try:
            words = text.split()
            sentences = text.split('.')
            paragraphs = text.split('\n\n')
            
            return {
                'character_count': len(text),
                'word_count': len(words),
                'sentence_count': len([s for s in sentences if s.strip()]),
                'paragraph_count': len([p for p in paragraphs if p.strip()]),
                'avg_words_per_sentence': len(words) / max(1, len(sentences)),
                'avg_sentences_per_paragraph': len(sentences) / max(1, len(paragraphs)),
                'punctuation_count': sum(1 for char in text if not char.isalnum() and not char.isspace()),
                'uppercase_count': sum(1 for char in text if char.isupper()),
                'digit_count': sum(1 for char in text if char.isdigit())
            }
        except Exception as e:
            print(f"Error calculating text statistics: {str(e)}")
            return {}

    def train_models(self, training_data):
        """Train content analysis models"""
        try:
            # Prepare training data
            texts = []
            categories = []
            sentiments = []
            quality_scores = []
            
            for item in training_data:
                text = self._extract_text(item)
                if text.strip():
                    texts.append(text)
                    categories.append(item.get('category', 'general'))
                    sentiments.append(item.get('sentiment', 'neutral'))
                    quality_scores.append(item.get('quality_score', 0.5))
            
            if len(texts) < 10:
                return {'status': 'error', 'message': 'Insufficient training data'}
            
            # Preprocess texts
            processed_texts = [self._preprocess_text(text) for text in texts]
            
            # Vectorize texts
            X_tfidf = self.tfidf_vectorizer.fit_transform(processed_texts)
            X_count = self.count_vectorizer.fit_transform(processed_texts)
            
            # Train text classifier
            self.text_classifier.fit(X_tfidf, categories)
            
            # Train sentiment classifier
            self.sentiment_classifier.fit(X_count, sentiments)
            
            # Train topic model
            self.topic_model.fit(X_count)
            
            # Train quality model
            quality_features = []
            for text in processed_texts:
                features = self._extract_text_features(text)
                quality_features.append(self._prepare_quality_features(features))
            
            self.content_quality_model.fit(quality_features, quality_scores)
            
            self.is_trained = True
            
            return {
                'status': 'success',
                'training_samples': len(texts),
                'models_trained': ['text_classifier', 'sentiment_classifier', 'topic_model', 'quality_model']
            }
        except Exception as e:
            print(f"Error training models: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def save_model(self, filepath):
        """Save trained models"""
        try:
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'count_vectorizer': self.count_vectorizer,
                'text_classifier': self.text_classifier,
                'sentiment_classifier': self.sentiment_classifier,
                'topic_model': self.topic_model,
                'content_quality_model': self.content_quality_model,
                'clustering_model': self.clustering_model,
                'positive_words': self.positive_words,
                'negative_words': self.negative_words,
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
            
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.count_vectorizer = model_data['count_vectorizer']
            self.text_classifier = model_data['text_classifier']
            self.sentiment_classifier = model_data['sentiment_classifier']
            self.topic_model = model_data['topic_model']
            self.content_quality_model = model_data['content_quality_model']
            self.clustering_model = model_data['clustering_model']
            self.positive_words = model_data['positive_words']
            self.negative_words = model_data['negative_words']
            self.is_trained = model_data['is_trained']
            
            return {'status': 'success', 'message': f'Model loaded from {filepath}'}
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the content analysis system
    content_analyzer = ContentAnalysisSystem()
    
    # Sample content data
    sample_content = {
        'content_id': 'content_123',
        'title': 'Introduction to Machine Learning',
        'description': 'A comprehensive guide to machine learning concepts',
        'text': 'Machine learning is a fascinating field of artificial intelligence that enables computers to learn from data without being explicitly programmed. This comprehensive guide covers the fundamental concepts, algorithms, and applications of machine learning. You will learn about supervised learning, unsupervised learning, and reinforcement learning techniques.',
        'questions': [
            {'question': 'What is machine learning?', 'answer': 'Machine learning is a subset of artificial intelligence.'},
            {'question': 'What are the main types of machine learning?', 'answer': 'The main types are supervised, unsupervised, and reinforcement learning.'}
        ]
    }
    
    # Analyze content
    analysis_result = content_analyzer.analyze_text_content(sample_content)
    print("Content Analysis Result:", json.dumps(analysis_result, indent=2, default=str))
