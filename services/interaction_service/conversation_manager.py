"""
This module contains the InterviewConversationManager class, which is responsible for managing the conversation during the interview.
It includes the following classes:
- InterviewConversationManager: Class for managing the conversation during the interview
"""

from typing import Dict, Any, List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from .interaction_service import ConversationManager, InterviewContext

class InterviewConversationManager(ConversationManager):
    def __init__(
        self,
        model_name: str = "microsoft/DialoGPT-medium",
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
        
        # Define interview-specific prompts and evaluation criteria
        self.interview_prompts = {
            "technical": [
                "Tell me about your experience with {technology}.",
                "How would you solve {problem}?",
                "Explain the concept of {concept}."
            ],
            "behavioral": [
                "Tell me about a time when you {situation}.",
                "How do you handle {scenario}?",
                "Describe a situation where you {action}."
            ]
        }

    async def generate_response(
        self,
        context: InterviewContext,
        user_input: str
    ) -> str:
        """Generate AI response based on context and user input."""
        # Initialize conversation history if not exists
        if context.interview_id not in self.conversation_history:
            self.conversation_history[context.interview_id] = []
        
        # Add user input to history
        self.conversation_history[context.interview_id].append(f"User: {user_input}")
        
        # Prepare conversation history for the model
        conversation = " ".join(self.conversation_history[context.interview_id])
        
        # Generate response
        inputs = self.tokenizer.encode(conversation + " Assistant:", return_tensors="pt")
        response_ids = self.model.generate(
            inputs,
            max_length=self.max_length,
            temperature=self.temperature,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7
        )
        
        response = self.tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        
        # Add response to history
        self.conversation_history[context.interview_id].append(f"Assistant: {response}")
        
        return response

    async def evaluate_response(
        self,
        context: InterviewContext,
        user_response: str
    ) -> Dict[str, Any]:
        """Evaluate user's response based on interview type and context."""
        # TODO: Implement more sophisticated evaluation logic
        # For now, return basic metrics
        evaluation = {
            "response_length": len(user_response),
            "interview_type": context.metadata.get("type", "unknown"),
            "question_index": context.current_question_index,
            "metrics": {
                "clarity": 0.0,  # TODO: Implement clarity scoring
                "relevance": 0.0,  # TODO: Implement relevance scoring
                "technical_depth": 0.0,  # TODO: Implement technical depth scoring
                "communication_skills": 0.0  # TODO: Implement communication skills scoring
            }
        }
        
        return evaluation

    def _get_next_question(self, context: InterviewContext) -> str:
        """Get the next question based on interview type and progress."""
        interview_type = context.metadata.get("type", "technical")
        questions = self.interview_prompts.get(interview_type, self.interview_prompts["technical"])
        
        if context.current_question_index < len(questions):
            return questions[context.current_question_index]
        return "Thank you for completing the interview. Do you have any questions for me?" 