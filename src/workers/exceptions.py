from typing import Optional


class TaskManagerNotInitializedError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "not initialized 'TaskManager' in worker"

        super().__init__(message)


class SchedulerNotInitializedError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "not initialized 'Scheduler' in worker"

        super().__init__(message)


class ContainerNotInitializedError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "not initialized 'container' in 'TaskManager'"

        super().__init__(message)
