import pytest
from src.questionnaire import Questionnaire

def test_questionnaire_initialization(questionnaire):
    """Test that the questionnaire initializes correctly."""
    assert questionnaire is not None
    assert questionnaire.get_current_question() is not None

def test_get_current_question(questionnaire):
    """Test getting the current question."""
    question = questionnaire.get_current_question()
    
    assert question is not None
    assert isinstance(question, str)
    assert len(question) > 0

def test_move_to_next_question(questionnaire):
    """Test moving to the next question."""
    first_question = questionnaire.get_current_question()
    questionnaire.move_to_next_question()
    second_question = questionnaire.get_current_question()
    
    assert first_question != second_question
    assert second_question is not None
    assert isinstance(second_question, str)
    assert len(second_question) > 0

def test_is_complete(questionnaire):
    """Test questionnaire completion status."""
    # Move through all questions
    while not questionnaire.is_complete():
        questionnaire.move_to_next_question()
    
    assert questionnaire.is_complete()

def test_reset_questionnaire(questionnaire):
    """Test resetting the questionnaire."""
    # Move to a later question
    questionnaire.move_to_next_question()
    questionnaire.move_to_next_question()
    
    # Reset the questionnaire
    questionnaire.reset()
    
    # Should be back at the first question
    assert not questionnaire.is_complete()
    first_question = questionnaire.get_current_question()
    assert first_question is not None

def test_get_question_count(questionnaire):
    """Test getting the total number of questions."""
    count = questionnaire.get_question_count()
    
    assert isinstance(count, int)
    assert count > 0

def test_get_current_question_index(questionnaire):
    """Test getting the current question index."""
    index = questionnaire.get_current_question_index()
    
    assert isinstance(index, int)
    assert index >= 0
    assert index < questionnaire.get_question_count() 