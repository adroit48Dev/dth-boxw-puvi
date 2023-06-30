from typing import List, Dict
from fastapi import FastAPI, HTTPException

from src.task_scheduler import TaskScheduler
from src.task_model import Task

app = FastAPI()
scheduler = TaskScheduler(node_count=3, max_capacity=2)


@app.get('/')
def root():
    return {"message": "Task Scheduler is working.."}

@app.post("/schedule")
async def schedule_tasks(tasks: List[Task]):
    # Validating the incoming JSON data against the TaskCreate model
    validated_tasks = [Task(**task.dict()) for task in tasks]

    try:
        await scheduler.process_tasks(validated_tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Tasks are being processed", "tasks": [task.dict() for task in validated_tasks]}

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    task = scheduler.tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": task.status}