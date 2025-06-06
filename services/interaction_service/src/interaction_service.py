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
from typing import Dict, Optional, Any, List


class InterviewState(Enum):
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class ChecklistItem:
    description: str
    is_completed: bool = False
    notes: str = ""

@dataclass
class InterviewContext:
    interview_id: str
    user_id: str
    current_state: InterviewState
    start_time: datetime
    current_question_index: int = 0
    metadata: Dict[str, Any] = None
    checklist: List[ChecklistItem] = None
    implicit_thoughts: List[str] = None
    structure_service_id: Optional[str] = None  # Reference to structure service interview

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

class DefaultInterviewSummarizer(InterviewSummarizer):
    """
    This class is responsible for summarizing the interview.
    It includes the following methods:
    - summarize_interview: Summarize the interview.
    - _analyze_sentiment_trends: Analyze sentiment trends throughout the interview.
    - _generate_assessment: Generate an overall assessment of the interview performance.
    - _identify_strengths: Identify key strengths demonstrated during the interview.
    - _identify_improvements: Identify areas that need improvement.
    """
    async def summarize_interview(self, context: InterviewContext) -> Dict[str, Any]:
        """Generate a comprehensive summary of the interview."""
        # Calculate time metrics
        duration = (datetime.now() - context.start_time).total_seconds()
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        # Analyze sentiment trends
        sentiment_trends = self._analyze_sentiment_trends(context)
        
        # Generate overall assessment
        assessment = self._generate_assessment(context)
        
        return {
            "duration": f"{minutes}m {seconds}s",
            "questions_answered": context.current_question_index,
            "sentiment_trends": sentiment_trends,
            "assessment": assessment,
            "strengths": self._identify_strengths(context),
            "areas_for_improvement": self._identify_improvements(context),
            "recommendations": self._generate_recommendations(context)
        }
    
    def _analyze_sentiment_trends(self, context: InterviewContext) -> Dict[str, Any]:
        """Analyze sentiment trends throughout the interview."""
        if not context.implicit_thoughts:
            return {"message": "No sentiment data available"}
            
        # Extract sentiment scores from implicit thoughts
        sentiments = []
        for thought in context.implicit_thoughts:
            if "tone appears" in thought:
                sentiment = thought.split("tone appears")[1].split("(")[0].strip()
                confidence = float(thought.split("(")[1].split(")")[0])
                sentiments.append((sentiment, confidence))
        
        if not sentiments:
            return {"message": "No sentiment data available"}
            
        # Calculate dominant sentiments
        sentiment_counts = {}
        for sentiment, confidence in sentiments:
            if confidence > 0.5:  # Only count high confidence predictions
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        return {
            "dominant_sentiment": max(sentiment_counts.items(), key=lambda x: x[1])[0] if sentiment_counts else "neutral",
            "sentiment_distribution": sentiment_counts,
            "total_analyzed": len(sentiments)
        }
    
    def _generate_assessment(self, context: InterviewContext) -> str:
        """Generate an overall assessment of the interview performance."""
        if not context.checklist:
            return "No assessment criteria provided"
            
        completed_items = sum(1 for item in context.checklist if item.is_completed)
        total_items = len(context.checklist)
        completion_rate = (completed_items / total_items) * 100 if total_items > 0 else 0
        
        if completion_rate >= 80:
            return "Excellent performance - demonstrated strong understanding of key concepts"
        elif completion_rate >= 60:
            return "Good performance - showed solid understanding with some areas for improvement"
        elif completion_rate >= 40:
            return "Satisfactory performance - basic understanding demonstrated"
        else:
            return "Needs improvement - key concepts require more attention"
    
    def _identify_strengths(self, context: InterviewContext) -> List[str]:
        """Identify key strengths demonstrated during the interview."""
        strengths = []
        
        # Analyze completed checklist items
        if context.checklist:
            completed_items = [item for item in context.checklist if item.is_completed]
            if completed_items:
                strengths.append(f"Successfully addressed {len(completed_items)} key assessment criteria")
        
        # Analyze sentiment trends
        if context.implicit_thoughts:
            positive_sentiments = sum(1 for thought in context.implicit_thoughts 
                                   if "positive" in thought.lower() or "happy" in thought.lower())
            if positive_sentiments > len(context.implicit_thoughts) / 2:
                strengths.append("Maintained positive and engaging communication style")
        
        return strengths
    
    def _identify_improvements(self, context: InterviewContext) -> List[str]:
        """Identify areas that need improvement."""
        improvements = []
        
        # Analyze incomplete checklist items
        if context.checklist:
            incomplete_items = [item for item in context.checklist if not item.is_completed]
            if incomplete_items:
                improvements.append(f"Need to address {len(incomplete_items)} remaining assessment criteria")
        
        # Analyze sentiment trends
        if context.implicit_thoughts:
            negative_sentiments = sum(1 for thought in context.implicit_thoughts 
                                   if "negative" in thought.lower() or "sad" in thought.lower())
            if negative_sentiments > len(context.implicit_thoughts) / 3:
                improvements.append("Work on maintaining more positive communication tone")
        
        return improvements
    
    def _generate_recommendations(self, context: InterviewContext) -> List[str]:
        """Generate specific recommendations for improvement."""
        recommendations = []
        
        # Add recommendations based on incomplete checklist items
        if context.checklist:
            incomplete_items = [item for item in context.checklist if not item.is_completed]
            for item in incomplete_items:
                recommendations.append(f"Focus on developing skills related to: {item.description}")
        
        # Add general recommendations based on interview performance
        if context.current_question_index < 5:
            recommendations.append("Practice more interview scenarios to build confidence")
        
        return recommendations

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
        conversation_manager: ConversationManager,
        interview_summarizer: InterviewSummarizer,
        structure_service: Any  # Type hint for structure service
    ):
        self.speech_processor = speech_processor
        self.sentiment_analyzer = sentiment_analyzer
        self.conversation_manager = conversation_manager
        self.interview_summarizer = interview_summarizer
        self.structure_service = structure_service
        self.active_interviews: Dict[str, InterviewContext] = {}

    async def start_interview(
        self,
        user_id: str,
        interview_type: str,
        checklist: Optional[List[str]] = None,
        custom_schedule: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Start a new interview session."""
        interview_id = f"{user_id}_{datetime.now().timestamp()}"
        
        # Initialize checklist items
        checklist_items = [
            ChecklistItem(description=item) for item in (checklist or [])
        ]
        
        # Create interview context
        context = InterviewContext(
            interview_id=interview_id,
            user_id=user_id,
            current_state=InterviewState.IN_PROGRESS,
            start_time=datetime.now(),
            metadata={"type": interview_type},
            checklist=checklist_items,
            implicit_thoughts=[]
        )
        
        # Start structure service
        schedule = await self.structure_service.create_schedule(custom_schedule)
        await self.structure_service.start_interview(
            interview_id=interview_id,
            schedule=schedule,
            phase_transition_callback=self._handle_phase_transition
        )
        context.structure_service_id = interview_id
        
        self.active_interviews[interview_id] = context
        return interview_id

    async def _handle_phase_transition(self, transition_data: Dict[str, Any]) -> None:
        """Handle phase transition from structure service."""
        interview_id = transition_data.get("interview_id")
        if not interview_id or interview_id not in self.active_interviews:
            return

        context = self.active_interviews[interview_id]
        
        # Add phase transition to implicit thoughts
        time_impact = transition_data.get("time_impact", {})
        if time_impact.get("is_over_time", False):
            context.implicit_thoughts.append(
                f"Phase timing impact: {abs(time_impact['difference_minutes']):.1f} minutes over time"
            )
        
        # Update conversation context based on new phase
        if "to_phase" in transition_data:
            context.implicit_thoughts.append(
                f"Transitioning to {transition_data['to_phase']} phase"
            )

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
        
        # Get time warnings from structure service
        time_warnings = await self.structure_service.get_time_warnings(interview_id)
        
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
        
        # Generate implicit thoughts
        implicit_thoughts = await self._generate_implicit_thoughts(
            context,
            text_input,
            sentiment_analysis,
            facial_analysis,
            time_warnings
        )
        context.implicit_thoughts.append(implicit_thoughts)
        
        # Update checklist based on response
        await self._update_checklist(context, text_input, ai_response)
        
        # Convert AI response to speech
        speech_response = await self.speech_processor.text_to_speech(ai_response)
        
        return {
            "text_response": ai_response,
            "speech_response": speech_response,
            "sentiment_analysis": sentiment_analysis,
            "facial_analysis": facial_analysis,
            "implicit_thoughts": implicit_thoughts,
            "checklist_progress": self._get_checklist_progress(context),
            "time_warnings": time_warnings.get("warnings", [])
        }

    async def _generate_implicit_thoughts(
        self,
        context: InterviewContext,
        user_input: str,
        sentiment_analysis: Optional[Dict[str, float]],
        facial_analysis: Optional[Dict[str, float]],
        time_warnings: Dict[str, Any]
    ) -> str:
        """Generate implicit thoughts based on user input and analysis."""
        thoughts = []
        
        if sentiment_analysis:
            dominant_sentiment = max(sentiment_analysis.items(), key=lambda x: x[1])
            thoughts.append(f"User's tone appears {dominant_sentiment[0]} ({dominant_sentiment[1]:.2f} confidence)")
        
        if facial_analysis:
            dominant_emotion = max(facial_analysis.items(), key=lambda x: x[1])
            thoughts.append(f"Facial expression shows {dominant_emotion[0]} ({dominant_emotion[1]:.2f} confidence)")
        
        # Add time-related thoughts
        for warning in time_warnings.get("warnings", []):
            thoughts.append(f"Time management: {warning['message']}")
        
        # Add context-specific thoughts
        if context.current_question_index > 0:
            thoughts.append(f"Progressing through question {context.current_question_index}")
        
        return " | ".join(thoughts)

    async def _update_checklist(
        self,
        context: InterviewContext,
        user_input: str,
        ai_response: str
    ) -> None:
        """Update checklist items based on user input and AI response."""
        if not context.checklist:
            return
            
        # Example checklist update logic - this should be customized based on specific criteria
        for item in context.checklist:
            if not item.is_completed:
                # Check if the response addresses this checklist item
                if any(keyword.lower() in user_input.lower() for keyword in item.description.split()):
                    item.is_completed = True
                    item.notes = f"Addressed in response to question {context.current_question_index}"

    def _get_checklist_progress(self, context: InterviewContext) -> Dict[str, Any]:
        """Get the current progress of the checklist."""
        if not context.checklist:
            return {"total": 0, "completed": 0, "items": []}
            
        return {
            "total": len(context.checklist),
            "completed": sum(1 for item in context.checklist if item.is_completed),
            "items": [
                {
                    "description": item.description,
                    "is_completed": item.is_completed,
                    "notes": item.notes
                }
                for item in context.checklist
            ]
        }

    async def pause_interview(self, interview_id: str) -> None:
        """Pause the interview."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")
            
        context = self.active_interviews[interview_id]
        context.current_state = InterviewState.PAUSED
        
        # Pause structure service
        if context.structure_service_id:
            await self.structure_service.pause_interview(context.structure_service_id)

    async def resume_interview(self, interview_id: str) -> None:
        """Resume the interview."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")
            
        context = self.active_interviews[interview_id]
        context.current_state = InterviewState.IN_PROGRESS
        
        # Resume structure service
        if context.structure_service_id:
            await self.structure_service.resume_interview(context.structure_service_id)

    async def end_interview(self, interview_id: str) -> Dict[str, Any]:
        """End an interview session and return summary."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")
        
        context = self.active_interviews[interview_id]
        context.current_state = InterviewState.COMPLETED
        
        # Generate interview summary
        summary = await self.interview_summarizer.summarize_interview(context)
        
        # Add checklist progress to summary
        summary.update({
            "interview_id": interview_id,
            "duration": (datetime.now() - context.start_time).total_seconds(),
            "questions_answered": context.current_question_index,
            "checklist_progress": self._get_checklist_progress(context),
            "implicit_thoughts": context.implicit_thoughts
        })
        
        del self.active_interviews[interview_id]
        return summary 