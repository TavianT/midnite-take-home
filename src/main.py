import crud, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from process import check_withdrawal_over_one_hundred, check_three_consecutive_withdrawals

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
    print(f"Request: {event}")
    db_event = crud.create_event(db, event)
    alert = False
    alert_codes = []
    user_id = event.user_id

    func_response = check_withdrawal_over_one_hundred(event)
    if func_response[0] == True:
        alert = func_response[0]
        alert_codes.append(func_response[1])

    func_response = check_three_consecutive_withdrawals(db)
    
    return {
        "alert": alert,
        "alert_codes": alert_codes,
        "user_id": user_id
    }