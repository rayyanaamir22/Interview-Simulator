import pytest
from src.sentiment_analyzer import SentimentAnalyzer

def test_sentiment_analyzer_initialization(sentiment_analyzer):
    """Test that the sentiment analyzer initializes correctly."""
    assert sentiment_analyzer is not None

def test_analyze_positive_sentiment(sentiment_analyzer):
    """Test sentiment analysis with positive input."""
    text = "I am very excited about this opportunity and confident in my abilities"
    result = sentiment_analyzer.analyze(text)
    
    assert result is not None
    assert "sentiment" in result
    assert "score" in result
    assert result["sentiment"] in ["positive", "negative", "neutral"]
    assert isinstance(result["score"], float)
    assert 0 <= result["score"] <= 1

def test_analyze_negative_sentiment(sentiment_analyzer):
    """Test sentiment analysis with negative input."""
    text = "I am nervous and unsure about my performance"
    result = sentiment_analyzer.analyze(text)
    
    assert result is not None
    assert "sentiment" in result
    assert "score" in result
    assert result["sentiment"] in ["positive", "negative", "neutral"]
    assert isinstance(result["score"], float)
    assert 0 <= result["score"] <= 1

def test_analyze_neutral_sentiment(sentiment_analyzer):
    """Test sentiment analysis with neutral input."""
    text = "I have 5 years of experience in software development"
    result = sentiment_analyzer.analyze(text)
    
    assert result is not None
    assert "sentiment" in result
    assert "score" in result
    assert result["sentiment"] in ["positive", "negative", "neutral"]
    assert isinstance(result["score"], float)
    assert 0 <= result["score"] <= 1

def test_analyze_empty_input(sentiment_analyzer):
    """Test sentiment analysis with empty input."""
    with pytest.raises(ValueError):
        sentiment_analyzer.analyze("")

def test_analyze_invalid_input(sentiment_analyzer):
    """Test sentiment analysis with invalid input."""
    with pytest.raises(ValueError):
        sentiment_analyzer.analyze(None) 