```markdown
# Task Scheduler

The Task Scheduler is a system designed to manage and execute tasks in a distributed environment. It provides a scalable and efficient way to process tasks while considering their priorities and dependencies.

## Features

- Submit tasks with priority and dependencies
- Parallel processing of tasks based on available nodes
- Automatic scheduling of tasks based on priority levels
- Failure handling and error logging
- Scalable and configurable based on the number of nodes and maximum capacity

## Installation

1. Clone the repository:

```bash
git clone 
cd task-scheduler
```
2. Create Virtual environment
    ```bash
    pipenv shell
    ```

2. Install the required dependencies:

```bash
pipenv install -r requirements.txt
```
3. Run the server

```bash
uvicorn src.main:app --reload (--port 8000 |optional)
```
## Docker Setup
```bash
docker build .
or
docker-compose up
```

## Usage


1. Create an instance of the `TaskScheduler` class:

```python
node_count = 4
max_capacity = 2
scheduler = TaskScheduler(node_count, max_capacity)
```

3. Project tree:
~~~
.
├── notes.txt
├── readme.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── task_model.py
│   └── task_scheduler.py
├── task_log.log
├── task.txt
├── tests
│   ├── __init__.py
│   └── test_tasks.py
└── test_task_log.log
~~~
5. Monitor the execution progress and task logs:

```bash
tail -f task_log.log
```

## License

This project is for personal testing purpose not for production use
```

