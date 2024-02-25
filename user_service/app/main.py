from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from uuid import UUID
from model.user import User
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session

app = FastAPI()

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def user_health():
    return {'message': 'service is active'}


@app.get("/get_users")
async def get_users(db: db_dependency):
    result = db.query(database.User).offset(0).limit(100).all()
    return result


@app.get("/get_user_by_id")
async def get_user_by_id(user_id: UUID, db: db_dependency):
    result = db.query(database.DBDoc).filter(database.DBDoc.owner_id == user_id).first()
    print(user_id)
    print(result)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'user with such owner id is not found. user_id: {user_id}'
        )
    return result


@app.post('/add_user')
async def add_doc(user: User, db: db_dependency):
    db_user = database.DBDoc(
        id=user.id,
        name=user.name,
        second_name=user.second_name,
        dick_size=user.dick_size,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "Success"


@app.delete("/delete_user")
async def delete_doc(user_id: UUID, db: db_dependency):
    try:
        user_db = db.query(database.DBDoc).filter(database.DBDoc.id == user_id).first()
        db.delete(user_db)
        db.commit()
        return "Success"
    except Exception:
        return "cant find user"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

