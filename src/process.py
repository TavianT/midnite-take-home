import schemas
import crud
from sqlalchemy.orm import Session

def check_withdrawal_over_one_hundred(event: schemas.EventCreate):
    if event.type == "withdrawal" and float(event.amount) > 100:
        return True, 1100
    return False, None

def check_three_consecutive_withdrawals(user_id: int, db: Session):
    events = crud.get_last_three_user_events(db, user_id)
    if len(events) >= 3 and all(event.type == "withdrawal" for event in events):
        return True, 30
    return False, None

def check_three_consecutive_deposits_within_parameter(user_id: int, db: Session):
    events = crud.get_last_three_user_events(db, user_id)
    if len(events) >= 3 and all(event.type == "deposit" for event in events):
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