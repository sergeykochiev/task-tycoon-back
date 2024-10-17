from uuid import UUID
from pydantic import BaseModel


class TaskStats(BaseModel):
    competitors_count: int
    avg_result: float
    best_result: float
    total_attempts: int


class TaskStatsResultingResponse(BaseModel):
    user_initials: str
    best_result: float
    avg_result: float
    attempt_amount: int
    


class TaskStatsResponse(TaskStats):
    task_title: str
    task_id: UUID
    