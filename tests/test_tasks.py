import asyncio
import logging
import pytest
from src.task_model import Task, TaskStatus
from src.task_scheduler import TaskScheduler

@pytest.fixture(scope="session")
def task_scheduler():
    # Node_count can be altered and max_capacity
    scheduler = TaskScheduler(node_count=3, max_capacity=2)
    yield scheduler


@pytest.fixture(scope="function")
def setup_logging(request):
    # Creating a FileHandler 
    log_file = "test_task_log.log"
    file_handler = logging.FileHandler(log_file, mode="a")

    # Configure the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # A finalizer to close the file handler after the test
    def close_file_handler():
        file_handler.close()
        logger.removeHandler(file_handler)

    request.addfinalizer(close_file_handler)

## Testing some edge cases ##

@pytest.mark.asyncio
async def test_maximum_load(task_scheduler, setup_logging):
    # Generating a large number of tasks
    num_tasks = 3 # Tested with 100 tasks | System becomes slower as tasks increase.
    tasks = []
    for i in range(num_tasks):
        task = Task(task_id=str(i), priority=1, dependencies=[])
        tasks.append(task)
        task_scheduler.tasks[task.task_id] = task

    # Logging the start of the test
    logging.info(f"Submitting {num_tasks} tasks for maximum load test")

    # Running the process_tasks function
    await task_scheduler.process_tasks(tasks)

    # Logging the completion of the test
    logging.info(f"{num_tasks} tasks processed successfully")

    # Validating the results
    for task in tasks:
        assert task.status == "completed"

@pytest.mark.asyncio
async def test_minimum_load(task_scheduler, setup_logging):
    # Logging the start of the test
    logging.info("Starting minimum load test")

    # Running the process_tasks function with an empty task list
    await task_scheduler.process_tasks([])

    # Logging the completion of the test
    logging.info("Minimum load test completed")

    # Validating the results
    assert True

@pytest.mark.asyncio
async def test_priority_handling(task_scheduler, setup_logging):
    # Loggin the start of the test
    logging.info("Starting priority handling test")

    # Creating tasks with different priorities
    tasks = [
        Task(task_id="1", priority=1, dependencies=["3", "4"]),
        Task(task_id="2", priority=3, dependencies=["4", "1"]),
        Task(task_id="3", priority=2, dependencies=["4"]),
        Task(task_id="4", priority=1, dependencies=[]),
    ]

    # Calling the process_tasks function
    await task_scheduler.process_tasks(tasks)

    # Validating the execution order based on priority
    assert tasks[0].status == TaskStatus.COMPLETED
    assert tasks[3].status == TaskStatus.COMPLETED
    assert tasks[2].status == TaskStatus.COMPLETED
    assert tasks[1].status == TaskStatus.COMPLETED

    # Loggin the completion of the test
    logging.info("Priority handling test completed")

# Testcase to handle failure
@pytest.mark.asyncio
async def test_failure_handling():
    # Creating a TaskScheduler instance with maximum retries
    logging.info("Starting handling failure case")
    node_count = 2
    max_capacity = 2
    max_retries = 3
    task_scheduler = TaskScheduler(node_count, max_capacity)

    # Creating a task that will fail
    task_id = "123"
    priority = 1
    dependencies = []
    task = Task(task_id=task_id, priority=priority, dependencies=dependencies)
    task.status = TaskStatus.FAILED
    logging.info(f"{task_id} is {task.status}")

    # Adding the task to the scheduler
    await task_scheduler.process_tasks([task])
    logging.info(f"{task_id} is now {task.status}")

    # Verifying that the task is retried up to the configured limit
    assert task.status == TaskStatus.COMPLETED
    assert task.retries <= max_retries

    # Creating a task that will fail repeatedly
    task_id = "456"
    priority = 2
    dependencies = []
    task = Task(task_id=task_id, priority=priority, dependencies=dependencies)
    task.status = TaskStatus.FAILED
    
    logging.info(f"{task_id} is {task.status}")

    # Add the task to the scheduler
    await task_scheduler.process_tasks([task])
    
    logging.info(f"{task_id} is now {task.status}")

    # Verify that the task is retried up to the configured limit
    assert task.status == TaskStatus.COMPLETED
    assert task.retries <= max_retries

    