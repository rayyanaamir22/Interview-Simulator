"""
This module contains the InterviewStructureService class, which is responsible for managing the interview structure and timing.
It includes the following classes:
- InterviewPhase: Enum for different interview phases
- PhaseConfig: Dataclass for phase configuration
- InterviewSchedule: Dataclass for interview schedule
- InterviewStructureService: Class for managing interview structure and timing
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import asyncio
import json

class InterviewPhase(str, Enum):
    """A string-based enum that allows custom values."""
    INTRODUCTION = "introduction"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    CODING = "coding"
    CLOSING = "closing"

    @classmethod
    def _missing_(cls, value):
        """Allow any string value to be used as a phase."""
        return value

@dataclass
class PhaseConfig:
    phase: str  # Changed from InterviewPhase to str to allow custom phases
    duration_minutes: int
    description: str
    is_skippable: bool = False
    is_shortenable: bool = True

@dataclass
class InterviewSchedule:
    phases: List[PhaseConfig]
    total_duration_minutes: int
    is_custom: bool = False
    created_at: datetime = datetime.now()

@dataclass
class PhaseState:
    phase: str  # Changed from InterviewPhase to str to allow custom phases
    start_time: datetime
    end_time: datetime
    is_completed: bool = False
    is_skipped: bool = False
    actual_duration_minutes: Optional[float] = None

class InterviewStructureService:
    """
    This class is responsible for managing the interview structure and timing.
    It includes the following methods:
    - create_schedule: Create a new interview schedule
    - start_interview: Start the interview timer
    - get_current_phase: Get the current phase of the interview
    - get_phase_progress: Get the progress of the current phase
    - handle_phase_transition: Handle phase transition
    - pause_interview: Pause the interview timer
    - resume_interview: Resume the interview timer
    - get_time_warnings: Get time warnings for the current phase
    """

    DEFAULT_SCHEDULE = InterviewSchedule(
        phases=[
            PhaseConfig(InterviewPhase.INTRODUCTION, 5, "Introduction and rapport building"),
            PhaseConfig(InterviewPhase.BEHAVIORAL, 15, "Behavioral questions and past experience"),
            PhaseConfig(InterviewPhase.TECHNICAL, 20, "Technical knowledge assessment"),
            PhaseConfig(InterviewPhase.CODING, 30, "Coding problem solving"),
            PhaseConfig(InterviewPhase.CLOSING, 5, "Closing remarks and questions")
        ],
        total_duration_minutes=75
    )

    def __init__(self):
        self.active_interviews: Dict[str, Dict[str, Any]] = {}
        self.phase_transition_callbacks: Dict[str, callable] = {}

    async def create_schedule(
        self,
        custom_phases: Optional[List[Dict[str, Any]]] = None
    ) -> InterviewSchedule:
        """Create a new interview schedule."""
        if not custom_phases:
            return self.DEFAULT_SCHEDULE

        phases = []
        total_duration = 0

        for phase_data in custom_phases:
            phase = phase_data["phase"].lower()  # Accept any phase name
            duration = phase_data["duration_minutes"]
            description = phase_data.get("description", f"{phase.title()} phase")
            
            phases.append(PhaseConfig(
                phase=phase,
                duration_minutes=duration,
                description=description
            ))
            total_duration += duration

        return InterviewSchedule(
            phases=phases,
            total_duration_minutes=total_duration,
            is_custom=True
        )

    async def start_interview(
        self,
        interview_id: str,
        schedule: InterviewSchedule,
        phase_transition_callback: callable
    ) -> None:
        """Start the interview timer and initialize phase tracking."""
        if interview_id in self.active_interviews:
            raise ValueError(f"Interview {interview_id} already exists")

        current_time = datetime.now()
        phase_states = []

        for phase_config in schedule.phases:
            phase_states.append(PhaseState(
                phase=phase_config.phase,
                start_time=current_time,
                end_time=current_time + timedelta(minutes=phase_config.duration_minutes)
            ))
            current_time += timedelta(minutes=phase_config.duration_minutes)

        self.active_interviews[interview_id] = {
            "schedule": schedule,
            "phase_states": phase_states,
            "current_phase_index": 0,
            "is_paused": False,
            "pause_start_time": None,
            "total_pause_duration": timedelta()
        }

        self.phase_transition_callbacks[interview_id] = phase_transition_callback

        # Start the phase monitoring task
        asyncio.create_task(self._monitor_phases(interview_id))

    async def get_current_phase(self, interview_id: str) -> Optional[PhaseState]:
        """Get the current phase of the interview."""
        if interview_id not in self.active_interviews:
            return None

        interview_data = self.active_interviews[interview_id]
        current_index = interview_data["current_phase_index"]
        
        if current_index >= len(interview_data["phase_states"]):
            return None

        return interview_data["phase_states"][current_index]

    async def get_phase_progress(self, interview_id: str) -> Dict[str, Any]:
        """Get the progress of the current phase."""
        current_phase = await self.get_current_phase(interview_id)
        if not current_phase:
            return {"message": "No active phase"}

        now = datetime.now()
        if self.active_interviews[interview_id]["is_paused"]:
            now = self.active_interviews[interview_id]["pause_start_time"]

        elapsed = now - current_phase.start_time
        total = current_phase.end_time - current_phase.start_time
        progress_percentage = (elapsed.total_seconds() / total.total_seconds()) * 100

        return {
            "phase": current_phase.phase,
            "elapsed_minutes": elapsed.total_seconds() / 60,
            "total_minutes": total.total_seconds() / 60,
            "progress_percentage": progress_percentage,
            "is_completed": current_phase.is_completed,
            "is_skipped": current_phase.is_skipped
        }

    async def handle_phase_transition(
        self,
        interview_id: str,
        force_transition: bool = False
    ) -> Dict[str, Any]:
        """Handle phase transition and return transition metadata."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")

        interview_data = self.active_interviews[interview_id]
        current_index = interview_data["current_phase_index"]
        current_phase = interview_data["phase_states"][current_index]

        # Mark current phase as completed
        current_phase.is_completed = True
        current_phase.actual_duration_minutes = (
            datetime.now() - current_phase.start_time
        ).total_seconds() / 60

        # Check if we should move to next phase
        if current_index + 1 < len(interview_data["phase_states"]):
            interview_data["current_phase_index"] += 1
            next_phase = interview_data["phase_states"][current_index + 1]
            
            # Notify about phase transition
            await self.phase_transition_callbacks[interview_id]({
                "from_phase": current_phase.phase,
                "to_phase": next_phase.phase,
                "was_forced": force_transition,
                "time_impact": self._calculate_time_impact(current_phase)
            })

            return {
                "success": True,
                "message": f"Transitioned from {current_phase.phase} to {next_phase.phase}",
                "time_impact": self._calculate_time_impact(current_phase)
            }
        else:
            return {
                "success": True,
                "message": "Interview completed",
                "time_impact": self._calculate_time_impact(current_phase)
            }

    async def pause_interview(self, interview_id: str) -> None:
        """Pause the interview timer."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")

        interview_data = self.active_interviews[interview_id]
        if not interview_data["is_paused"]:
            interview_data["is_paused"] = True
            interview_data["pause_start_time"] = datetime.now()

    async def resume_interview(self, interview_id: str) -> None:
        """Resume the interview timer."""
        if interview_id not in self.active_interviews:
            raise ValueError(f"Interview {interview_id} not found")

        interview_data = self.active_interviews[interview_id]
        if interview_data["is_paused"]:
            pause_duration = datetime.now() - interview_data["pause_start_time"]
            interview_data["total_pause_duration"] += pause_duration
            interview_data["is_paused"] = False
            interview_data["pause_start_time"] = None

    async def get_time_warnings(self, interview_id: str) -> Dict[str, Any]:
        """Get time warnings for the current phase."""
        current_phase = await self.get_current_phase(interview_id)
        if not current_phase:
            return {"message": "No active phase"}

        now = datetime.now()
        if self.active_interviews[interview_id]["is_paused"]:
            now = self.active_interviews[interview_id]["pause_start_time"]

        elapsed = now - current_phase.start_time
        total = current_phase.end_time - current_phase.start_time
        remaining = total - elapsed

        warnings = {
            "phase": current_phase.phase,
            "elapsed_minutes": elapsed.total_seconds() / 60,
            "remaining_minutes": remaining.total_seconds() / 60,
            "total_minutes": total.total_seconds() / 60,
            "is_running_late": elapsed > total,
            "is_almost_done": remaining.total_seconds() < 300  # 5 minutes
        }

        return warnings

    async def _monitor_phases(self, interview_id: str) -> None:
        """Monitor phases and handle transitions."""
        while True:
            try:
                current_phase = await self.get_current_phase(interview_id)
                if not current_phase:
                    break

                now = datetime.now()
                if self.active_interviews[interview_id]["is_paused"]:
                    now = self.active_interviews[interview_id]["pause_start_time"]

                if now >= current_phase.end_time:
                    await self.handle_phase_transition(interview_id)

                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error monitoring phases for interview {interview_id}: {e}")
                break

    def _calculate_time_impact(self, phase: PhaseState) -> Dict[str, Any]:
        """Calculate the time impact of a phase."""
        actual_duration = phase.actual_duration_minutes or 0
        planned_duration = (phase.end_time - phase.start_time).total_seconds() / 60
        time_difference = actual_duration - planned_duration

        return {
            "actual_duration_minutes": actual_duration,
            "planned_duration_minutes": planned_duration,
            "time_difference_minutes": time_difference,
            "is_over_time": time_difference > 0
        } 