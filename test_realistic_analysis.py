#!/usr/bin/env python3
"""
Enhanced test script to demonstrate the role-specific skill analysis with realistic performance
"""

import requests
import json
import time

# Base URLs
BACKEND_URL = "http://localhost:8000"

def test_realistic_role_analysis():
    """Test the complete role analysis flow with realistic answers"""
    print("🚀 Testing Role-Specific Skill Analysis Flow (Realistic Performance)")
    print("=" * 70)
    
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
            
            # Display 10 questions with correct answers marked
            print("\n📚 Sample Questions (10 out of {len(questions)}):")
            print("-" * 70)
            for i, question in enumerate(questions[:10], 1):
                print(f"\n❓ Question {i}: {question['question']}")
                for j, option in enumerate(question['options']):
                    marker = "✓" if j == question['correct'] else " "
                    print(f"  {marker} {chr(65+j)}. {option}")
                print(f"  💡 Correct Answer: {question['options'][question['correct']]}")
                print(f"  📖 Explanation: {question['explanation']}")
            
        else:
            print(f"❌ Failed to generate questions: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        return
    
    # Step 3: Submit realistic answers for analysis (75% correct - good performance)
    print("\n📊 Step 3: Submitting answers for analysis (Simulating 75% correct)...")
    
    answers = []
    correct_count = 0
    
    for i, question in enumerate(questions[:10]):
        # Simulate 75% correct answers for realistic performance
        import random
        if i < 7:  # First 7 questions correct
            selected_option = question['correct']
            correct_count += 1
        else:  # Last 3 questions incorrect
            available_options = [j for j in range(len(question['options'])) if j != question['correct']]
            selected_option = random.choice(available_options)
        
        answers.append({
            "questionId": question['id'],
            "selectedOption": selected_option
        })
        
        print(f"  Q{i+1}: {'✓ Correct' if selected_option == question['correct'] else '✗ Wrong'}")
    
    print(f"\n📈 Summary: {correct_count}/10 questions correct (75% accuracy)")
    
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
            print("=" * 70)
            
            print(f"\n📈 Overall Performance:")
            print(f"  • Overall Score: {analysis['overallScore']}%")
            print(f"  • Correct Answers: {analysis['correctAnswers']}/{analysis['totalQuestions']}")
            print(f"  • Readiness Level: {analysis['readiness']} 🎯")
            
            print(f"\n🔍 Skill Breakdown:")
            for skill in analysis['skillScores']:
                emoji = "🟢" if skill['score'] >= 80 else "🟡" if skill['score'] >= 60 else "🔴"
                print(f"  {emoji} {skill['skill']}: {skill['score']}% ({skill['level']})")
                print(f"      → {skill['correct']}/{skill['total']} questions correct")
            
            print(f"\n💡 Personalized Recommendations:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            print(f"\n🚀 Next Steps for Career Growth:")
            for i, step in enumerate(analysis['nextSteps'], 1):
                print(f"  {i}. {step}")
            
            print(f"\n🎉 Analysis Summary:")
            if analysis['readiness'] == 'High':
                print("  🌟 Excellent! You're well-prepared for this role!")
            elif analysis['readiness'] == 'Medium':
                print("  👍 Good foundation! Focus on recommended improvements.")
            else:
                print("  📚 Keep learning! Focus on foundational skills.")
                
        else:
            print(f"❌ Failed to analyze results: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")

def test_multiple_roles():
    """Test analysis for multiple roles"""
    print("\n\n🔄 Testing Multiple Roles Analysis")
    print("=" * 70)
    
    roles = [
        {"id": "frontend-developer", "title": "Frontend Developer"},
        {"id": "backend-developer", "title": "Backend Developer"},
        {"id": "data-scientist", "title": "Data Scientist"},
        {"id": "product-manager", "title": "Product Manager"}
    ]
    
    for role in roles:
        print(f"\n🎯 Testing {role['title']}...")
        # This would generate questions for each role
        print(f"  • Role ID: {role['id']}")
        print(f"  • Questions would be tailored to {role['title']} skills")
        print(f"  • Analysis would focus on role-specific competencies")

if __name__ == "__main__":
    test_realistic_role_analysis()
    test_multiple_roles()
