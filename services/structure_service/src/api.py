from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .structure_service import InterviewStructureService, InterviewPhase
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

structure_service = InterviewStructureService()

class PhaseConfigRequest(BaseModel):
    phase: str
    duration_minutes: int
    is_skippable: bool = False
    is_shortenable: bool = True
    description: Optional[str] = None

class InterviewConfigRequest(BaseModel):
    phases: List[PhaseConfigRequest]

@app.post("/api/interview/start")
async def start_interview(config: InterviewConfigRequest):
    try:
        # Convert request to format expected by structure service
        custom_phases = [
            {
                "phase": phase.phase.lower(),
                "duration_minutes": phase.duration_minutes,
                "is_skippable": phase.is_skippable,
                "is_shortenable": phase.is_shortenable,
                "description": phase.description or f"{phase.phase.title()} phase"
            }
            for phase in config.phases
        ]

        # Create schedule
        schedule = await structure_service.create_schedule(custom_phases)
        
        # Generate a unique interview ID (in production, this would come from user service)
        interview_id = f"interview_{datetime.now().timestamp()}"
        
        # Start the interview
        await structure_service.start_interview(
            interview_id=interview_id,
            schedule=schedule,
            phase_transition_callback=lambda x: print(f"Phase transition: {x}")  # TODO: Implement proper callback
        )
        
        return {
            "interview_id": interview_id,
            "schedule": {
                "phases": [
                    {
                        "phase": phase.phase.value,
                        "duration_minutes": phase.duration_minutes,
                        "description": phase.description
                    }
                    for phase in schedule.phases
                ],
                "total_duration_minutes": schedule.total_duration_minutes,
                "is_custom": schedule.is_custom
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/interview/{interview_id}/status")
async def get_interview_status(interview_id: str):
    try:
        current_phase = await structure_service.get_current_phase(interview_id)
        if not current_phase:
            raise HTTPException(status_code=404, detail="Interview not found")
            
        progress = await structure_service.get_phase_progress(interview_id)
        return {
            "current_phase": current_phase.phase.value,
            "progress": progress
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/interview/{interview_id}/pause")
async def pause_interview(interview_id: str):
    try:
        await structure_service.pause_interview(interview_id)
        return {"message": "Interview paused successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/interview/{interview_id}/resume")
async def resume_interview(interview_id: str):
    try:
        await structure_service.resume_interview(interview_id)
        return {"message": "Interview resumed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 