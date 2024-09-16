from sqlalchemy import Column, Integer, String
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    user_id = Column(Integer)
    amount = Column(String)
    time = Column(Integer)