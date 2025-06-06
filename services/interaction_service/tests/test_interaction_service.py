import pytest
from unittest.mock import Mock, patch

def test_interaction_service_initialization(interaction_service):
    """Test that the interaction service initializes correctly with all dependencies."""
    assert interaction_service is not None
    assert interaction_service.sentiment_analyzer is not None
    assert interaction_service.conversation_manager is not None
    assert interaction_service.questionnaire is not None
    assert interaction_service.speech_processor is not None

@pytest.mark.asyncio
async def test_process_user_input(interaction_service):
    """Test processing user input through the interaction service."""
    test_input = "Hello, I'm ready for the interview"
    
    # Mock the necessary methods
    interaction_service.speech_processor.process_input = Mock(return_value=test_input)
    interaction_service.sentiment_analyzer.analyze = Mock(return_value={"sentiment": "positive", "score": 0.8})
    interaction_service.conversation_manager.get_next_response = Mock(return_value="Welcome to the interview!")
    
    response = await interaction_service.process_user_input(test_input)
    
    assert response is not None
    interaction_service.speech_processor.process_input.assert_called_once_with(test_input)
    interaction_service.sentiment_analyzer.analyze.assert_called_once()
    interaction_service.conversation_manager.get_next_response.assert_called_once()

@pytest.mark.asyncio
async def test_handle_interview_flow(interaction_service):
    """Test the interview flow handling."""
    # Mock questionnaire methods
    interaction_service.questionnaire.get_current_question = Mock(return_value="Tell me about yourself")
    interaction_service.questionnaire.is_complete = Mock(return_value=False)
    
    # Mock conversation manager
    interaction_service.conversation_manager.get_next_response = Mock(return_value="Thank you for your answer")
    
    response = await interaction_service.handle_interview_flow("I have 5 years of experience in software development")
    
    assert response is not None
    interaction_service.questionnaire.get_current_question.assert_called_once()
    interaction_service.conversation_manager.get_next_response.assert_called_once()

def test_error_handling(interaction_service):
    """Test error handling in the interaction service."""
    with pytest.raises(Exception):
        interaction_service.process_user_input(None) 