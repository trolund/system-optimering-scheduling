from taskType import TaskType


class Task:
    
    def __init__(self, name: str, duration: int, period: int, type: TaskType, priority: int, deadline: int, et_subset=None, separation = 0, period_index = 0):
        self.name = name
        self.duration = duration
        self.period = period
        self.type = type
        self.priority = priority
        self.deadline = deadline
        self.release_time = 0
        self.et_subset = et_subset
        self.separation = separation
        self.period_index = period_index # used for neighborhood