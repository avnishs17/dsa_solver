from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""
    content: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str


class CodeAnalysisRequest(BaseModel):
    """Code analysis request model."""
    code: str
    language: str = "python"


class CodeAnalysisResponse(BaseModel):
    """Code analysis response model."""
    time_complexity: str
    space_complexity: str
    quality_feedback: str
    bug_hints: str


class HintRequest(BaseModel):
    """Hint generation request model."""
    problem_statement: str


class HintResponse(BaseModel):
    """Hint response model."""
    hint: str
    test_cases: List[str]


class StudyPlanRequest(BaseModel):
    """Study plan request model."""
    timeline_weeks: str
    current_level: str
    target_goals: str


class StudyPlanResponse(BaseModel):
    """Study plan response model."""
    plan: str
