"""
This module contains the GoogleCloudSpeechProcessor class, which is responsible for converting speech to text and text to speech using Google Cloud Speech-to-Text and Text-to-Speech.
It includes the following classes:
- GoogleCloudSpeechProcessor: Class for converting speech to text and text to speech using Google Cloud Speech-to-Text and Text-to-Speech
"""

from typing import Optional
import os
from google.cloud import texttospeech, speech
from .interaction_service import SpeechProcessor

class GoogleCloudSpeechProcessor(SpeechProcessor):
    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Google Cloud Speech and Text-to-Speech clients."""
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        self.speech_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()

    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text using Google Cloud Speech-to-Text."""
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True
        )

        response = self.speech_client.recognize(config=config, audio=audio)
        
        # Combine all transcriptions
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return transcript

    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using Google Cloud Text-to-Speech."""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Configure voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",  # Using a neural voice for better quality
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        # Configure audio parameters
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )

        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content 