"""
This module defines the interview questionnaire system, including question categories,
evaluation criteria, and feedback generation functionality.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import random

class QuestionCategory(Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    PROBLEM_SOLVING = "problem_solving"
    LEADERSHIP = "leadership"

@dataclass
class Question:
    text: str
    category: QuestionCategory
    difficulty: int  # 1-5
    expected_keywords: List[str]
    evaluation_criteria: Dict[str, float]  # Criteria and their weights

@dataclass
class EvaluationResult:
    score: float  # 0-100
    feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    keyword_matches: List[str]

class InterviewQuestionnaire:
    def __init__(self):
        self.questions = self._initialize_questions()
        self.evaluation_criteria = self._initialize_evaluation_criteria()
        self.feedback_templates = self._initialize_feedback_templates()

    def _initialize_questions(self) -> Dict[QuestionCategory, List[Question]]:
        """Initialize all interview questions categorized by type."""
        return {
            QuestionCategory.TECHNICAL: [
                Question(
                    text="Explain the concept of dependency injection and its benefits.",
                    category=QuestionCategory.TECHNICAL,
                    difficulty=3,
                    expected_keywords=["loose coupling", "testability", "maintainability", "inversion of control"],
                    evaluation_criteria={"technical_accuracy": 0.4, "clarity": 0.3, "depth": 0.3}
                ),
                Question(
                    text="What are the differences between REST and GraphQL? When would you choose one over the other?",
                    category=QuestionCategory.TECHNICAL,
                    difficulty=4,
                    expected_keywords=["over-fetching", "under-fetching", "flexibility", "caching", "performance"],
                    evaluation_criteria={"technical_accuracy": 0.4, "practical_knowledge": 0.3, "decision_making": 0.3}
                ),
                # Add more technical questions...
            ],
            QuestionCategory.BEHAVIORAL: [
                Question(
                    text="Tell me about a time when you had to handle a difficult team conflict. How did you resolve it?",
                    category=QuestionCategory.BEHAVIORAL,
                    difficulty=3,
                    expected_keywords=["communication", "compromise", "understanding", "resolution"],
                    evaluation_criteria={"situation_handling": 0.4, "communication": 0.3, "outcome": 0.3}
                ),
                Question(
                    text="Describe a situation where you had to make a difficult technical decision. What was your process?",
                    category=QuestionCategory.BEHAVIORAL,
                    difficulty=4,
                    expected_keywords=["analysis", "trade-offs", "decision-making", "impact"],
                    evaluation_criteria={"decision_process": 0.4, "technical_understanding": 0.3, "outcome": 0.3}
                ),
                # Add more behavioral questions...
            ],
            QuestionCategory.SYSTEM_DESIGN: [
                Question(
                    text="Design a scalable notification system that can handle millions of users.",
                    category=QuestionCategory.SYSTEM_DESIGN,
                    difficulty=5,
                    expected_keywords=["message queue", "scalability", "reliability", "latency", "consistency"],
                    evaluation_criteria={"system_understanding": 0.3, "scalability": 0.3, "practicality": 0.4}
                ),
                # Add more system design questions...
            ],
            # Add more categories...
        }

    def _initialize_evaluation_criteria(self) -> Dict[str, Dict[str, float]]:
        """Initialize evaluation criteria and their weights for different question categories."""
        return {
            QuestionCategory.TECHNICAL: {
                "technical_accuracy": 0.4,
                "clarity": 0.3,
                "depth": 0.3
            },
            QuestionCategory.BEHAVIORAL: {
                "situation_handling": 0.4,
                "communication": 0.3,
                "outcome": 0.3
            },
            QuestionCategory.SYSTEM_DESIGN: {
                "system_understanding": 0.3,
                "scalability": 0.3,
                "practicality": 0.4
            }
        }

    def _initialize_feedback_templates(self) -> Dict[str, List[str]]:
        """Initialize templates for generating feedback."""
        return {
            "strengths": [
                "Excellent explanation of {concept}",
                "Strong demonstration of {skill}",
                "Clear and concise communication",
                "Good use of examples to illustrate points"
            ],
            "improvements": [
                "Consider elaborating more on {concept}",
                "Could provide more specific examples",
                "Try to structure your response more clearly",
                "Consider addressing {aspect} in more detail"
            ]
        }

    def get_question(self, category: QuestionCategory, difficulty: Optional[int] = None) -> Question:
        """Get a random question from the specified category and difficulty level."""
        category_questions = self.questions[category]
        if difficulty:
            filtered_questions = [q for q in category_questions if q.difficulty == difficulty]
            if not filtered_questions:
                return random.choice(category_questions)
            return random.choice(filtered_questions)
        return random.choice(category_questions)

    def evaluate_response(self, question: Question, response: str) -> EvaluationResult:
        """Evaluate a candidate's response to a question."""
        # Calculate keyword matches
        keyword_matches = [kw for kw in question.expected_keywords if kw.lower() in response.lower()]
        
        # Calculate base score based on keyword matches
        keyword_score = len(keyword_matches) / len(question.expected_keywords) * 100
        
        # Generate feedback
        strengths = self._generate_strengths(keyword_matches, response)
        improvements = self._generate_improvements(keyword_matches, question.expected_keywords)
        
        # Generate overall feedback
        feedback = self._generate_overall_feedback(strengths, improvements, keyword_score)
        
        return EvaluationResult(
            score=keyword_score,
            feedback=feedback,
            strengths=strengths,
            areas_for_improvement=improvements,
            keyword_matches=keyword_matches
        )

    def _generate_strengths(self, keyword_matches: List[str], response: str) -> List[str]:
        """Generate list of strengths based on response analysis."""
        strengths = []
        if len(keyword_matches) > len(keyword_matches) / 2:
            strengths.append("Good coverage of key concepts")
        if len(response.split()) > 100:
            strengths.append("Detailed and thorough response")
        return strengths

    def _generate_improvements(self, keyword_matches: List[str], expected_keywords: List[str]) -> List[str]:
        """Generate list of areas for improvement based on missing keywords."""
        improvements = []
        missing_keywords = [kw for kw in expected_keywords if kw not in keyword_matches]
        if missing_keywords:
            improvements.append(f"Consider addressing: {', '.join(missing_keywords)}")
        return improvements

    def _generate_overall_feedback(self, strengths: List[str], improvements: List[str], score: float) -> str:
        """Generate overall feedback combining strengths and areas for improvement."""
        feedback = []
        if strengths:
            feedback.append("Strengths:\n" + "\n".join(f"- {s}" for s in strengths))
        if improvements:
            feedback.append("\nAreas for improvement:\n" + "\n".join(f"- {i}" for i in improvements))
        feedback.append(f"\nOverall score: {score:.1f}/100")
        return "\n".join(feedback)
