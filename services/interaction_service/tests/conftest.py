import pytest
from src.interaction_service import InteractionService
from src.sentiment_analyzer import SentimentAnalyzer
from src.conversation_manager import ConversationManager
from src.questionnaire import Questionnaire
from src.speech_processor import SpeechProcessor

@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()

@pytest.fixture
def conversation_manager():
    return ConversationManager()

@pytest.fixture
def questionnaire():
    return Questionnaire()

@pytest.fixture
def speech_processor():
    return SpeechProcessor()

@pytest.fixture
def interaction_service(sentiment_analyzer, conversation_manager, questionnaire, speech_processor):
    return InteractionService(
        sentiment_analyzer=sentiment_analyzer,
        conversation_manager=conversation_manager,
        questionnaire=questionnaire,
        speech_processor=speech_processor
    ) 