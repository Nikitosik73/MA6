from fastapi import FastAPI, HTTPException, status, Depends, Form
from typing import Annotated
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session
import random
from keycloak import KeycloakOpenID

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


# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

###########
#Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/get_token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def roulette_health():
    if (check_user_roles()):
        return {'message': 'service is active'}
    else:
        return "Wrong JWT Token"


@app.get("/deposit")
async def deposit(amount: int, db: db_dependency):
    if (check_user_roles()):
        global balance
        balance += amount
        return f"Your current balance is {balance}"
    else:
        return "Wrong JWT Token"


@app.get("/roll")
async def roll(sum: int, point: str, db: db_dependency):
    if (check_user_roles()):
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
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

