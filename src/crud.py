from sqlalchemy import desc
import models, schemas
from sqlalchemy.orm import Session


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(type=event.type, user_id=event.user_id, amount=event.amount, time=event.time)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_last_three_user_events(db : Session, user_id: int):
    return db.query(models.Event).filter(models.Event.user_id == user_id).order_by(desc(models.Event.time)).limit(3).all()

def get_user_events(db : Session, user_id: int):
    return db.query(models.Event).filter(models.Event.user_id == user_id)

def get_last_user_event_time(db : Session, user_id: int):
    return db.query(models.Event.time).filter(models.Event.user_id == user_id).order_by(desc(models.Event.time)).all()

def get_total_deposited_in_thirty_second_window(db : Session, user_id: int, time: int):
    return db.query(models.Event.amount).filter(models.Event.user_id == user_id, models.Event.time > max(0, time - 30)).all()