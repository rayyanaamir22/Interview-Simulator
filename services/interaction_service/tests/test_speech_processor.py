import pytest
from src.speech_processor import SpeechProcessor

def test_speech_processor_initialization(speech_processor):
    """Test that the speech processor initializes correctly."""
    assert speech_processor is not None

def test_process_input(speech_processor):
    """Test processing text input."""
    text = "Hello, I'm here for the interview"
    processed_text = speech_processor.process_input(text)
    
    assert processed_text is not None
    assert isinstance(processed_text, str)
    assert len(processed_text) > 0

def test_process_input_with_punctuation(speech_processor):
    """Test processing text input with punctuation."""
    text = "Hello! I'm here for the interview..."
    processed_text = speech_processor.process_input(text)
    
    assert processed_text is not None
    assert isinstance(processed_text, str)
    assert len(processed_text) > 0

def test_process_input_with_numbers(speech_processor):
    """Test processing text input with numbers."""
    text = "I have 5 years of experience in Python and 3 years in JavaScript"
    processed_text = speech_processor.process_input(text)
    
    assert processed_text is not None
    assert isinstance(processed_text, str)
    assert len(processed_text) > 0

def test_process_input_with_special_characters(speech_processor):
    """Test processing text input with special characters."""
    text = "I'm experienced in C++, Python, and JavaScript!"
    processed_text = speech_processor.process_input(text)
    
    assert processed_text is not None
    assert isinstance(processed_text, str)
    assert len(processed_text) > 0

def test_process_empty_input(speech_processor):
    """Test processing empty input."""
    with pytest.raises(ValueError):
        speech_processor.process_input("")

def test_process_none_input(speech_processor):
    """Test processing None input."""
    with pytest.raises(ValueError):
        speech_processor.process_input(None) 