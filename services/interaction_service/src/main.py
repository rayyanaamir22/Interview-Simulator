from fastapi import FastAPI
from .interaction_service import InterviewInteractionService
from .speech_processor import GoogleCloudSpeechProcessor
from .sentiment_analyzer import MultiModalSentimentAnalyzer
from .conversation_manager import InterviewConversationManager
from .questionnaire import InterviewQuestionnaire

app = FastAPI(title="Interview Interaction Service")

# Initialize service components
speech_processor = GoogleCloudSpeechProcessor()
sentiment_analyzer = MultiModalSentimentAnalyzer()
conversation_manager = InterviewConversationManager()
questionnaire = InterviewQuestionnaire()

# Initialize the main service
interaction_service = InterviewInteractionService(
    speech_processor=speech_processor,
    sentiment_analyzer=sentiment_analyzer,
    conversation_manager=conversation_manager,
    interview_summarizer=None,  # TODO: Implement interview summarizer
    structure_service=None  # TODO: Add structure service client
)

@app.get("/")
async def root():
    return {"message": "Interview Interaction Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 