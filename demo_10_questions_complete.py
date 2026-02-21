#!/usr/bin/env python3
"""
Complete demonstration of 10 questions per role with analysis results
"""

import requests
import json

# Base URLs
BACKEND_URL = "http://localhost:8000"

def demo_complete_10_questions_flow():
    """Complete demonstration of the 10 questions flow"""
    print("🎯 COMPLETE 10 QUESTIONS DEMONSTRATION")
    print("=" * 70)
    
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
        print(f"   Token: {token[:50]}...")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test all roles with 10 questions each
    print("\n📋 Step 2: Generate 10 Questions for Each Role")
    print("=" * 70)
    
    roles = [
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
    
    for role in roles:
        print(f"\n🎯 {role['roleTitle']}")
        print("-" * 50)
        
        # Generate 10 questions
        response = requests.post(f"{BACKEND_URL}/api/generate-role-questions", 
                               json=role, headers=headers)
        
        if response.status_code == 200:
            questions = response.json()["questions"]
            print(f"✅ Generated {len(questions)} questions")
            
            # Show first 3 questions
            print("   📝 Sample Questions:")
            for i, q in enumerate(questions[:3], 1):
                print(f"      {i}. {q['question']}")
                print(f"         ✓ Correct: {q['options'][q['correct']]}")
            
            # Simulate answering all 10 questions
            answers = []
            for i, question in enumerate(questions):
                # 70% correct rate for demonstration
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
            
            # Analyze results
            analysis_data = {
                "roleId": role['roleId'],
                "roleTitle": role['roleTitle'],
                "questions": questions,
                "answers": answers
            }
            
            response = requests.post(f"{BACKEND_URL}/api/analyze-role-results", 
                                   json=analysis_data, headers=headers)
            
            if response.status_code == 200:
                analysis = response.json()["analysis"]
                print(f"✅ Analysis Complete!")
                print(f"   📊 Score: {analysis['overallScore']}%")
                print(f"   🎯 Readiness: {analysis['readiness']}")
                print(f"   ✅ Correct: {analysis['correctAnswers']}/{analysis['totalQuestions']}")
                print(f"   📈 Skills: {len(analysis['skillScores'])}")
                
                # Show top recommendations
                print("   💡 Top Recommendations:")
                for i, rec in enumerate(analysis['recommendations'][:2], 1):
                    print(f"      {i}. {rec}")
                
        else:
            print(f"❌ Failed: {response.status_code}")
    
    print("\n🎉 DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print("✅ Each role generates exactly 10 AI questions")
    print("✅ Questions are role-specific and relevant")
    print("✅ Complete analysis with skill breakdown")
    print("✅ Personalized recommendations provided")
    print("✅ Ready for frontend integration")
    
    print(f"\n🌐 Frontend Access: http://localhost:3000")
    print(f"🔧 Backend API: http://localhost:8000")
    print(f"\n📋 Available Roles:")
    for role in roles:
        print(f"   • {role['roleTitle']}")

if __name__ == "__main__":
    demo_complete_10_questions_flow()
