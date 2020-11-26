from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from deta import Deta

deta = Deta()

users = deta.Base("fastapi-crud")

app = FastAPI()


class User(BaseModel):
    name: str
    age: int
    hometown: str


class UserUpdate(BaseModel):
    name: str = None
    age: int = None
    hometown: str = None

@app.get("/")
def read_root():
    return {"Hello": "There"}


@app.post("/users", status_code=201)
def create_user(user: User):
    u = users.put(user.dict())
    return u

@app.get("/users")
def list_users():
    us = next(users.fetch())
    return us

@app.get("/users/{uid}")
def get_user(uid: str):
    user = users.get(uid)
    if user:
        return user
    return JSONResponse({"message": "user not found"}, status_code=404)


@app.patch("/users/{uid}")
def update_user(uid: str, uu: UserUpdate):
    updates = {k:v for k,v in uu.dict().items() if v is not None}
    try:
        users.update(updates, uid)
        return users.get(uid)
    except Exception:
        return JSONResponse({"message": "user not found"}, status_code=404)


@app.delete("/users/{uid}")
def delete_user(uid: str):
    users.delete(uid)
    return
