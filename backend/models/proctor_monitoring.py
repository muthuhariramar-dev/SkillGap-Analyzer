"""
Proctor Mode Monitoring - Computer Vision for Face Detection, Gaze Tracking, Posture Analysis
"""

import cv2
import numpy as np
import mediapipe as mp
import face_recognition
import dlib
from typing import Dict, List, Tuple, Optional
import json
import time
from datetime import datetime
import logging

class ProctorMonitoringSystem:
    """
    Comprehensive proctoring system with computer vision capabilities
    """
    
    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        
        # Initialize face detection models
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5
        )
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        
        # Initialize face recognition
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Behavioral tracking
        self.gaze_history = []
        self.posture_history = []
        self.behavioral_patterns = []
        
        # Anomaly detection thresholds
        self.gaze_threshold = 0.3  # 30% of time looking away
        self.posture_threshold = 0.2  # 20% of time in bad posture
        self.movement_threshold = 0.1  # 10% excessive movement
        
        # Fullscreen detection
        self.is_fullscreen = False
        self.fullscreen_violations = 0
        self.max_fullscreen_violations = 3  # Max violations before termination
        
        # Session management
        self.session_active = False
        self.session_id = None
        self.termination_reason = None
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start_proctoring_session(self, session_id: str, user_id: str) -> Dict:
        """
        Start a new proctoring session
        """
        try:
            self.session_id = session_id
            self.session_active = True
            self.fullscreen_violations = 0
            self.termination_reason = None
            
            # Clear previous session data
            self.gaze_history = []
            self.posture_history = []
            self.behavioral_patterns = []
            
            self.logger.info(f"Started proctoring session: {session_id} for user: {user_id}")
            
            return {
                'success': True,
                'session_id': session_id,
                'message': 'Proctoring session started successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Error starting proctoring session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_fullscreen_status(self) -> Dict:
        """
        Check if user is in fullscreen mode
        """
        try:
            # Check if any window is in fullscreen
            is_fullscreen = (
                hasattr(self, '_is_fullscreen') and self._is_fullscreen or
                False  # Default to False if not detected
            )
            
            # Check for fullscreen violations
            if self.session_active and not is_fullscreen:
                self.fullscreen_violations += 1
                self.logger.warning(f"Fullscreen violation detected. Total violations: {self.fullscreen_violations}")
                
                # Check if should terminate
                if self.fullscreen_violations >= self.max_fullscreen_violations:
                    return self.terminate_session('EXCESSIVE_FULLSCREEN_VIOLATIONS')
            
            self.is_fullscreen = is_fullscreen
            
            return {
                'is_fullscreen': is_fullscreen,
                'violations': self.fullscreen_violations,
                'max_violations': self.max_fullscreen_violations
            }
            
        except Exception as e:
            self.logger.error(f"Error checking fullscreen status: {e}")
            return {
                'is_fullscreen': False,
                'error': str(e)
            }
    
    def detect_mischievous_activities(self, frame: np.ndarray, previous_frames: List[np.ndarray]) -> Dict:
        """
        Detect suspicious activities during assessment
        """
        try:
            suspicious_activities = []
            
            # Check for multiple faces (potential collaboration)
            faces = self.detect_faces(frame)
            if len(faces) > 1:
                suspicious_activities.append({
                    'type': 'MULTIPLE_FACES_DETECTED',
                    'severity': 'HIGH',
                    'face_count': len(faces),
                    'timestamp': datetime.now().isoformat(),
                    'description': f'Multiple faces ({len(faces)}) detected - possible collaboration'
                })
            
            # Check for no face (potential absence)
            elif len(faces) == 0 and self.session_active:
                suspicious_activities.append({
                    'type': 'NO_FACE_DETECTED',
                    'severity': 'MEDIUM',
                    'timestamp': datetime.now().isoformat(),
                    'description': 'No face detected - user may be absent'
                })
            
            # Check for phone/tablet detection (based on hand position)
            if len(previous_frames) >= 2:
                movement_analysis = self.detect_behavioral_anomalies(frame, previous_frames)
                for anomaly in movement_analysis:
                    if anomaly['type'] in ['excessive_movement', 'sudden_movements']:
                        suspicious_activities.append({
                            'type': 'SUSPICIOUS_MOVEMENT',
                            'severity': anomaly['severity'],
                            'timestamp': anomaly['timestamp'],
                            'description': f'Suspicious movement detected: {anomaly["type"]}'
                        })
            
            # Check for unauthorized materials (books, notes, etc.)
            unauthorized_objects = self.detect_unauthorized_objects(frame)
            if unauthorized_objects:
                suspicious_activities.append({
                    'type': 'UNAUTHORIZED_MATERIALS',
                    'severity': 'HIGH',
                    'objects_detected': unauthorized_objects,
                    'timestamp': datetime.now().isoformat(),
                    'description': 'Unauthorized materials detected in assessment area'
                })
            
            # Check for screen sharing/mirroring
            screen_anomalies = self.detect_screen_anomalies(frame)
            if screen_anomalies:
                suspicious_activities.append({
                    'type': 'SCREEN_ANOMALIES',
                    'severity': 'MEDIUM',
                    'anomalies': screen_anomalies,
                    'timestamp': datetime.now().isoformat(),
                    'description': 'Screen anomalies detected - possible screen sharing'
                })
            
            return {
                'suspicious_activities': suspicious_activities,
                'immediate_termination': any(activity['severity'] == 'HIGH' for activity in suspicious_activities)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting mischievous activities: {e}")
            return {
                'suspicious_activities': [],
                'error': str(e)
            }
    
    def detect_unauthorized_objects(self, frame: np.ndarray) -> List[str]:
        """
        Detect unauthorized objects like books, phones, notes
        """
        try:
            # Convert to grayscale for object detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Simple object detection using contours (placeholder implementation)
            contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            unauthorized_objects = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter for book-sized objects
                if 5000 < area < 50000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Check for book-like aspect ratio
                    if 0.5 < aspect_ratio < 2.0:
                        unauthorized_objects.append('book_or_document')
                
                # Filter for phone-sized objects
                elif 1000 < area < 10000:
                    unauthorized_objects.append('electronic_device')
            
            return unauthorized_objects
            
        except Exception as e:
            self.logger.error(f"Error detecting unauthorized objects: {e}")
            return []
    
    def detect_screen_anomalies(self, frame: np.ndarray) -> List[str]:
        """
        Detect screen anomalies like screen sharing or unusual display patterns
        """
        try:
            anomalies = []
            
            # Check for unusual brightness (could indicate screen recording)
            brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            if brightness < 50 or brightness > 200:
                anomalies.append('unusual_brightness')
            
            # Check for screen recording indicators
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Red recording dot detection
            red_lower = np.array([0, 120, 70])
            red_upper = np.array([10, 255, 255])
            red_mask = cv2.inRange(hsv, red_lower, red_upper)
            red_pixels = cv2.countNonZero(red_mask)
            
            if red_pixels > 100:
                anomalies.append('recording_indicator')
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error detecting screen anomalies: {e}")
            return []
    
    def terminate_session(self, reason: str) -> Dict:
        """
        Terminate proctoring session with specific reason
        """
        try:
            self.session_active = False
            self.termination_reason = reason
            
            # Generate final report
            final_report = self.generate_proctor_report(self.session_id or 'unknown')
            final_report['termination_reason'] = reason
            final_report['termination_timestamp'] = datetime.now().isoformat()
            
            self.logger.warning(f"Proctoring session terminated: {reason}")
            
            return {
                'success': True,
                'session_id': self.session_id,
                'termination_reason': reason,
                'final_report': final_report,
                'message': f'Session terminated due to: {reason}'
            }
            
        except Exception as e:
            self.logger.error(f"Error terminating session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_frame_with_proctoring(self, frame: np.ndarray, previous_frames: List[np.ndarray]) -> Dict:
        """
        Comprehensive frame analysis with proctoring checks
        """
        try:
            if not self.session_active:
                return {'status': 'SESSION_INACTIVE'}
            
            # Basic face and gaze analysis
            faces = self.detect_faces(frame)
            gaze_data = {}
            posture_data = {}
            
            if faces:
                face_data = faces[0]
                gaze_data = self.analyze_gaze_tracking(frame, face_data)
                posture_data = self.analyze_posture_tracking(frame, face_data)
            
            # Check fullscreen status
            fullscreen_status = self.check_fullscreen_status()
            
            # Detect mischievous activities
            suspicious_activities = self.detect_mischievous_activities(frame, previous_frames)
            
            # Determine if immediate termination is needed
            should_terminate = suspicious_activities.get('immediate_termination', False)
            if should_terminate:
                termination_result = self.terminate_session('MISCHIEVOUS_ACTIVITY_DETECTED')
                return {
                    'status': 'TERMINATED',
                    'termination_result': termination_result,
                    'suspicious_activities': suspicious_activities
                }
            
            return {
                'status': 'ACTIVE',
                'faces_detected': len(faces),
                'gaze_data': gaze_data,
                'posture_data': posture_data,
                'fullscreen_status': fullscreen_status,
                'suspicious_activities': suspicious_activities,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive frame analysis: {e}")
            return {
                'status': 'ERROR',
                'error': str(e)
            }
    
    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect faces in the frame using MediaPipe
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_frame)
            
            faces = []
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    
                    face_data = {
                        'bbox': {
                            'x': int(bbox.xmin * w),
                            'y': int(bbox.ymin * h),
                            'width': int(bbox.width * w),
                            'height': int(bbox.height * h)
                        },
                        'confidence': detection.score[0],
                        'timestamp': datetime.now().isoformat()
                    }
                    faces.append(face_data)
            
            return faces
            
        except Exception as e:
            self.logger.error(f"Face detection error: {e}")
            return []
    
    def analyze_gaze_tracking(self, frame: np.ndarray, face_data: Dict) -> Dict:
        """
        Analyze gaze direction using eye landmarks
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                
                # Eye landmarks (MediaPipe indices)
                left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133]
                right_eye_indices = [362, 398, 384, 385, 386, 387, 388, 466, 263]
                
                # Calculate eye centers
                left_eye_center = self._calculate_eye_center(landmarks, left_eye_indices)
                right_eye_center = self._calculate_eye_center(landmarks, right_eye_indices)
                
                # Gaze estimation
                gaze_direction = self._estimate_gaze_direction(
                    left_eye_center, right_eye_center, frame.shape
                )
                
                gaze_data = {
                    'gaze_direction': gaze_direction,
                    'looking_at_screen': self._is_looking_at_screen(gaze_direction),
                    'eye_openness': self._calculate_eye_openness(landmarks),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.gaze_history.append(gaze_data)
                return gaze_data
            
            return {'looking_at_screen': False, 'timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Gaze tracking error: {e}")
            return {'looking_at_screen': False, 'timestamp': datetime.now().isoformat()}
    
    def analyze_posture(self, frame: np.ndarray) -> Dict:
        """
        Analyze user posture using pose estimation
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            
            posture_data = {
                'shoulder_alignment': 0.0,
                'head_position': 'normal',
                'body_lean': 0.0,
                'posture_score': 0.0,
                'timestamp': datetime.now().isoformat()
            }
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmarks
                
                # Key pose landmarks
                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]
                nose = landmarks[0]
                left_hip = landmarks[23]
                right_hip = landmarks[24]
                
                # Calculate shoulder alignment
                shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
                posture_data['shoulder_alignment'] = shoulder_diff
                
                # Calculate head position
                head_center_y = nose.y
                shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
                head_shoulder_ratio = head_center_y / shoulder_center_y
                
                if head_shoulder_ratio < 0.8:
                    posture_data['head_position'] = 'forward'
                elif head_shoulder_ratio > 1.2:
                    posture_data['head_position'] = 'backward'
                else:
                    posture_data['head_position'] = 'normal'
                
                # Calculate body lean
                hip_center_y = (left_hip.y + right_hip.y) / 2
                body_lean = abs(shoulder_center_y - hip_center_y)
                posture_data['body_lean'] = body_lean
                
                # Calculate overall posture score
                posture_score = self._calculate_posture_score(posture_data)
                posture_data['posture_score'] = posture_score
                
                self.posture_history.append(posture_data)
            
            return posture_data
            
        except Exception as e:
            self.logger.error(f"Posture analysis error: {e}")
            return {'posture_score': 0.0, 'timestamp': datetime.now().isoformat()}
    
    def detect_behavioral_anomalies(self, current_frame: np.ndarray, 
                                  previous_frames: List[np.ndarray]) -> List[Dict]:
        """
        Detect behavioral anomalies using movement analysis
        """
        try:
            anomalies = []
            
            if len(previous_frames) < 2:
                return anomalies
            
            # Calculate movement between frames
            movement_data = self._calculate_movement_metrics(current_frame, previous_frames)
            
            # Detect excessive movement
            if movement_data['total_movement'] > self.movement_threshold:
                anomalies.append({
                    'type': 'excessive_movement',
                    'severity': 'high' if movement_data['total_movement'] > 0.2 else 'medium',
                    'movement_value': movement_data['total_movement'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # Detect sudden movements
            if movement_data['sudden_movements'] > 3:
                anomalies.append({
                    'type': 'sudden_movements',
                    'severity': 'medium',
                    'movement_count': movement_data['sudden_movements'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # Store behavioral patterns
            self.behavioral_patterns.append({
                'movement_data': movement_data,
                'timestamp': datetime.now().isoformat()
            })
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Behavioral anomaly detection error: {e}")
            return []
    
    def generate_proctor_report(self, session_id: str) -> Dict:
        """
        Generate comprehensive proctoring report
        """
        try:
            report = {
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'face_detection_summary': self._analyze_face_detection_history(),
                'gaze_analysis_summary': self._analyze_gaze_history(),
                'posture_analysis_summary': self._analyze_posture_history(),
                'behavioral_anomalies': self._get_behavioral_anomalies(),
                'overall_compliance_score': self._calculate_compliance_score(),
                'recommendations': self._generate_recommendations()
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation error: {e}")
            return {'error': str(e)}
    
    # Helper methods
    def _calculate_eye_center(self, landmarks: List, eye_indices: List) -> Tuple[float, float]:
        """Calculate center of eye using landmarks"""
        x_coords = [landmarks[i].x for i in eye_indices]
        y_coords = [landmarks[i].y for i in eye_indices]
        return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))
    
    def _estimate_gaze_direction(self, left_eye: Tuple, right_eye: Tuple, 
                               frame_shape: Tuple) -> Dict:
        """Estimate gaze direction from eye positions"""
        eye_center = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2)
        frame_center = (0.5, 0.5)
        
        gaze_x = eye_center[0] - frame_center[0]
        gaze_y = eye_center[1] - frame_center[1]
        
        return {
            'x_offset': gaze_x,
            'y_offset': gaze_y,
            'direction': self._classify_gaze_direction(gaze_x, gaze_y)
        }
    
    def _classify_gaze_direction(self, x_offset: float, y_offset: float) -> str:
        """Classify gaze direction into categories"""
        if abs(x_offset) < 0.1 and abs(y_offset) < 0.1:
            return 'center'
        elif x_offset > 0.1:
            return 'right'
        elif x_offset < -0.1:
            return 'left'
        elif y_offset > 0.1:
            return 'down'
        else:
            return 'up'
    
    def _is_looking_at_screen(self, gaze_direction: Dict) -> bool:
        """Determine if user is looking at screen"""
        return (abs(gaze_direction['x_offset']) < 0.3 and 
                abs(gaze_direction['y_offset']) < 0.3)
    
    def _calculate_eye_openness(self, landmarks: List) -> float:
        """Calculate eye openness ratio"""
        # Simplified eye openness calculation
        return 0.8  # Placeholder - implement actual calculation
    
    def _calculate_posture_score(self, posture_data: Dict) -> float:
        """Calculate overall posture score (0-1)"""
        score = 1.0
        
        # Deduct points for poor posture
        if posture_data['shoulder_alignment'] > 0.1:
            score -= 0.2
        
        if posture_data['head_position'] != 'normal':
            score -= 0.3
        
        if posture_data['body_lean'] > 0.3:
            score -= 0.2
        
        return max(0.0, score)
    
    def _calculate_movement_metrics(self, current_frame: np.ndarray, 
                                   previous_frames: List[np.ndarray]) -> Dict:
        """Calculate movement metrics between frames"""
        # Simplified movement calculation
        return {
            'total_movement': 0.05,  # Placeholder
            'sudden_movements': 1,    # Placeholder
            'movement_areas': []      # Placeholder
        }
    
    def _analyze_face_detection_history(self) -> Dict:
        """Analyze face detection history"""
        if not self.gaze_history:
            return {'face_detected_percentage': 0.0}
        
        face_detected_count = sum(1 for _ in self.gaze_history)
        total_frames = len(self.gaze_history)
        
        return {
            'face_detected_percentage': (face_detected_count / total_frames) * 100,
            'total_frames_analyzed': total_frames
        }
    
    def _analyze_gaze_history(self) -> Dict:
        """Analyze gaze tracking history"""
        if not self.gaze_history:
            return {'looking_at_screen_percentage': 0.0}
        
        looking_at_screen_count = sum(1 for gaze in self.gaze_history 
                                    if gaze.get('looking_at_screen', False))
        total_frames = len(self.gaze_history)
        
        return {
            'looking_at_screen_percentage': (looking_at_screen_count / total_frames) * 100,
            'gaze_directions': [gaze.get('gaze_direction', {}) for gaze in self.gaze_history]
        }
    
    def _analyze_posture_history(self) -> Dict:
        """Analyze posture history"""
        if not self.posture_history:
            return {'average_posture_score': 0.0}
        
        posture_scores = [posture.get('posture_score', 0.0) for posture in self.posture_history]
        avg_score = sum(posture_scores) / len(posture_scores)
        
        return {
            'average_posture_score': avg_score,
            'posture_trend': 'stable'  # Placeholder - implement trend analysis
        }
    
    def _get_behavioral_anomalies(self) -> List[Dict]:
        """Get behavioral anomalies from history"""
        anomalies = []
        for pattern in self.behavioral_patterns:
            if 'anomaly' in pattern:
                anomalies.append(pattern['anomaly'])
        return anomalies
    
    def _calculate_compliance_score(self) -> float:
        """Calculate overall compliance score"""
        gaze_score = self._analyze_gaze_history().get('looking_at_screen_percentage', 0) / 100
        posture_score = self._analyze_posture_history().get('average_posture_score', 0)
        
        return (gaze_score * 0.6 + posture_score * 0.4)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        gaze_analysis = self._analyze_gaze_history()
        if gaze_analysis.get('looking_at_screen_percentage', 0) < 80:
            recommendations.append("Maintain focus on screen during assessment")
        
        posture_analysis = self._analyze_posture_history()
        if posture_analysis.get('average_posture_score', 0) < 0.7:
            recommendations.append("Improve sitting posture for better concentration")
        
        return recommendations

# Initialize global proctor monitoring system
proctor_system = ProctorMonitoringSystem()
