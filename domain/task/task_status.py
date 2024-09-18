from enum import Enum

class TaskStatus(str, Enum):
    complete = "完了"
    incomplete = "未完了"