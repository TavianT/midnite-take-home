import crud, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from process import check_withdrawal_over_one_hundred, check_three_consecutive_withdrawals, check_three_consecutive_deposits_within_parameter, check_total_amount_deposited_within_paramter, validation

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
    # Validate request
    validation(event, db)
    # Add event to database
    db_event = crud.create_event(db, event)
    alert = False
    alert_codes = []
    user_id = event.user_id

    # Check if the event type is withdrawal and amount is more than 100
    func_response = check_withdrawal_over_one_hundred(event)
    print(func_response)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    # Check if 3 withdrawals have been made in a row
    func_response = check_three_consecutive_withdrawals(user_id, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    # Check if 3 deposits have been made in a row with each greater than the last
    func_response = check_three_consecutive_deposits_within_parameter(user_id, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    # Check if total amount deposited in a 30 second windows is greater than 200
    func_response = check_total_amount_deposited_within_paramter(user_id, event.time, event.type.value, db)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])
    
    return {
        "alert": alert,
        "alert_codes": alert_codes,
        "user_id": user_id
    }