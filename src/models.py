import uuid

from sqlalchemy import Column, Integer, String
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    type = Column(String)
    user_id = Column(Integer)
    amount = Column(String)
    time = Column(Integer)