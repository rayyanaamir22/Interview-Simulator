"""
This module contains the DefaultInterviewSummarizer class, which is responsible for generating interview summaries.
"""

from typing import Dict, Any, List
from .conversation_manager import InterviewContext

class DefaultInterviewSummarizer:
    """Default implementation of interview summarization."""
    
    async def generate_summary(self, context: InterviewContext) -> Dict[str, Any]:
        """
        Generate a summary of the interview.
        
        Args:
            context: The interview context containing all responses and metadata
            
        Returns:
            Dict containing the interview summary
        """
        summary = {
            "interview_id": context.interview_id,
            "total_questions": context.current_question_index,
            "responses": context.responses,
            "implicit_thoughts": context.implicit_thoughts,
            "metadata": context.metadata
        }
        
        # Add overall assessment
        summary["overall_assessment"] = self._generate_overall_assessment(context)
        
        return summary
    
    def _generate_overall_assessment(self, context: InterviewContext) -> Dict[str, Any]:
        """Generate an overall assessment of the interview."""
        return {
            "completion_status": "complete" if context.state.value == "completed" else "incomplete",
            "total_responses": len(context.responses),
            "key_insights": self._extract_key_insights(context)
        }
    
    def _extract_key_insights(self, context: InterviewContext) -> List[str]:
        """Extract key insights from the interview."""
        insights = []
        
        # Add insights from implicit thoughts
        insights.extend(context.implicit_thoughts)
        
        # Add insights from responses
        for response in context.responses.values():
            if "sentiment" in response:
                sentiment = response["sentiment"]
                if sentiment.get("score", 0) < 0.3:
                    insights.append("Candidate showed signs of uncertainty in some responses")
                elif sentiment.get("score", 0) > 0.7:
                    insights.append("Candidate demonstrated confidence in responses")
        
        return insights 