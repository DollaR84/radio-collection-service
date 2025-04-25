from typing import Optional


class TaskManagerNotInitializedError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "not initialized task manager in worker"

        super().__init__(message)
