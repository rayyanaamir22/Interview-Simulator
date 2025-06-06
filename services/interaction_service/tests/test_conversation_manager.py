import pytest
from src.conversation_manager import ConversationManager

def test_conversation_manager_initialization(conversation_manager):
    """Test that the conversation manager initializes correctly."""
    assert conversation_manager is not None

def test_get_next_response(conversation_manager):
    """Test getting the next response in the conversation."""
    user_input = "I have experience in Python and JavaScript"
    response = conversation_manager.get_next_response(user_input)
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_conversation_history(conversation_manager):
    """Test that conversation history is maintained correctly."""
    # Add some conversation turns
    conversation_manager.get_next_response("Hello")
    conversation_manager.get_next_response("I'm here for the interview")
    
    history = conversation_manager.get_conversation_history()
    
    assert history is not None
    assert isinstance(history, list)
    assert len(history) >= 2

def test_reset_conversation(conversation_manager):
    """Test resetting the conversation."""
    # Add some conversation turns
    conversation_manager.get_next_response("Hello")
    conversation_manager.get_next_response("I'm here for the interview")
    
    # Reset the conversation
    conversation_manager.reset_conversation()
    
    history = conversation_manager.get_conversation_history()
    assert len(history) == 0

def test_invalid_input_handling(conversation_manager):
    """Test handling of invalid inputs."""
    with pytest.raises(ValueError):
        conversation_manager.get_next_response("")
    
    with pytest.raises(ValueError):
        conversation_manager.get_next_response(None) 