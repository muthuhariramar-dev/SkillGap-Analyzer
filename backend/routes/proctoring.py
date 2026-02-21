from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

# Create Blueprint
proctoring_bp = Blueprint('proctoring', __name__)

# Store active sessions
active_sessions = {}

# Start proctoring session
@proctoring_bp.route('/start', methods=['POST'])
def start_proctoring():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        user_id = data.get('userId')
        role = data.get('role')
        
        if not session_id or not user_id:
            return jsonify({
                'success': False,
                'message': 'Session ID and User ID are required'
            }), 400
        
        # Store session info
        active_sessions[session_id] = {
            'userId': user_id,
            'role': role,
            'startTime': datetime.now().isoformat(),
            'status': 'ACTIVE'
        }
        
        return jsonify({
            'success': True,
            'sessionId': session_id,
            'message': 'Proctoring session started successfully'
        })
    except Exception as error:
        print(f'Error starting proctoring session: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to start proctoring session',
            'error': str(error)
        }), 500

# Analyze frame for proctoring
@proctoring_bp.route('/analyze-frame', methods=['POST'])
def analyze_frame():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        frame_data = data.get('frameData')
        previous_frames = data.get('previousFrames', [])
        
        if not session_id or not frame_data:
            return jsonify({
                'success': False,
                'message': 'Session ID and frame data are required'
            }), 400
        
        # Check if session is active
        session = active_sessions.get(session_id)
        if not session or session.get('status') != 'ACTIVE':
            return jsonify({
                'success': False,
                'message': 'Invalid or inactive session'
            }), 400
        
        # For now, create a simple frame analysis result
        # In a real implementation, you'd process the actual image data
        analysis_result = {
            'status': 'ACTIVE',
            'faces_detected': 1,
            'gaze_data': {
                'looking_at_screen': True,
                'gaze_direction': 'center'
            },
            'posture_data': {
                'posture_score': 0.8,
                'head_position': 'normal'
            },
            'fullscreen_status': {
                'is_fullscreen': True,
                'violations': 0
            },
            'suspicious_activities': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Check for suspicious activities
        if analysis_result['suspicious_activities']:
            high_severity_activities = [
                activity for activity in analysis_result['suspicious_activities'] 
                if activity.get('severity') == 'HIGH'
            ]
            
            if high_severity_activities:
                # Update session status
                active_sessions[session_id]['status'] = 'TERMINATED'
                active_sessions[session_id]['endTime'] = datetime.now().isoformat()
                active_sessions[session_id]['terminationReason'] = 'MISCHIEVOUS_ACTIVITY_DETECTED'
                
                return jsonify({
                    'success': True,
                    'status': 'TERMINATED',
                    'terminationResult': {
                        'success': True,
                        'sessionId': session_id,
                        'termination_reason': 'MISCHIEVOUS_ACTIVITY_DETECTED',
                        'final_report': analysis_result,
                        'message': 'Session terminated due to suspicious activity'
                    },
                    'message': 'Session terminated due to suspicious activity'
                })
        
        return jsonify({
            'success': True,
            'analysisResult': analysis_result,
            'message': 'Frame analysis completed'
        })
        
    except Exception as error:
        print(f'Error analyzing frame: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to analyze frame',
            'error': str(error)
        }), 500

# Check fullscreen status
@proctoring_bp.route('/check-fullscreen', methods=['POST'])
def check_fullscreen():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Session ID is required'
            }), 400
        
        # For now, return a simple fullscreen status
        fullscreen_status = {
            'is_fullscreen': True,
            'violations': 0,
            'max_violations': 3
        }
        
        return jsonify({
            'success': True,
            'fullscreenStatus': fullscreen_status,
            'message': 'Fullscreen status checked'
        })
        
    except Exception as error:
        print(f'Error checking fullscreen status: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to check fullscreen status',
            'error': str(error)
        }), 500

# Terminate proctoring session
@proctoring_bp.route('/terminate', methods=['POST'])
def terminate_session():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        reason = data.get('reason')
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Session ID is required'
            }), 400
        
        # Update session status
        session = active_sessions.get(session_id)
        if session:
            active_sessions[session_id]['status'] = 'TERMINATED'
            active_sessions[session_id]['endTime'] = datetime.now().isoformat()
            active_sessions[session_id]['terminationReason'] = reason or 'USER_TERMINATED'
        
        return jsonify({
            'success': True,
            'terminationResult': {
                'success': True,
                'sessionId': session_id,
                'termination_reason': reason or 'USER_TERMINATED',
                'message': 'Proctoring session terminated'
            },
            'message': 'Proctoring session terminated'
        })
        
    except Exception as error:
        print(f'Error terminating session: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to terminate session',
            'error': str(error)
        }), 500

# Get session status
@proctoring_bp.route('/session/<session_id>', methods=['GET'])
def get_session_status(session_id):
    try:
        session = active_sessions.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session': session,
            'message': 'Session status retrieved'
        })
        
    except Exception as error:
        print(f'Error getting session status: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to get session status',
            'error': str(error)
        }), 500

# Get all active sessions
@proctoring_bp.route('/sessions', methods=['GET'])
def get_all_sessions():
    try:
        sessions = []
        for session_id, session_data in active_sessions.items():
            sessions.append({
                'sessionId': session_id,
                **session_data
            })
        
        active_count = len([s for s in sessions if s.get('status') == 'ACTIVE'])
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'activeCount': active_count,
            'message': 'Active sessions retrieved'
        })
        
    except Exception as error:
        print(f'Error getting sessions: {error}')
        return jsonify({
            'success': False,
            'message': 'Failed to get sessions',
            'error': str(error)
        }), 500
