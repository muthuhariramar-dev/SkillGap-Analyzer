"""
Skill Validation Model - Skill Validation and Verification

This module implements a comprehensive skill validation system that verifies
user-reported skills through various assessment methods, including tests,
projects, peer reviews, and external certifications.
"""

import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import hashlib
import uuid

# ML imports
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationMethod(Enum):
    """Methods for skill validation"""
    ASSESSMENT_TEST = "assessment_test"
    PROJECT_REVIEW = "project_review"
    PEER_REVIEW = "peer_review"
    CERTIFICATION = "certification"
    INTERVIEW = "interview"
    PRACTICAL_DEMO = "practical_demo"


class ValidationStatus(Enum):
    """Validation status levels"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class SkillClaim:
    """Represents a user's skill claim"""
    user_id: str
    skill_name: str
    claimed_level: int
    claimed_experience: int
    evidence_urls: List[str]
    submission_date: datetime
    validation_status: ValidationStatus = ValidationStatus.PENDING


@dataclass
class ValidationResult:
    """Result of skill validation"""
    claim_id: str
    validated_level: int
    confidence_score: float
    validation_method: ValidationMethod
    validator_id: str
    validation_date: datetime
    feedback: str
    evidence_reviewed: List[str]


@dataclass
class ValidationTest:
    """Represents a validation test for a skill"""
    test_id: str
    skill_name: str
    difficulty_level: int
    questions: List[Dict]
    passing_score: float
    time_limit_minutes: int
    is_active: bool


