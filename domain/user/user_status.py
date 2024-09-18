from enum import Enum

class UserStatus(str, Enum):
    active = "活性"
    inactive = "非活性"