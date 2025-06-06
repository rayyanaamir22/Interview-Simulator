"""
This module contains the InterviewConversationManager class, which is responsible for managing the conversation during the interview.
It includes the following classes:
- InterviewConversationManager: Class for managing the conversation during the interview
"""

# frameworks
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any, List
from .interaction_service import ConversationManager, InterviewContext
from .questionnaire import InterviewQuestionnaire, QuestionCategory, Question

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
        user_response: str
    ) -> Dict[str, Any]:
        """Evaluate user's response based on interview type and context."""
        if context.interview_id not in self.current_questions:
            return {
                "feedback": "No question context found for evaluation.",
                "metrics": {}
            }
        
        current_question = self.current_questions[context.interview_id]
        evaluation_result = self.questionnaire.evaluate_response(current_question, user_response)
        
        return {
            "feedback": evaluation_result.feedback,
            "metrics": {
                "score": evaluation_result.score,
                "strengths": evaluation_result.strengths,
                "areas_for_improvement": evaluation_result.areas_for_improvement,
                "keyword_matches": evaluation_result.keyword_matches
            }
        }

    def _get_next_question(self, context: InterviewContext) -> Question:
        """Get the next question based on interview type and progress."""
        interview_type = context.metadata.get("type", "technical")
        category = QuestionCategory.TECHNICAL if interview_type == "technical" else QuestionCategory.BEHAVIORAL
        
        # Increment question index
        context.current_question_index += 1
        
        # Get next question with increasing difficulty
        difficulty = min(5, 1 + (context.current_question_index // 3))  # Increase difficulty every 3 questions
        return self.questionnaire.get_question(category, difficulty) 