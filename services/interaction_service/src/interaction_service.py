"""
This module contains the InterviewInteractionService class, which is responsible for managing the interview process.
It includes the following classes:
- InterviewState: Enum for the state of the interview
- InterviewContext: Dataclass for the context of the interview
- SpeechProcessor: Abstract base class for speech processing
- SentimentAnalyzer: Abstract base class for sentiment analysis
- ConversationManager: Abstract base class for conversation management
- InterviewInteractionService: Class for managing the interview process
"""

from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Any


class InterviewState(Enum):
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class InterviewContext:
    interview_id: str
    user_id: str
    current_state: InterviewState
    start_time: datetime
    current_question_index: int = 0
    metadata: Dict[str, Any] = None

class SpeechProcessor(ABC):
    @abstractmethod
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text."""
        pass

    @abstractmethod
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech."""
        pass

class SentimentAnalyzer(ABC):
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment from text."""
        pass

    @abstractmethod
    async def analyze_facial_expression(self, image_data: bytes) -> Dict[str, float]:
        """Analyze facial expressions from image."""
        pass

class ConversationManager(ABC):
    @abstractmethod
    async def generate_response(self, context: InterviewContext, user_input: str) -> str:
        """Generate AI response based on context and user input."""
        pass

    @abstractmethod
    async def evaluate_response(self, context: InterviewContext, user_response: str) -> Dict[str, Any]:
        """Evaluate user's response."""
        pass

class InterviewSummarizer(ABC):
    @abstractmethod
    async def summarize_interview(self, context: InterviewContext) -> str:
        """Summarize the interview."""
        pass

class InterviewInteractionService:
    """
    This class is responsible for managing the interview process.
    It includes the following methods:
    - start_interview: Start a new interview session
    - process_user_input: Process user input and generate response
    - end_interview: End an interview session and return summary
    """
    def __init__(
        self,
        speech_processor: SpeechProcessor,
        sentiment_analyzer: SentimentAnalyzer,
        conversation_manager: ConversationManager
    ):
        self.speech_processor = speech_processor
        self.sentiment_analyzer = sentiment_analyzer
        self.conversation_manager = conversation_manager
        self.active_interviews: Dict[str, InterviewContext] = {}

    async def start_interview(self, user_id: str, interview_type: str) -> str:
        """Start a new interview session."""
        interview_id = f"{user_id}_{datetime.now().timestamp()}"  # TODO: Implement an objectively unique interview ID generation
        context = InterviewContext(
            interview_id=interview_id,
            user_id=user_id,
            current_state=InterviewState.IN_PROGRESS,
            start_time=datetime.now(),
            metadata={"type": interview_type}
        )
        self.active_interviews[interview_id] = context
        return interview_id

    async def process_user_input(
        self,
        interview_id: str,
        audio_data: Optional[bytes] = None,
        text_input: Optional[str] = None,
        image_data: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """Process user input and generate response."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")

        context = self.active_interviews[interview_id]
        
        # Process speech if audio provided
        if audio_data:
            text_input = await self.speech_processor.speech_to_text(audio_data)
        
        # Analyze sentiment if text provided
        sentiment_analysis = None
        if text_input:
            sentiment_analysis = await self.sentiment_analyzer.analyze_sentiment(text_input)
        
        # Analyze facial expression if image provided
        facial_analysis = None
        if image_data:
            facial_analysis = await self.sentiment_analyzer.analyze_facial_expression(image_data)
        
        # Generate AI response
        ai_response = await self.conversation_manager.generate_response(context, text_input)
        
        # Convert AI response to speech
        speech_response = await self.speech_processor.text_to_speech(ai_response)
        
        return {
            "text_response": ai_response,
            "speech_response": speech_response,
            "sentiment_analysis": sentiment_analysis,
            "facial_analysis": facial_analysis
        }

    async def end_interview(self, interview_id: str) -> Dict[str, Any]:
        """End an interview session and return summary."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")
        
        context = self.active_interviews[interview_id]
        context.current_state = InterviewState.COMPLETED
        
        # TODO: Implement interview summary generation
        summary = {
            "interview_id": interview_id,
            "duration": (datetime.now() - context.start_time).total_seconds(),
            "questions_answered": context.current_question_index,
            # Add more summary metrics as needed
        }
        
        del self.active_interviews[interview_id]
        return summary 