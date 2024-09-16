from enum import Enum
from pydantic import BaseModel


class Types(Enum):
    withdrawal = "withdrawal"
    deposit = "deposit"

class EventBase(BaseModel):
    type: Types
    amount: str
    user_id: int
    time: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    class Config:
        orm_mode = True