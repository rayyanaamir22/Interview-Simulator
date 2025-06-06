"""
This module contains the MultiModalSentimentAnalyzer class, which is responsible for analyzing sentiment from text and facial expressions.
It includes the following classes:
- MultiModalSentimentAnalyzer: Class for analyzing sentiment from text and facial expressions
"""

from typing import Dict, Any
import numpy as np
from transformers import pipeline
from deepface import DeepFace
from .interaction_service import SentimentAnalyzer

class MultiModalSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self):
        """Initialize sentiment analysis models."""
        # Initialize text sentiment analysis pipeline
        self.text_sentiment = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
        
        # Define emotion mapping for facial analysis
        self.emotion_mapping = {
            'angry': 'anger',
            'disgust': 'disgust',
            'fear': 'fear',
            'happy': 'happiness',
            'sad': 'sadness',
            'surprise': 'surprise',
            'neutral': 'neutral'
        }

    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment from text using Hugging Face transformers."""
        results = self.text_sentiment(text)[0]
        
        # Convert results to a more usable format
        sentiment_scores = {
            result['label'].lower(): float(result['score'])
            for result in results
        }
        
        return sentiment_scores

    async def analyze_facial_expression(self, image_data: bytes) -> Dict[str, float]:
        """Analyze facial expressions using DeepFace."""
        try:
            # Save image data to temporary file
            with open('temp_image.jpg', 'wb') as f:
                f.write(image_data)
            
            # Analyze facial expressions
            result = DeepFace.analyze(
                img_path='temp_image.jpg',
                actions=['emotion'],
                enforce_detection=False
            )
            
            # Clean up temporary file
            import os
            os.remove('temp_image.jpg')
            
            # Extract emotion scores
            emotions = result[0]['emotion']
            
            # Map emotions to our standard format
            mapped_emotions = {
                self.emotion_mapping.get(k, k): float(v)
                for k, v in emotions.items()
            }
            
            return mapped_emotions
            
        except Exception as e:
            # Return neutral emotion if analysis fails
            return {
                'neutral': 1.0,
                'happiness': 0.0,
                'sadness': 0.0,
                'anger': 0.0,
                'fear': 0.0,
                'surprise': 0.0,
                'disgust': 0.0
            } 