import schemas
import crud
from sqlalchemy.orm import Session

def check_withdrawal_over_one_hundred(event: schemas.EventCreate):
    if event.type == "withdrawal" and float(event.amount) > 100:
        return True, 1100
    return False, None

def check_three_consecutive_withdrawals(user_id: int, db: Session):
    events = crud.get_last_three_user_events(db, user_id)
    withdrawal_found = []
    for event in events:
        if event.type == "withdrawal":
            withdrawal_found.append(True)
        else:
            withdrawal_found.append(False)