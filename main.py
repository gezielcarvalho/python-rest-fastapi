from uuid import uuid4
from fastapi import FastAPI, Response
from typing import List

from Models.User import User

db: List[User] = [
    User(id="7443a1e7-9ccd-4ea3-a5ed-187d6a14c82c", fullname="John Doe", username="johndoe", email="john@email.com", password="password",
         address="123 Main St."),
    User(id="6f59ab7d-a868-48a1-ab48-70c67b999841", fullname="Jane Doe", username="janedoe", email="jane@email.com", password="password",
         address="123 Main St.")
]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/users")
async def get_users():
    # declare variable with a copy of the db
    users = db[:]
    # remove the password from each user
    for user in users:
        # if field password exists, remove it
        if hasattr(user, "password"):
            delattr(user, "password")
    # return the users
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    # copy a user from the db where the id matches the user_id
    user = next((user for user in db if str(user.id) == user_id), None)
    # if the user exists
    if user:
        # remove the password from the user
        if hasattr(user, "password"):
            delattr(user, "password")
    # return the user
    return user


@app.post("/users", status_code=201)
async def create_user(user: User, response: Response):
    # add the user to the db
    db.append(user)
    # remove the password from the user
    if hasattr(user, "password"):
        delattr(user, "password")
    # return the user
    response.headers["Location"] = f"/users/{user.id}"
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    # copy a user from the db where the id matches the user_id
    user = next((user for user in db if str(user.id) == user_id), None)
    # if the user exists
    if user:
        # update the user
        user.fullname = user.fullname
        user.username = user.username
        user.email = user.email
        user.address = user.address
        user.password = user.password
        # remove the password from the user
        if hasattr(user, "password"):
            delattr(user, "password")
    # return the user
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: str, response: Response):
    # copy a user from the db where the id matches the user_id
    user = next((user for user in db if str(user.id) == user_id), None)
    # if the user exists
    if user:
        # remove the user from the db
        db.remove(user)
        response.status_code = 204
        return
    # return
    response.status_code = 404
    return {"message": "User not found"}
