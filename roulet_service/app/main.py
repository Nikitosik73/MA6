from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from uuid import UUID
from model.user import User
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session
import random

app = FastAPI()

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

balance = 0

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def roulet_health():
    return {'message': 'service is active'}


@app.get("/deposit")
async def deposit(amount: int, db: db_dependency):
    global balance
    balance += amount
    return f"Your current balance is {balance}"


@app.get("/roll")
async def roll(sum: int, point: str, db: db_dependency):
    global balance
    if sum > balance:
        raise HTTPException(
            status_code=404,
            detail=f'You dont have enough money, ur current balance: {balance}'
        )
    if point != "red" and point != "black" and point != "green":
        raise HTTPException(
            status_code=404,
            detail=f'u cant choose this point'
        )
    result = random.random(0, 36)
    if result == 0 and point == "green":
        balance += (sum * 10)
    elif (result % 2 == 0 and point == "black") or (result % 2 == 1 and point == "red"):
        balance += sum
    else:
        balance -= sum
        print("Ha-ha, loser")
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

