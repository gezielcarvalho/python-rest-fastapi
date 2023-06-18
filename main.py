from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import UUID

from Models.UserDTO import User

db: List[User] = [
    User(id="7443a1e7-9ccd-4ea3-a5ed-187d6a14c82c", fullname="John Doe", username="johndoe", email="john@email.com", password="password",
         address="123 Main St."),
    User(id="6f59ab7d-a868-48a1-ab48-70c67b999841", fullname="Jane Doe", username="janedoe", email="jane@email.com", password="password",
         address="123 Main St.")
]

app = FastAPI()


from Core.Model import (
    fetch_one_user,
    fetch_all_users,
    create_user,
    update_user,
    remove_user
)


# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/users")
async def get_users():
    users = await fetch_all_users()
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    user = await fetch_one_user(user_id)
    return user


@app.post("/users", status_code=201)
async def add_user(user: User):
    await create_user(user)
    return user


@app.put("/users/{user_id}")
async def save_user(user_id: UUID, user_to_save: User, response: Response):
    user = await fetch_one_user(user_id)
    if user:
        update_data = user_to_save.dict(exclude_unset=True)
        updated_user = await update_user(user_id, update_data)
        return updated_user
    response.status_code = 404
    return {"message": "User not found"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, response: Response):
    user = await fetch_one_user(user_id)
    if user:
        await remove_user(user_id)
        return {"message": "User deleted successfully"}
    response.status_code = 404
    return {"message": "User not found"}
