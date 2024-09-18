from enum import Enum

class TaskStatus(str, Enum):
    complete = "完了"
    incomplete = "未完了"

class UserStatus(str, Enum):
    active = "活性"
    inactive = "非活性"