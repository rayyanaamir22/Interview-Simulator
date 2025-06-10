"""
This module contains the InterviewConversationManager class, which is responsible for managing the conversation during the interview.
It includes the following classes:
- ConversationManager: Base class for conversation management
- InterviewContext: Class for managing interview context
- InterviewConversationManager: Class for managing the conversation during the interview
"""

# frameworks
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class QuestionCategory(Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    GENERAL = "general"

@dataclass
class Question:
    id: str
    text: str
    category: QuestionCategory
    difficulty: int = 1
    keywords: List[str] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

class InterviewState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class InterviewContext:
    interview_id: str
    state: InterviewState
    current_question_index: int
    responses: Dict[str, Any]
    metadata: Dict[str, Any]
    implicit_thoughts: List[str] = None

    def __post_init__(self):
        if self.implicit_thoughts is None:
            self.implicit_thoughts = []

@dataclass
class ChecklistItem:
    """Represents a single item in the interview checklist."""
    id: str
    description: str
    category: str  # e.g., "technical", "behavioral", "communication"
    is_completed: bool = False
    notes: str = ""
    priority: int = 1  # 1-5, where 5 is highest priority

    def complete(self, notes: str = "") -> None:
        """Mark the item as completed with optional notes."""
        self.is_completed = True
        self.notes = notes

    def reset(self) -> None:
        """Reset the item to incomplete state."""
        self.is_completed = False
        self.notes = ""

class ConversationManager:
    """Base class for conversation management."""
    
    async def generate_response(self, context: InterviewContext, user_input: str) -> str:
        """Generate a response based on the context and user input."""
        raise NotImplementedError
    
    async def evaluate_response(self, context: InterviewContext, user_input: str) -> Dict[str, Any]:
        """Evaluate a user's response."""
        raise NotImplementedError
    
    async def update_state(self, interview_id: str, user_input: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
        """Update the conversation state."""
        raise NotImplementedError
    
    async def get_response(self, interview_id: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get the next response based on current state."""
        raise NotImplementedError
    
    async def get_interview_status(self, interview_id: str) -> Dict[str, Any]:
        """Get the current status of an interview."""
        raise NotImplementedError
    
    async def reset_interview(self, interview_id: str) -> Dict[str, Any]:
        """Reset an interview to its initial state."""
        raise NotImplementedError

class InterviewQuestionnaire:
    """Class for managing interview questions and evaluations."""
    
    def __init__(self):
        self.questions = {
            QuestionCategory.TECHNICAL: [
                Question(
                    id="tech_1",
                    text="Tell me about your experience with Python.",
                    category=QuestionCategory.TECHNICAL,
                    difficulty=1,
                    keywords=["python", "programming", "experience"]
                ),
                Question(
                    id="tech_2",
                    text="How do you handle error handling in your code?",
                    category=QuestionCategory.TECHNICAL,
                    difficulty=2,
                    keywords=["error handling", "exceptions", "debugging"]
                )
            ],
            QuestionCategory.BEHAVIORAL: [
                Question(
                    id="beh_1",
                    text="Tell me about a challenging project you worked on.",
                    category=QuestionCategory.BEHAVIORAL,
                    difficulty=1,
                    keywords=["challenge", "project", "experience"]
                ),
                Question(
                    id="beh_2",
                    text="How do you handle conflicts in a team?",
                    category=QuestionCategory.BEHAVIORAL,
                    difficulty=2,
                    keywords=["conflict", "team", "communication"]
                )
            ]
        }
    
    def get_question(self, category: QuestionCategory, difficulty: int = 1) -> Question:
        """Get a question based on category and difficulty."""
        available_questions = [
            q for q in self.questions[category]
            if q.difficulty == difficulty
        ]
        if not available_questions:
            # Fallback to any question in the category
            available_questions = self.questions[category]
        return available_questions[0]  # For now, just return the first available question
    
    def evaluate_response(self, question: Question, response: str) -> Dict[str, Any]:
        """Evaluate a response to a question."""
        # Simple keyword matching for now
        matched_keywords = [
            keyword for keyword in question.keywords
            if keyword.lower() in response.lower()
        ]
        
        score = len(matched_keywords) / len(question.keywords) if question.keywords else 0.5
        
        return {
            "score": score,
            "matched_keywords": matched_keywords,
            "feedback": f"Matched {len(matched_keywords)} out of {len(question.keywords)} keywords."
        }

@dataclass
class InterviewMetrics:
    """Stores metrics about the interview performance."""
    technical_score: float = 0.0
    behavioral_score: float = 0.0
    communication_score: float = 0.0
    time_per_question: Dict[str, float] = None
    total_duration: float = 0.0
    questions_attempted: int = 0
    questions_completed: int = 0

    def __post_init__(self):
        if self.time_per_question is None:
            self.time_per_question = {}

class InterviewSummarizer:
    """Generates comprehensive summaries of interview performance and outcomes."""
    
    def __init__(self):
        self.metrics = InterviewMetrics()
        self.feedback_points = []
        self.strengths = []
        self.areas_for_improvement = []
        self.question_analysis = {}
    
    def update_metrics(self, question: Question, response: str, time_spent: float) -> None:
        """Update metrics based on a question response."""
        self.metrics.questions_attempted += 1
        self.metrics.time_per_question[question.id] = time_spent
        self.metrics.total_duration += time_spent
        
        # Evaluate response and update scores
        evaluation = self._evaluate_response(question, response)
        if question.category == QuestionCategory.TECHNICAL:
            self.metrics.technical_score = (self.metrics.technical_score * (self.metrics.questions_attempted - 1) + 
                                          evaluation["score"]) / self.metrics.questions_attempted
        elif question.category == QuestionCategory.BEHAVIORAL:
            self.metrics.behavioral_score = (self.metrics.behavioral_score * (self.metrics.questions_attempted - 1) + 
                                           evaluation["score"]) / self.metrics.questions_attempted
        
        # Update communication score based on response length and clarity
        self.metrics.communication_score = (self.metrics.communication_score * (self.metrics.questions_attempted - 1) + 
                                          self._evaluate_communication(response)) / self.metrics.questions_attempted
        
        # Store question analysis
        self.question_analysis[question.id] = {
            "response": response,
            "evaluation": evaluation,
            "time_spent": time_spent
        }
    
    def _evaluate_response(self, question: Question, response: str) -> Dict[str, Any]:
        """Evaluate a response to a question."""
        # This would be enhanced with more sophisticated evaluation
        matched_keywords = [
            keyword for keyword in question.keywords
            if keyword.lower() in response.lower()
        ]
        
        score = len(matched_keywords) / len(question.keywords) if question.keywords else 0.5
        
        return {
            "score": score,
            "matched_keywords": matched_keywords,
            "feedback": f"Matched {len(matched_keywords)} out of {len(question.keywords)} keywords."
        }
    
    def _evaluate_communication(self, response: str) -> float:
        """Evaluate the communication quality of a response."""
        # Simple evaluation based on response length and structure
        words = response.split()
        if not words:
            return 0.0
        
        # Basic scoring based on response length and structure
        length_score = min(len(words) / 50, 1.0)  # Normalize to 0-1, assuming 50 words is ideal
        structure_score = 1.0 if len(words) > 10 else 0.5  # Simple structure check
        
        return (length_score + structure_score) / 2
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the interview."""
        self._analyze_performance()
        
        return {
            "metrics": {
                "technical_score": self.metrics.technical_score,
                "behavioral_score": self.metrics.behavioral_score,
                "communication_score": self.metrics.communication_score,
                "total_duration": self.metrics.total_duration,
                "questions_attempted": self.metrics.questions_attempted,
                "questions_completed": self.metrics.questions_completed
            },
            "strengths": self.strengths,
            "areas_for_improvement": self.areas_for_improvement,
            "feedback_points": self.feedback_points,
            "question_analysis": self.question_analysis
        }
    
    def _analyze_performance(self) -> None:
        """Analyze overall performance and generate insights."""
        # Analyze strengths
        if self.metrics.technical_score > 0.7:
            self.strengths.append("Strong technical knowledge")
        if self.metrics.behavioral_score > 0.7:
            self.strengths.append("Good behavioral response quality")
        if self.metrics.communication_score > 0.7:
            self.strengths.append("Clear and effective communication")
        
        # Analyze areas for improvement
        if self.metrics.technical_score < 0.5:
            self.areas_for_improvement.append("Technical knowledge needs improvement")
        if self.metrics.behavioral_score < 0.5:
            self.areas_for_improvement.append("Behavioral response quality could be enhanced")
        if self.metrics.communication_score < 0.5:
            self.areas_for_improvement.append("Communication skills need development")
        
        # Generate specific feedback points
        for question_id, analysis in self.question_analysis.items():
            if analysis["evaluation"]["score"] < 0.5:
                self.feedback_points.append(
                    f"Question {question_id}: Consider providing more detailed responses"
                )

class InterviewConversationManager(ConversationManager):
    def __init__(
        self,
        model_name: str = "microsoft/DialoGPT-medium",  # TODO: find a better default LOL
        max_length: int = 1000,
        temperature: float = 0.7
    ):
        """Initialize the conversation manager with a pre-trained model."""
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.max_length = max_length
        self.temperature = temperature
        
        # Store conversation history for each interview
        self.conversation_history: Dict[str, List[str]] = {}
        
        # Initialize questionnaire system
        self.questionnaire = InterviewQuestionnaire()
        
        # Store current questions for each interview
        self.current_questions: Dict[str, Question] = {}

        self.interviews: Dict[str, InterviewContext] = {}

    async def generate_response(
        self,
        context: InterviewContext,
        user_input: str
    ) -> str:
        """Generate AI response based on context and user input."""
        # Initialize conversation history if not exists
        if context.interview_id not in self.conversation_history:
            self.conversation_history[context.interview_id] = []
            # Get first question based on interview type
            interview_type = context.metadata.get("type", "technical")
            category = QuestionCategory.TECHNICAL if interview_type == "technical" else QuestionCategory.BEHAVIORAL
            self.current_questions[context.interview_id] = self.questionnaire.get_question(category)
        
        # Add user input to history
        self.conversation_history[context.interview_id].append(f"User: {user_input}")
        
        # Evaluate the response
        evaluation = await self.evaluate_response(context, user_input)
        
        # Get next question
        next_question = self._get_next_question(context)
        self.current_questions[context.interview_id] = next_question
        
        # Prepare response with evaluation feedback and next question
        response = f"{evaluation['feedback']}\n\nNext question: {next_question.text}"
        
        # Add response to history
        self.conversation_history[context.interview_id].append(f"Assistant: {response}")
        
        return response

    async def evaluate_response(
        self,
        context: InterviewContext,
        user_input: str
    ) -> Dict[str, Any]:
        """Evaluate a user's response."""
        # For now, return a simple evaluation
        return {
            "feedback": "Thank you for your response.",
            "score": 0.5,  # Placeholder score
            "suggestions": []  # Placeholder suggestions
        }

    def _get_next_question(self, context: InterviewContext) -> Question:
        """Get the next question based on the current context."""
        # For now, return a placeholder question
        return Question(
            id="placeholder",
            text="Tell me about your experience.",
            category=QuestionCategory.TECHNICAL
        )

    async def update_state(
        self,
        interview_id: str,
        user_input: str,
        sentiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update the conversation state based on user input and sentiment.
        
        Args:
            interview_id: Unique identifier for the interview
            user_input: Transcribed user input
            sentiment: Sentiment analysis results
            
        Returns:
            Updated conversation state
        """
        if interview_id not in self.interviews:
            self.interviews[interview_id] = InterviewContext(
                interview_id=interview_id,
                state=InterviewState.NOT_STARTED,
                current_question_index=0,
                responses={},
                metadata={}
            )

        context = self.interviews[interview_id]
        
        # Update the state based on the interaction
        if context.state == InterviewState.NOT_STARTED:
            context.state = InterviewState.IN_PROGRESS
        
        # Store the response
        context.responses[str(context.current_question_index)] = {
            "text": user_input,
            "sentiment": sentiment
        }
        
        # Increment question index
        context.current_question_index += 1
        
        return {
            "interview_id": interview_id,
            "state": context.state.value,
            "current_question_index": context.current_question_index,
            "responses": context.responses
        }

    async def get_response(
        self,
        interview_id: str,
        current_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get the next response or question based on the current state.
        
        Args:
            interview_id: Unique identifier for the interview
            current_state: Current conversation state
            
        Returns:
            Response containing next question or feedback
        """
        context = self.interviews.get(interview_id)
        if not context:
            return {
                "error": "Interview not found",
                "message": "Please start a new interview"
            }

        # For now, return a simple response
        return {
            "type": "question",
            "content": f"Question {context.current_question_index + 1}",
            "metadata": {
                "state": context.state.value,
                "question_index": context.current_question_index
            }
        }

    async def get_interview_status(self, interview_id: str) -> Dict[str, Any]:
        """
        Get the current status of an interview.
        
        Args:
            interview_id: Unique identifier for the interview
            
        Returns:
            Dict containing the interview status
        """
        context = self.interviews.get(interview_id)
        if not context:
            return {
                "error": "Interview not found",
                "status": "not_found"
            }

        return {
            "interview_id": interview_id,
            "state": context.state.value,
            "current_question_index": context.current_question_index,
            "total_responses": len(context.responses)
        }

    async def reset_interview(self, interview_id: str) -> Dict[str, Any]:
        """
        Reset an interview to its initial state.
        
        Args:
            interview_id: Unique identifier for the interview
            
        Returns:
            Dict containing the reset confirmation
        """
        if interview_id in self.interviews:
            del self.interviews[interview_id]
        
        return {
            "message": "Interview reset successfully",
            "interview_id": interview_id
        } 