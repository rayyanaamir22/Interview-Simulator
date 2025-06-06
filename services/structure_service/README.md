# Structure Service

## Overview
The Structure Service manages interview templates, question banks, and interview configurations for the AI Interview Simulator. It provides a flexible and scalable way to create, modify, and manage different types of interview structures.

## Features
- Dynamic interview template management
- Comprehensive question bank system
- Interview configuration management
- Template versioning
- Question difficulty calibration
- Industry-specific interview structures

## Technical Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLAlchemy

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- Docker (for containerized deployment)
- PostgreSQL 13+
- Redis 6+

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

4. Initialize the database:
   ```bash
   alembic upgrade head
   ```

5. Run the service:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

### REST Endpoints

#### Template Management
- `GET /api/v1/templates` - List all interview templates
- `POST /api/v1/templates` - Create a new template
- `GET /api/v1/templates/{template_id}` - Get template details
- `PUT /api/v1/templates/{template_id}` - Update template
- `DELETE /api/v1/templates/{template_id}` - Delete template

#### Question Bank
- `GET /api/v1/questions` - List questions with filters
- `POST /api/v1/questions` - Add new question
- `GET /api/v1/questions/{question_id}` - Get question details
- `PUT /api/v1/questions/{question_id}` - Update question
- `DELETE /api/v1/questions/{question_id}` - Delete question

#### Interview Configuration
- `GET /api/v1/configurations` - List interview configurations
- `POST /api/v1/configurations` - Create new configuration
- `GET /api/v1/configurations/{config_id}` - Get configuration details
- `PUT /api/v1/configurations/{config_id}` - Update configuration

## Architecture

### Components
1. **Template Management Module**
   - Template CRUD operations
   - Version control
   - Template validation
   - Template export/import

2. **Question Bank Module**
   - Question management
   - Categorization system
   - Difficulty calibration
   - Quality control

3. **Configuration Module**
   - Interview type definitions
   - Time management
   - Scoring criteria
   - Feedback templates

## Database Schema

### Key Tables
- `templates` - Interview templates
- `questions` - Question bank
- `categories` - Question categories
- `configurations` - Interview configurations
- `template_versions` - Template version history

## Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_templates.py

# Run with coverage
pytest --cov=app tests/
```

## Deployment
The service can be deployed using Docker:
```bash
docker build -t structure-service .
docker run -p 8000:8000 structure-service
```

## Monitoring and Logging
- Prometheus metrics available at `/metrics`
- Structured logging with JSON format
- Health check endpoint at `/health`
- Database performance monitoring

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[License information to be added] 