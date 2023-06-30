
import asyncio
from typing import List, Dict
from src.task_model import TaskStatus
import logging

class TaskScheduler:
    def __init__(self, node_count: int, max_capacity: int):
        self.node_count = node_count
        self.max_capacity = max_capacity
        self.nodes = {node_id: max_capacity for node_id in range(1, node_count + 1)}
        self.tasks: Dict[str, "Task"] = {}

    # Config for logging file
    logging.basicConfig(filename='task_log.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    async def process_task(self, task_id: str):
        if task_id not in self.tasks:
            logging.error(f'Task ID: {task_id} does not exist.')
            return
        task = self.tasks[task_id]
        # Simulating the execution of the task asynchronously
        await asyncio.sleep(2)
        task.status = TaskStatus.COMPLETED
        logging.info(f'Task ID: {task_id} completed.')

    async def process_tasks(self, tasks: List["Task"]):
        for task in tasks:
            self.tasks[task.task_id] = task
            logging.info(f'Task ID: {task.task_id} is being processed.')

        # Sorting tasks by priority (higher priority first)
        tasks.sort(key=lambda t: t.priority)

        # Processing tasks in parallel, considering dependencies and available nodes
        for task in tasks:
            try:
                await self.process_task_with_dependencies(task)
            except KeyError as e:
                logging.error(f'Error processing Task ID: {task.task_id} - {str(e)}')
            

    async def process_task_with_dependencies(self, task: "Task"):
        dependencies = task.dependencies

        for dep in dependencies:
            if dep not in self.tasks:
                logging.error(f'Task ID: {task.task_id} depends on non-existent task ID: {dep}.')
                return
        # Waiting for other tasks to be completed
        await asyncio.gather(*[self.process_task_with_dependencies(self.tasks[dep]) for dep in dependencies])

        # Find an available node to execute the task
        node_id = self.find_available_node()
        if node_id:
            self.nodes[node_id] -= 1
            task.status = TaskStatus.RUNNING
            logging.info(f'Task {task.task_id} started on Node {node_id}')
            await self.process_task(task.task_id)
            logging.info(f'Task {task.task_id} completed on Node {node_id}')
            self.nodes[node_id] += 1

    # Finding available to node to run the task
    def find_available_node(self) -> int:
        for node_id, capacity in self.nodes.items():
            if capacity > 0:
                return node_id
        return 0