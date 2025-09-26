# models/tasks.py

import time
from threading import Thread

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, func, *args, **kwargs):
        """
        Add a task to be executed asynchronously.
        """
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        self.tasks.append(thread)
        return thread

    def wait_all(self):
        """
        Wait for all tasks to complete.
        """
        for task in self.tasks:
            task.join()

# Example usage
if __name__ == "__main__":
    def sample_task(name, duration=2):
        print(f"Starting task: {name}")
        time.sleep(duration)
        print(f"Completed task: {name}")

    manager = TaskManager()
    manager.add_task(sample_task, "Task 1", duration=3)
    manager.add_task(sample_task, "Task 2", duration=2)
    manager.wait_all()
