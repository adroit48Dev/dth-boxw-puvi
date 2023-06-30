
from typing import List, Union
from enum import Enum
from pydantic import BaseModel

class TaskStatus(str, Enum):
    NOT_STARTED = "not started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Task model
class Task(BaseModel):
    # Required fields
    task_id: str
    priority: int
    dependencies: List[str] 
    # Not Mandatory
    status: TaskStatus = TaskStatus.NOT_STARTED # default task status
    retries: int = 0
