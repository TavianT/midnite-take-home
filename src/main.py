import crud, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from process import check_withdrawal_over_one_hundred, check_three_consecutive_withdrawals, check_three_consecutive_deposits_within_parameter, check_total_amount_deposited_within_paramter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/event")
def post_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    # Add event to database
    event_times = crud.get_last_user_event_time(db, event.user_id)[0]
    if any(event.time <= event_time for event_time in event_times):
        raise HTTPException(status_code=400, detail=f"event time must be greater than the last event time")

    db_event = crud.create_event(db, event)
    alert = False
    alert_codes = []
    user_id = event.user_id

    func_response = check_withdrawal_over_one_hundred(event)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    func_response = check_three_consecutive_withdrawals(user_id, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    func_response = check_three_consecutive_deposits_within_parameter(user_id, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    func_response = check_total_amount_deposited_within_paramter(user_id, event.time, event.type, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])
    
    return {
        "alert": alert,
        "alert_codes": alert_codes,
        "user_id": user_id
    }