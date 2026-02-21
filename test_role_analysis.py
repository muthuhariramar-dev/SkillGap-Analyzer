#!/usr/bin/env python3
"""
Test script to demonstrate the role-specific skill analysis with 10 questions
"""

import requests
import json
import time

# Base URLs
BACKEND_URL = "http://localhost:8000"

def test_role_analysis():
    """Test the complete role analysis flow"""
    print("🚀 Testing Role-Specific Skill Analysis Flow")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("\n📝 Step 1: Logging in...")
    login_data = {
        "email": "samykmottaya@gmail.com",
        "password": "Danger!123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["token"]
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Generate questions for Frontend Developer role
    print("\n📋 Step 2: Generating questions for Frontend Developer...")
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
            print(f"✅ Generated {len(questions)} questions!")
            
            # Display first 10 questions
            print("\n📚 Questions (First 10):")
            print("-" * 50)
            for i, question in enumerate(questions[:10], 1):
                print(f"\nQuestion {i}: {question['question']}")
                for j, option in enumerate(question['options']):
                    marker = "✓" if j == question['correct'] else " "
                    print(f"  {marker} {j+1}. {option}")
                print(f"  💡 Explanation: {question['explanation']}")
            
        else:
            print(f"❌ Failed to generate questions: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        return
    
    # Step 3: Submit answers for analysis
    print("\n📊 Step 3: Submitting answers for analysis...")
    
    # Simulate user answers (mix of correct and incorrect)
    answers = []
    for i, question in enumerate(questions[:10]):
        # Simulate realistic answers - 70% correct
        import random
        if random.random() < 0.7:
            selected_option = question['correct']  # Correct answer
        else:
            # Select an incorrect answer
            available_options = [j for j in range(len(question['options'])) if j != question['correct']]
            selected_option = random.choice(available_options)
        
        answers.append({
            "questionId": question['id'],
            "selectedOption": selected_option
        })
    
    analysis_data = {
        "roleId": "frontend-developer",
        "roleTitle": "Frontend Developer",
        "questions": questions[:10],
        "answers": answers
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/analyze-role-results", 
                               json=analysis_data, headers=headers)
        if response.status_code == 200:
            analysis = response.json()["analysis"]
            print("✅ Analysis complete!")
            
            # Display detailed results
            print("\n🎯 Skill Analysis Results")
            print("=" * 50)
            
            print(f"\n📈 Overall Performance:")
            print(f"  • Score: {analysis['overallScore']}%")
            print(f"  • Correct Answers: {analysis['correctAnswers']}/{analysis['totalQuestions']}")
            print(f"  • Readiness Level: {analysis['readiness']}")
            
            print(f"\n🔍 Skill Breakdown:")
            for skill in analysis['skillScores']:
                print(f"  • {skill['skill']}: {skill['score']}% ({skill['level']}) - {skill['correct']}/{skill['total']} correct")
            
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            print(f"\n🚀 Next Steps:")
            for i, step in enumerate(analysis['nextSteps'], 1):
                print(f"  {i}. {step}")
                
        else:
            print(f"❌ Failed to analyze results: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")

if __name__ == "__main__":
    test_role_analysis()