class SkillValidator:
    """
    Skill Validation System
    
    This class implements various methods to validate user skill claims through
    automated tests, peer reviews, and external verification.
    """
    
    def __init__(self):
        """Initialize the skill validation system"""
        self.logger = logging.getLogger(__name__)
        
        # ML models
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.level_predictor = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Data storage
        self.skill_claims = {}
        self.validation_results = {}
        self.validation_tests = {}
        self.validators = {}
        
        # Configuration
        self.validation_thresholds = {
            "minimum_confidence": 0.7,
            "evidence_requirements": {
                "beginner": 1,
                "intermediate": 2,
                "advanced": 3,
                "expert": 4
            }
        }
        
        self._initialize_validation_tests()
    
    def _initialize_validation_tests(self):
        """Initialize predefined validation tests for common skills"""
        tests = [
            ValidationTest(
                test_id="python_basics",
                skill_name="Python",
                difficulty_level=2,
                questions=[
                    {
                        "question": "What is the output of print(2 ** 3)?",
                        "options": ["6", "8", "9", "12"],
                        "correct_answer": "8",
                        "points": 1
                    },
                    {
                        "question": "Which method is used to add an item to a list?",
                        "options": ["append()", "add()", "insert()", "push()"],
                        "correct_answer": "append()",
                        "points": 1
                    }
                ],
                passing_score=0.8,
                time_limit_minutes=30,
                is_active=True
            ),
            ValidationTest(
                test_id="sql_intermediate",
                skill_name="SQL",
                difficulty_level=3,
                questions=[
                    {
                        "question": "Which JOIN returns all records from the left table?",
                        "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"],
                        "correct_answer": "LEFT JOIN",
                        "points": 1
                    }
                ],
                passing_score=0.75,
                time_limit_minutes=45,
                is_active=True
            )
        ]
        
        self.validation_tests = {test.test_id: test for test in tests}
    
    def submit_skill_claim(self, user_id: str, skill_name: str, claimed_level: int,
                          claimed_experience: int, evidence_urls: List[str]) -> str:
        """
        Submit a new skill claim for validation
        
        Args:
            user_id: User identifier
            skill_name: Name of the skill
            claimed_level: Claimed proficiency level (1-5)
            claimed_experience: Years of experience claimed
            evidence_urls: URLs to supporting evidence
            
        Returns:
            Claim ID for tracking
        """
        try:
            claim_id = str(uuid.uuid4())
            
            # Validate input
            if not (1 <= claimed_level <= 5):
                raise ValueError("Skill level must be between 1 and 5")
            
            if claimed_experience < 0:
                raise ValueError("Experience cannot be negative")
            
            # Check evidence requirements
            required_evidence = self.validation_thresholds["evidence_requirements"].get(
                self._get_level_category(claimed_level), 1
            )
            
            if len(evidence_urls) < required_evidence:
                self.logger.warning(f"Insufficient evidence for level {claimed_level}")
            
            # Create skill claim
            claim = SkillClaim(
                user_id=user_id,
                skill_name=skill_name,
                claimed_level=claimed_level,
                claimed_experience=claimed_experience,
                evidence_urls=evidence_urls,
                submission_date=datetime.now()
            )
            
            self.skill_claims[claim_id] = claim
            
            # Start validation process
            self._initiate_validation_process(claim_id)
            
            self.logger.info(f"Skill claim submitted: {claim_id}")
            return claim_id
            
        except Exception as e:
            self.logger.error(f"Error submitting skill claim: {e}")
            raise
    
    def _get_level_category(self, level: int) -> str:
        """Get category name for skill level"""
        if level <= 2:
            return "beginner"
        elif level <= 3:
            return "intermediate"
        elif level <= 4:
            return "advanced"
        else:
            return "expert"
    
    def _initiate_validation_process(self, claim_id: str):
        """Initiate the validation process for a skill claim"""
        try:
            claim = self.skill_claims.get(claim_id)
            if not claim:
                return
            
            # Update status
            claim.validation_status = ValidationStatus.IN_PROGRESS
            
            # Determine validation methods based on skill level
            validation_methods = self._determine_validation_methods(claim)
            
            # Schedule validations
            for method in validation_methods:
                self._schedule_validation(claim_id, method)
            
        except Exception as e:
            self.logger.error(f"Error initiating validation process: {e}")
    
    def _determine_validation_methods(self, claim: SkillClaim) -> List[ValidationMethod]:
        """Determine appropriate validation methods based on claim"""
        methods = []
        
        level_category = self._get_level_category(claim.claimed_level)
        
        # Base validation for all levels
        methods.append(ValidationMethod.ASSESSMENT_TEST)
        
        # Additional methods based on level
        if claim.claimed_level >= 3:
            methods.append(ValidationMethod.PROJECT_REVIEW)
        
        if claim.claimed_level >= 4:
            methods.append(ValidationMethod.PEER_REVIEW)
        
        if claim.claimed_level >= 5:
            methods.append(ValidationMethod.CERTIFICATION)
            methods.append(ValidationMethod.INTERVIEW)
        
        return methods
    
    def _schedule_validation(self, claim_id: str, method: ValidationMethod):
        """Schedule a specific validation method"""
        try:
            if method == ValidationMethod.ASSESSMENT_TEST:
                self._schedule_assessment_test(claim_id)
            elif method == ValidationMethod.PROJECT_REVIEW:
                self._schedule_project_review(claim_id)
            elif method == ValidationMethod.PEER_REVIEW:
                self._schedule_peer_review(claim_id)
            # Add other methods as needed
            
        except Exception as e:
            self.logger.error(f"Error scheduling validation: {e}")
    
    def _schedule_assessment_test(self, claim_id: str):
        """Schedule an assessment test for the claim"""
        try:
            claim = self.skill_claims[claim_id]
            
            # Find appropriate test
            suitable_test = None
            for test in self.validation_tests.values():
                if (test.skill_name.lower() == claim.skill_name.lower() and 
                    test.is_active and
                    abs(test.difficulty_level - claim.claimed_level) <= 1):
                    suitable_test = test
                    break
            
            if suitable_test:
                self.logger.info(f"Scheduled assessment test {suitable_test.test_id} for claim {claim_id}")
            else:
                self.logger.warning(f"No suitable test found for {claim.skill_name} at level {claim.claimed_level}")
                
        except Exception as e:
            self.logger.error(f"Error scheduling assessment test: {e}")
    
    def _schedule_project_review(self, claim_id: str):
        """Schedule a project review for the claim"""
        try:
            claim = self.skill_claims[claim_id]
            
            # Check if project evidence is provided
            project_urls = [url for url in claim.evidence_urls if 'github' in url or 'portfolio' in url]
            
            if project_urls:
                self.logger.info(f"Scheduled project review for claim {claim_id}")
            else:
                self.logger.warning(f"No project evidence found for claim {claim_id}")
                
        except Exception as e:
            self.logger.error(f"Error scheduling project review: {e}")
    
    def _schedule_peer_review(self, claim_id: str):
        """Schedule peer review for the claim"""
        try:
            # Find qualified peer reviewers
            qualified_reviewers = self._find_qualified_reviewers(claim_id)
            
            if qualified_reviewers:
                self.logger.info(f"Scheduled peer review for claim {claim_id} with {len(qualified_reviewers)} reviewers")
            else:
                self.logger.warning(f"No qualified reviewers found for claim {claim_id}")
                
        except Exception as e:
            self.logger.error(f"Error scheduling peer review: {e}")
    
    def _find_qualified_reviewers(self, claim_id: str) -> List[str]:
        """Find qualified peer reviewers for a skill claim"""
        try:
            claim = self.skill_claims[claim_id]
            
            # In a real system, this would query a database of qualified reviewers
            # For now, return mock reviewer IDs
            qualified_reviewers = [
                f"reviewer_{i}" for i in range(3)
            ]
            
            return qualified_reviewers
            
        except Exception as e:
            self.logger.error(f"Error finding qualified reviewers: {e}")
            return []
    
    def validate_assessment_test(self, claim_id: str, test_id: str, 
                               answers: List[str]) -> ValidationResult:
        """
        Validate assessment test results
        
        Args:
            claim_id: Skill claim ID
            test_id: Test ID
            answers: User's answers
            
        Returns:
            ValidationResult object
        """
        try:
            test = self.validation_tests.get(test_id)
            if not test:
                raise ValueError(f"Test {test_id} not found")
            
            claim = self.skill_claims.get(claim_id)
            if not claim:
                raise ValueError(f"Claim {claim_id} not found")
            
            # Calculate score
            correct_answers = 0
            total_points = 0
            
            for i, question in enumerate(test.questions):
                if i < len(answers):
                    total_points += question["points"]
                    if answers[i] == question["correct_answer"]:
                        correct_answers += question["points"]
            
            score = correct_answers / total_points if total_points > 0 else 0
            
            # Determine validation result
            passed = score >= test.passing_score
            
            # Calculate validated level based on performance
            if score >= 0.9:
                validated_level = test.difficulty_level + 1
            elif score >= 0.7:
                validated_level = test.difficulty_level
            else:
                validated_level = max(1, test.difficulty_level - 1)
            
            # Create validation result
            result = ValidationResult(
                claim_id=claim_id,
                validated_level=validated_level,
                confidence_score=score,
                validation_method=ValidationMethod.ASSESSMENT_TEST,
                validator_id="system_auto",
                validation_date=datetime.now(),
                feedback=f"Test score: {score:.2f}. {'Passed' if passed else 'Failed'}",
                evidence_reviewed=[test_id]
            )
            
            self.validation_results[f"{claim_id}_{test_id}"] = result
            
            # Update claim status if this is the primary validation
            if passed:
                self._update_claim_validation_status(claim_id, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating assessment test: {e}")
            raise
    
    def _update_claim_validation_status(self, claim_id: str, result: ValidationResult):
        """Update the validation status of a skill claim"""
        try:
            claim = self.skill_claims.get(claim_id)
            if not claim:
                return
            
            # Check if confidence meets threshold
            if result.confidence_score >= self.validation_thresholds["minimum_confidence"]:
                claim.validation_status = ValidationStatus.VALIDATED
                self.logger.info(f"Claim {claim_id} validated with level {result.validated_level}")
            else:
                self.logger.info(f"Claim {claim_id} validation pending additional evidence")
                
        except Exception as e:
            self.logger.error(f"Error updating claim validation status: {e}")
    
    def detect_anomalous_claims(self) -> List[str]:
        """
        Detect potentially fraudulent skill claims using anomaly detection
        
        Returns:
            List of suspicious claim IDs
        """
        try:
            if len(self.skill_claims) < 10:
                return []
            
            # Prepare features for anomaly detection
            features = []
            claim_ids = []
            
            for claim_id, claim in self.skill_claims.items():
                feature_vector = [
                    claim.claimed_level,
                    claim.claimed_experience,
                    len(claim.evidence_urls),
                    claim.submission_date.timestamp()
                ]
                features.append(feature_vector)
                claim_ids.append(claim_id)
            
            # Detect anomalies
            features_array = np.array(features)
            anomalies = self.anomaly_detector.fit_predict(features_array)
            
            # Return anomalous claim IDs
            suspicious_claims = [
                claim_ids[i] for i, anomaly in enumerate(anomalies) 
                if anomaly == -1
            ]
            
            self.logger.info(f"Detected {len(suspicious_claims)} anomalous claims")
            return suspicious_claims
            
        except Exception as e:
            self.logger.error(f"Error detecting anomalous claims: {e}")
            return []
    
    def get_validation_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of validation results for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with validation summary
        """
        try:
            user_claims = [
                claim for claim in self.skill_claims.values()
                if claim.user_id == user_id
            ]
            
            user_results = [
                result for result in self.validation_results.values()
                if any(claim_id.startswith(result.claim_id) for claim_id in self.skill_claims
                      if self.skill_claims[claim_id].user_id == user_id)
            ]
            
            summary = {
                "user_id": user_id,
                "total_claims": len(user_claims),
                "validated_skills": 0,
                "pending_validations": 0,
                "rejected_claims": 0,
                "skills_by_level": {},
                "validation_methods_used": set(),
                "average_confidence": 0.0
            }
            
            confidence_scores = []
            
            for claim in user_claims:
                if claim.validation_status == ValidationStatus.VALIDATED:
                    summary["validated_skills"] += 1
                elif claim.validation_status == ValidationStatus.PENDING:
                    summary["pending_validations"] += 1
                elif claim.validation_status == ValidationStatus.REJECTED:
                    summary["rejected_claims"] += 1
                
                level_category = self._get_level_category(claim.claimed_level)
                summary["skills_by_level"][level_category] = summary["skills_by_level"].get(level_category, 0) + 1
            
            for result in user_results:
                summary["validation_methods_used"].add(result.validation_method.value)
                confidence_scores.append(result.confidence_score)
            
            if confidence_scores:
                summary["average_confidence"] = np.mean(confidence_scores)
            
            summary["validation_methods_used"] = list(summary["validation_methods_used"])
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting validation summary: {e}")
            return {}
    
    def verify_external_certification(self, claim_id: str, certification_url: str,
                                    issuing_body: str) -> ValidationResult:
        """
        Verify external certification
        
        Args:
            claim_id: Skill claim ID
            certification_url: URL to certification verification
            issuing_body: Organization that issued the certification
            
        Returns:
            ValidationResult object
        """
        try:
            claim = self.skill_claims.get(claim_id)
            if not claim:
                raise ValueError(f"Claim {claim_id} not found")
            
            # In a real implementation, this would verify with the issuing body
            # For now, simulate verification
            is_valid = self._simulate_certification_verification(certification_url, issuing_body)
            
            if is_valid:
                validated_level = min(5, claim.claimed_level + 1)
                confidence = 0.9
                feedback = f"Certification verified from {issuing_body}"
            else:
                validated_level = claim.claimed_level
                confidence = 0.3
                feedback = "Certification could not be verified"
            
            result = ValidationResult(
                claim_id=claim_id,
                validated_level=validated_level,
                confidence_score=confidence,
                validation_method=ValidationMethod.CERTIFICATION,
                validator_id="external_verification",
                validation_date=datetime.now(),
                feedback=feedback,
                evidence_reviewed=[certification_url]
            )
            
            self.validation_results[f"{claim_id}_cert"] = result
            
            if is_valid:
                self._update_claim_validation_status(claim_id, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error verifying external certification: {e}")
            raise
    
    def _simulate_certification_verification(self, url: str, issuing_body: str) -> bool:
        """Simulate external certification verification"""
        # In real implementation, this would make API calls to verify
        # For simulation, return True for known issuers
        known_issuers = ["coursera", "udemy", "edx", "aws", "microsoft", "google"]
        return any(issuer in issuing_body.lower() for issuer in known_issuers)
    
    def generate_validation_report(self, claim_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive validation report for a skill claim
        
        Args:
            claim_id: Skill claim ID
            
        Returns:
            Dictionary with validation report
        """
        try:
            claim = self.skill_claims.get(claim_id)
            if not claim:
                raise ValueError(f"Claim {claim_id} not found")
            
            # Get all validation results for this claim
            claim_results = [
                result for result in self.validation_results.values()
                if result.claim_id == claim_id or result.claim_id.startswith(claim_id)
            ]
            
            report = {
                "claim_id": claim_id,
                "user_id": claim.user_id,
                "skill_name": claim.skill_name,
                "claimed_level": claim.claimed_level,
                "claimed_experience": claim.claimed_experience,
                "submission_date": claim.submission_date.isoformat(),
                "current_status": claim.validation_status.value,
                "validation_results": [],
                "overall_confidence": 0.0,
                "final_validated_level": claim.claimed_level,
                "recommendations": []
            }
            
            if claim_results:
                confidence_scores = [result.confidence_score for result in claim_results]
                report["overall_confidence"] = np.mean(confidence_scores)
                
                # Determine final validated level
                validated_levels = [result.validated_level for result in claim_results]
                if validated_levels:
                    report["final_validated_level"] = int(np.mean(validated_levels))
                
                # Add validation details
                for result in claim_results:
                    report["validation_results"].append({
                        "method": result.validation_method.value,
                        "validated_level": result.validated_level,
                        "confidence": result.confidence_score,
                        "date": result.validation_date.isoformat(),
                        "feedback": result.feedback
                    })
            
            # Generate recommendations
            report["recommendations"] = self._generate_validation_recommendations(claim, claim_results)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating validation report: {e}")
            return {}
    
    def _generate_validation_recommendations(self, claim: SkillClaim, 
                                           results: List[ValidationResult]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if not results:
            recommendations.append("Complete the required assessment tests to validate your skills")
            return recommendations
        
        avg_confidence = np.mean([r.confidence_score for r in results])
        
        if avg_confidence < 0.5:
            recommendations.append("Consider additional training or practice to improve skill validation")
        
        if claim.claimed_level > 3 and len(results) < 2:
            recommendations.append("Advanced skills require multiple validation methods")
        
        if len(claim.evidence_urls) < 2:
            recommendations.append("Add more evidence (projects, certifications) to strengthen your claim")
        
        if not recommendations:
            recommendations.append("Your skill claim has been successfully validated")
        
        return recommendations


# Example usage and testing
if __name__ == "__main__":
    # Initialize the skill validation system
    validator = SkillValidator()
    
    print("=== Skill Validation System ===\n")
    
    # 1. Submit a skill claim
    print("1. Submitting Skill Claim:")
    user_id = "user_123"
    skill_name = "Python"
    claimed_level = 3
    claimed_experience = 2
    evidence_urls = [
        "https://github.com/user/python-projects",
        "https://portfolio.example.com/python-work"
    ]
    
    claim_id = validator.submit_skill_claim(
        user_id, skill_name, claimed_level, claimed_experience, evidence_urls
    )
    print(f"   Claim submitted with ID: {claim_id}")
    print()
    
    # 2. Take an assessment test
    print("2. Taking Assessment Test:")
    test_id = "python_basics"
    answers = ["8", "append()"]  # Correct answers
    
    test_result = validator.validate_assessment_test(claim_id, test_id, answers)
    print(f"   Test Result: {test_result.feedback}")
    print(f"   Validated Level: {test_result.validated_level}")
    print(f"   Confidence Score: {test_result.confidence_score:.2f}")
    print()
    
    # 3. Verify external certification
    print("3. Verifying External Certification:")
    cert_url = "https://coursera.org/verify/python-certificate"
    issuing_body = "Coursera"
    
    cert_result = validator.verify_external_certification(claim_id, cert_url, issuing_body)
    print(f"   Certification Result: {cert_result.feedback}")
    print(f"   Updated Validated Level: {cert_result.validated_level}")
    print()
    
    # 4. Get validation summary
    print("4. User Validation Summary:")
    summary = validator.get_validation_summary(user_id)
    print(f"   Total Claims: {summary.get('total_claims', 0)}")
    print(f"   Validated Skills: {summary.get('validated_skills', 0)}")
    print(f"   Average Confidence: {summary.get('average_confidence', 0):.2f}")
    print()
    
    # 5. Generate validation report
    print("5. Generating Validation Report:")
    report = validator.generate_validation_report(claim_id)
    print(f"   Overall Confidence: {report.get('overall_confidence', 0):.2f}")
    print(f"   Final Validated Level: {report.get('final_validated_level', 0)}")
    print(f"   Current Status: {report.get('current_status', 'unknown')}")
    print("   Recommendations:")
    for rec in report.get('recommendations', []):
        print(f"     - {rec}")
    print()
    
    # 6. Detect anomalous claims
    print("6. Anomaly Detection:")
    suspicious_claims = validator.detect_anomalous_claims()
    print(f"   Suspicious claims detected: {len(suspicious_claims)}")
    
    print("\n=== Validation Complete ===")
