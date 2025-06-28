from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Union

class MultiplicationRequest(BaseModel):
    """Schema for the multiplication request."""
    x: float = Field(..., description="First number to multiply")
    y: float = Field(..., description="Second number to multiply")

class TaskSubmitResponse(BaseModel):
    """Schema for the response when a task is submitted."""
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    """Schema for the response when checking a task's status."""
    task_id: str
    status: str
    result: Optional[float] = None
    error: Optional[str] = None
