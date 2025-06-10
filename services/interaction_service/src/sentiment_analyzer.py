"""
This module contains the MultiModalSentimentAnalyzer class, which is responsible for analyzing sentiment from text and facial expressions.
It includes the following classes:
- MultiModalSentimentAnalyzer: Class for analyzing sentiment from text and facial expressions
"""

from typing import Dict, Any, Tuple
import os
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import pipeline
from .base import SentimentAnalyzer

class MultiModalSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self):
        """Initialize sentiment analysis models."""
        # Initialize emotion detection pipeline
        self.emotion_detector = pipeline(
            "image-classification",
            model="microsoft/resnet-50",
            top_k=1
        )
        
        # Initialize text sentiment analysis pipeline
        self.text_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        # Load face detection model
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment from text."""
        try:
            result = self.text_analyzer(text)
            return {
                "sentiment": result[0]["label"],
                "confidence": float(result[0]["score"])
            }
        except Exception as e:
            return {"error": str(e)}

    async def analyze_facial_expression(self, image_data: bytes) -> Dict[str, float]:
        """Analyze facial expressions from image."""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                return {"error": "No face detected"}
            
            # Get the first face
            x, y, w, h = faces[0]
            face_img = image[y:y+h, x:x+w]
            
            # Convert to PIL Image for the model
            face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
            
            # Get emotion prediction
            result = self.emotion_detector(face_pil)
            
            return {
                "emotion": result[0]["label"],
                "confidence": float(result[0]["score"]),
                "face_detected": True
            }
            
        except Exception as e:
            return {"error": str(e)}

    def analyze_interaction(self, image_path: str, text: str) -> Dict[str, Any]:
        """Analyze both image and text for comprehensive sentiment analysis."""
        image_result = self.analyze_facial_expression(image_path)
        text_result = self.analyze_sentiment(text)
        
        return {
            "image_analysis": image_result,
            "text_analysis": text_result
        } 