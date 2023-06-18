from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from Models.UserDTO import UserDTO
import Core.Model as Model
import App.User as App
from dotenv import load_dotenv
load_dotenv()


# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

model = Model.Model()

user = App.User()


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/users")
async def get_users():
    users = await user.fetch_all_users()
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    response = await user.fetch_one_user(user_id)
    if response:
        return response
    raise HTTPException(status_code=404, detail="Users not found")


@app.post("/users", status_code=201)
async def add_user(user_to_add: UserDTO):
    response = await user.create_user(user_to_add)
    if response:
        return user_to_add
    raise HTTPException(status_code=400, detail="Bad request")


@app.put("/users/{user_id}")
async def save_user(user_id: UUID, user_to_save: UserDTO):
    response = await user.fetch_one_user(user_id)
    if response:
        update_data = user_to_save.dict(exclude_unset=True)
        updated_user = await user.update_user(user_id, update_data)
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    response = await user.fetch_one_user(user_id)
    if user:
        await user.remove_user(user_id)
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
