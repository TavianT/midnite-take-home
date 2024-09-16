import schemas
import crud
from sqlalchemy.orm import Session
from fastapi import HTTPException

def validation(event: schemas.EventCreate, db: Session):
    event_times = crud.get_last_user_event_time(db, event.user_id)
    # Check if event time is less than any event time already in the DB
    if len(event_times) > 0:
        event_times = event_times[0]
    if any(event.time <= event_time for event_time in event_times):
        raise HTTPException(status_code=400, detail=f"event time must be greater than the last event time")
    # Check can actually be converted to a number
    try:
        float(event.amount)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"event amount must be castable to a float")

def check_withdrawal_over_one_hundred(event: schemas.EventCreate):
    print(event)
    if event.type.value == "withdrawal" and float(event.amount) > 100:
        return True, 1100
    return False, None

def check_three_consecutive_withdrawals(user_id: int, db: Session):
    events = crud.get_last_three_user_events(db, user_id)
    if len(events) >= 3 and all(event.type.value == "withdrawal" for event in events):
        return True, 30
    return False, None

def check_three_consecutive_deposits_within_parameter(user_id: int, db: Session):
    events = crud.get_last_three_user_events(db, user_id)
    if len(events) >= 3 and all(event.type.value == "deposit" for event in events):
        print(events[0].amount)
        print(events[1].amount)
        print(events[2].amount)
        if events[0].amount > events[1].amount and events[1].amount > events[2].amount:
            return True, 300
    return False, None

def check_total_amount_deposited_within_paramter(user_id: int, time: int, type: str, db: Session):
    if type == "deposit":
        amounts = crud.get_total_deposited_in_thirty_second_window(db, user_id, time)
        total = 0
        for amount in amounts:
            total += float(amount[0])
        if total > 200:
            return True, 123
    return False, None