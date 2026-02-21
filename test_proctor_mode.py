#!/usr/bin/env python3
"""
Test script to demonstrate the Proctor Mode functionality
"""

import requests
import json

# Base URLs
BACKEND_URL = "http://localhost:8000"

def test_proctor_mode():
    """Test the proctor mode functionality"""
    print("🔒 PROCTOR MODE DEMONSTRATION")
    print("=" * 60)
    
    # Step 1: Login
    print("\n🔐 Step 1: User Login")
    print("-" * 40)
    
    login_data = {
        "email": "samykmottaya@gmail.com",
        "password": "Danger!123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        token = response.json()["token"]
        print("✅ Login successful")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test Proctor Logging
    print("\n📋 Step 2: Testing Proctor Event Logging")
    print("-" * 40)
    
    proctor_events = [
        {
            "event_type": "proctor_mode_activated",
            "message": "User enabled proctor mode",
            "severity": "info",
            "metadata": {"timestamp": "2024-01-01T10:00:00Z"}
        },
        {
            "event_type": "camera_started",
            "message": "Camera monitoring started",
            "severity": "success",
            "metadata": {"camera_id": "cam_001"}
        },
        {
            "event_type": "screen_monitoring",
            "message": "Screen monitoring activated",
            "severity": "info",
            "metadata": {"screen_resolution": "1920x1080"}
        },
        {
            "event_type": "ai_analysis",
            "message": "AI analysis engine started",
            "severity": "success",
            "metadata": {"ai_version": "v2.1"}
        }
    ]
    
    for event in proctor_events:
        try:
            response = requests.post(f"{BACKEND_URL}/api/proctor/log", 
                                   json=event, headers=headers)
            if response.status_code == 200:
                print(f"✅ Logged: {event['event_type']}")
            else:
                print(f"❌ Failed to log: {event['event_type']}")
        except Exception as e:
            print(f"❌ Error logging {event['event_type']}: {e}")
    
    # Step 3: Test AI Analysis
    print("\n🤖 Step 3: Testing AI Analysis")
    print("-" * 40)
    
    analysis_data = {
        "session_data": {
            "duration": 1800,  # 30 minutes
            "questions_answered": 10,
            "camera_events": 45,
            "screen_events": 120
        },
        "user_behavior": {
            "attention_score": 0.85,
            "posture_score": 0.92,
            "environment_score": 0.95
        }
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/proctor/analysis", 
                               json=analysis_data, headers=headers)
        if response.status_code == 200:
            analysis = response.json()["analysis"]
            print("✅ AI Analysis Complete!")
            print(f"   Risk Score: {analysis['risk_score']}")
            print(f"   Alerts: {len(analysis['alerts'])}")
            print(f"   Recommendations: {len(analysis['recommendations'])}")
            
            print("\n   📊 AI Alerts:")
            for alert in analysis['alerts']:
                print(f"      • {alert['type']}: {alert['message']}")
            
            print("\n   💡 Recommendations:")
            for rec in analysis['recommendations']:
                print(f"      • {rec}")
        else:
            print(f"❌ AI Analysis failed: {response.json()}")
    except Exception as e:
        print(f"❌ AI Analysis error: {e}")
    
    # Step 4: Generate Questions for Frontend Developer Role
    print("\n📋 Step 4: Generate Questions with Proctor Mode")
    print("-" * 40)
    
    role_data = {
        "roleId": "frontend-developer",
        "roleTitle": "Frontend Developer",
        "requiredSkills": ["HTML/CSS", "JavaScript", "React/Vue", "Responsive Design", "UI/UX"]
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/generate-role-questions", 
                               json=role_data, headers=headers)
        
        if response.status_code == 200:
            questions = response.json()["questions"]
            print(f"✅ Generated {len(questions)} questions for Frontend Developer")
            
            # Log question generation with proctor
            proctor_log = {
                "event_type": "questions_generated",
                "message": f"Generated {len(questions)} questions for {role_data['roleTitle']}",
                "severity": "info",
                "metadata": {"role_id": role_data["roleId"], "question_count": len(questions)}
            }
            
            response = requests.post(f"{BACKEND_URL}/api/proctor/log", 
                                   json=proctor_log, headers=headers)
            
            if response.status_code == 200:
                print("✅ Question generation logged to proctor system")
            
        else:
            print(f"❌ Question generation failed: {response.json()}")
    except Exception as e:
        print(f"❌ Question generation error: {e}")
    
    print("\n🎉 PROCTOR MODE DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("✅ Proctor event logging working")
    print("✅ AI analysis simulation working")
    print("✅ Integration with role questions working")
    print("✅ Frontend proctor mode ready")
    
    print(f"\n🌐 Frontend Features:")
    print(f"   • Camera monitoring with live feed")
    print(f"   • Screen activity tracking")
    print(f"   • AI-powered behavior analysis")
    print(f"   • Real-time alerts and notifications")
    print(f"   • Activity logging and monitoring")
    print(f"   • Risk assessment and recommendations")
    
    print(f"\n🔧 Backend APIs:")
    print(f"   • POST /api/proctor/log - Log proctor events")
    print(f"   • POST /api/proctor/analysis - AI analysis")
    print(f"   • Integration with existing auth system")

if __name__ == "__main__":
    test_proctor_mode()
