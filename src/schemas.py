from pydantic import BaseModel

class EventBase(BaseModel):
    type: str
    amount: str
    user_id: int
    time: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    class Config:
        orm_mode = True