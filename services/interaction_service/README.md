# Interaction Service

## Overview
The Interaction Service is the core component of the AI Interview Simulator, responsible for managing real-time interview conversations and analyzing user responses through multiple modalities.

## Features
- Real-time speech processing (STT/TTS)
- Multi-modal sentiment analysis
- Dynamic conversation management
- Interview state tracking
- Comprehensive feedback generation

## Technical Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **AI/ML Components**:
  - Google Cloud Speech-to-Text
  - Google Cloud Text-to-Speech
  - DistilBERT for sentiment analysis
  - DeepFace for facial expression analysis
  - DialoGPT for response generation

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- Docker (for containerized deployment)
- Google Cloud credentials
- Redis (for caching)

### Local Development Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the service:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

### WebSocket Endpoints
- `ws://localhost:8000/ws/interview` - Main interview WebSocket endpoint
- `ws://localhost:8000/ws/feedback` - Real-time feedback WebSocket endpoint

### REST Endpoints
- `POST /api/v1/interview/start` - Start a new interview session
- `POST /api/v1/interview/end` - End an interview session
- `GET /api/v1/interview/{session_id}/status` - Get interview status
- `POST /api/v1/interview/{session_id}/feedback` - Get interview feedback

## Architecture

### Components
1. **Speech Processing Module**
   - Handles real-time speech-to-text conversion
   - Manages text-to-speech synthesis
   - Implements voice activity detection

2. **Sentiment Analysis Module**
   - Text-based sentiment analysis
   - Facial expression analysis
   - Combined sentiment scoring

3. **Conversation Management**
   - Interview flow control
   - Response generation
   - Context management

4. **State Management**
   - Interview progress tracking
   - Session management
   - Checklist tracking

## Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_speech_processing.py

# Run with coverage
pytest --cov=app tests/
```

## Deployment
The service can be deployed using Docker:
```bash
docker build -t interaction-service .
docker run -p 8000:8000 interaction-service
```

## Monitoring and Logging
- Prometheus metrics available at `/metrics`
- Structured logging with JSON format
- Health check endpoint at `/health`

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[License information to be added] 