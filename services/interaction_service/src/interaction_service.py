"""
This module contains the InterviewInteractionService class, which is responsible for managing the interview process.
It includes the following classes:
- InterviewInteractionService: Class for managing the interview process
"""

import asyncio
from datetime import datetime
from typing import Dict, Optional, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from .sentiment_analyzer import MultiModalSentimentAnalyzer
from .speech_processor import GoogleCloudSpeechProcessor
from .conversation_manager import InterviewConversationManager, InterviewContext, InterviewState
from .interview_summarizer import DefaultInterviewSummarizer
from .questionnaire import InterviewQuestionnaire

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        speech_processor: GoogleCloudSpeechProcessor,
        sentiment_analyzer: MultiModalSentimentAnalyzer,
        conversation_manager: InterviewConversationManager,
        interview_summarizer: Optional[Any] = None,
        structure_service: Optional[Any] = None
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

    async def process_interview_step(
        self,
        interview_id: str,
        audio_data: bytes,
        video_data: Optional[bytes] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a single step of the interview interaction.
        
        Args:
            interview_id: Unique identifier for the interview
            audio_data: Raw audio data from the user
            video_data: Optional video data from the user
            metadata: Additional metadata about the interaction
            
        Returns:
            Dict containing the processed results
        """
        # Process speech
        transcription = await self.speech_processor.process_audio(audio_data)
        
        # Analyze sentiment
        sentiment = await self.sentiment_analyzer.analyze(
            text=transcription,
            video_data=video_data
        )
        
        # Update conversation state
        conversation_state = await self.conversation_manager.update_state(
            interview_id=interview_id,
            user_input=transcription,
            sentiment=sentiment
        )
        
        # Get next question or response
        response = await self.conversation_manager.get_response(
            interview_id=interview_id,
            current_state=conversation_state
        )
        
        return {
            "transcription": transcription,
            "sentiment": sentiment,
            "response": response,
            "conversation_state": conversation_state
        }

    async def get_interview_status(self, interview_id: str) -> Dict[str, Any]:
        """
        Get the current status of an interview.
        
        Args:
            interview_id: Unique identifier for the interview
            
        Returns:
            Dict containing the interview status
        """
        return await self.conversation_manager.get_interview_status(interview_id)

    async def reset_interview(self, interview_id: str) -> Dict[str, Any]:
        """
        Reset an interview to its initial state.
        
        Args:
            interview_id: Unique identifier for the interview
            
        Returns:
            Dict containing the reset confirmation
        """
        return await self.conversation_manager.reset_interview(interview_id)

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

app = FastAPI(title="Interview Interaction Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
sentiment_analyzer = MultiModalSentimentAnalyzer()
summarizer = InterviewSummarizer()

# Store active sessions
active_sessions: Dict[str, InterviewContext] = {}

@app.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for interview interactions."""
    await websocket.accept()
    
    try:
        # Initialize or retrieve session context
        if session_id not in active_sessions:
            # In a real app, you'd get this from a database
            active_sessions[session_id] = InterviewContext(
                session_id=session_id,
                user_id="test_user"  # This should come from authentication
            )
        
        context = active_sessions[session_id]
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "answer":
                # Process answer
                answer = message["content"]
                context.answer_history.append(answer)
                
                # Analyze sentiment
                sentiment = sentiment_analyzer.analyze(answer)
                context.sentiment_history.append(sentiment)
                context.current_sentiment = sentiment
                
                # Send response
                await websocket.send_json({
                    "type": "sentiment",
                    "sentiment": sentiment
                })
                
            elif message["type"] == "question":
                # Store question
                question = message["content"]
                context.current_question = question
                context.question_history.append(question)
                
            elif message["type"] == "end_interview":
                # Generate summary
                summary = summarizer.summarize(context)
                key_points = summarizer.get_key_points(context)
                
                # Send summary
                await websocket.send_json({
                    "type": "summary",
                    "summary": summary,
                    "key_points": key_points
                })
                
                # Clean up
                del active_sessions[session_id]
                break
                
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from session {session_id}")
        if session_id in active_sessions:
            del active_sessions[session_id]
    except Exception as e:
        logger.error(f"Error in session {session_id}: {str(e)}")
        await websocket.close(code=1011)  # Internal error

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()} 