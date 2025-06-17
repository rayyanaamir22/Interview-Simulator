from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from models.interviewer import InterviewerModel

app = FastAPI(
    title="Interaction Service",
    description="Service for handling interview interactions",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the interviewer model
interviewer = InterviewerModel()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/interview")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive user input
            user_input = await websocket.receive_text()
            
            # Generate and stream response
            async for chunk in interviewer.generate_response(user_input):
                await websocket.send_text(chunk)
                
    except Exception as e:
        await websocket.close() 