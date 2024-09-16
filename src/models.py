from sqlalchemy import Column, Integer, String, Enum
from database import Base
from schemas import Types

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(Types))
    user_id = Column(Integer)
    amount = Column(String)
    time = Column(Integer)