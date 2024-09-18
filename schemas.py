from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Union
import phonenumbers

from domain.user.user_status import UserStatus
from domain.task.task_status import TaskStatus

class UserBase(BaseModel):
    name: str
    user_status: UserStatus
    email: EmailStr
    phone: str

    @field_validator("phone")
    def validate_phone(cls, v):
        try:
            number = phonenumbers.parse(v, "JP")
            if not phonenumbers.is_valid_number(number):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(
                number, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("NumberParseException")


class TaskBase(BaseModel):
    name: str
    task_status: TaskStatus = TaskStatus.incomplete
    owner_id: int
    due_date: datetime
    delays: int


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    tasks: List[TaskResponse]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    user_status: Union[UserStatus, None] = None
    email: Union[EmailStr, None] = None
    phone: Union[str, None] = None


class TaskUpdate(BaseModel):
    name: Union[str, None] = None
    task_status: Union[TaskStatus, None] = None
