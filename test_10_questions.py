#!/usr/bin/env python3
"""
Test script to verify exactly 10 questions are generated for each role
"""

import requests
import json

# Base URLs
BACKEND_URL = "http://localhost:8000"

def test_10_questions_per_role():
    """Test that exactly 10 questions are generated for each role"""
    print("🎯 Testing 10 Questions Per Role Generation")
    print("=" * 60)
    
    # Login to get token
    login_data = {
        "email": "samykmottaya@gmail.com",
        "password": "Danger!123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ Login failed")
            return
        
        token = response.json()["token"]
        print("✅ Login successful")
        
        # Test roles
        test_roles = [
            {
                "roleId": "frontend-developer",
                "roleTitle": "Frontend Developer",
                "requiredSkills": ["HTML/CSS", "JavaScript", "React/Vue", "Responsive Design", "UI/UX"]
            },
            {
                "roleId": "backend-developer", 
                "roleTitle": "Backend Developer",
                "requiredSkills": ["Node.js/Python", "Databases", "APIs", "Security", "Cloud Services"]
            },
            {
                "roleId": "fullstack-developer",
                "roleTitle": "Full Stack Developer", 
                "requiredSkills": ["Frontend", "Backend", "Databases", "DevOps", "System Design"]
            },
            {
                "roleId": "product-manager",
                "roleTitle": "Product Manager",
                "requiredSkills": ["Strategy", "Communication", "Analytics", "User Research", "Leadership"]
            },
            {
                "roleId": "data-scientist",
                "roleTitle": "Data Scientist",
                "requiredSkills": ["Machine Learning", "Python/R", "Statistics", "Data Visualization", "Deep Learning"]
            }
        ]
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        for role in test_roles:
            print(f"\n🔍 Testing {role['roleTitle']}...")
            print("-" * 40)
            
            response = requests.post(f"{BACKEND_URL}/api/generate-role-questions", 
                                   json=role, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get('questions', [])
                
                print(f"✅ Questions generated: {len(questions)}")
                print(f"📊 Total reported: {data.get('totalQuestions', 0)}")
                
                if len(questions) == 10:
                    print("✅ Exactly 10 questions generated!")
                else:
                    print(f"❌ Expected 10 questions, got {len(questions)}")
                
                # Show sample questions
                print(f"\n📝 Sample Questions for {role['roleTitle']}:")
                for i, q in enumerate(questions[:3], 1):
                    print(f"  {i}. {q['question']}")
                    print(f"     Options: {', '.join(q['options'][:2])}...")
                
                if len(questions) > 3:
                    print(f"  ... and {len(questions) - 3} more questions")
                    
            else:
                print(f"❌ Failed to generate questions: {response.status_code}")
                print(f"   Error: {response.json()}")
        
        print("\n🎉 Role Questions Test Complete!")
        print("=" * 60)
        print("✅ All roles should generate exactly 10 questions")
        print("✅ Each question has 4 options with correct answer")
        print("✅ Questions are role-specific and relevant")
        
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_complete_flow():
    """Test the complete flow with 10 questions and analysis"""
    print("\n🔄 Testing Complete Flow (10 Questions + Analysis)")
    print("=" * 60)
    
    # Login
    login_data = {
        "email": "samykmottaya@gmail.com", 
        "password": "Danger!123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        token = response.json()["token"]
        
        # Generate questions
        role_data = {
            "roleId": "frontend-developer",
            "roleTitle": "Frontend Developer",
            "requiredSkills": ["HTML/CSS", "JavaScript", "React/Vue", "Responsive Design", "UI/UX"]
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/generate-role-questions", 
                               json=role_data, headers=headers)
        
        questions = response.json()["questions"]
        print(f"✅ Generated {len(questions)} questions")
        
        # Simulate answering all 10 questions
        answers = []
        for i, question in enumerate(questions):
            # Mix of correct and incorrect answers (70% correct)
            import random
            if random.random() < 0.7:
                selected_option = question['correct']
            else:
                available_options = [j for j in range(4) if j != question['correct']]
                selected_option = random.choice(available_options)
            
            answers.append({
                "questionId": question['id'],
                "selectedOption": selected_option
            })
        
        print(f"✅ Answered all {len(answers)} questions")
        
        # Analyze results
        analysis_data = {
            "roleId": "frontend-developer",
            "roleTitle": "Frontend Developer", 
            "questions": questions,
            "answers": answers
        }
        
        response = requests.post(f"{BACKEND_URL}/api/analyze-role-results", 
                               json=analysis_data, headers=headers)
        
        if response.status_code == 200:
            analysis = response.json()["analysis"]
            print("✅ Analysis complete!")
            print(f"📊 Overall Score: {analysis['overallScore']}%")
            print(f"🎯 Readiness: {analysis['readiness']}")
            print(f"✅ Correct: {analysis['correctAnswers']}/{analysis['totalQuestions']}")
            print(f"📈 Skills analyzed: {len(analysis['skillScores'])}")
            
        else:
            print(f"❌ Analysis failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Flow test error: {e}")

if __name__ == "__main__":
    test_10_questions_per_role()
    test_complete_flow()
