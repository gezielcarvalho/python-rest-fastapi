from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from Models.UserDTO import UserDTO
import Core.Model as Model
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

@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/users")
async def get_users():
    users = await model.fetch_all_users()
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    user = await model.fetch_one_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Users not found")


@app.post("/users", status_code=201)
async def add_user(user: UserDTO):
    response = await model.create_user(user)
    if response:
        return user
    raise HTTPException(status_code=400, detail="Bad request")


@app.put("/users/{user_id}")
async def save_user(user_id: UUID, user_to_save: UserDTO, response: Response):
    user = await model.fetch_one_user(user_id)
    if user:
        update_data = user_to_save.dict(exclude_unset=True)
        updated_user = await model.update_user(user_id, update_data)
        return updated_user
    response.status_code = 404
    return {"message": "User not found"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, response: Response):
    user = await model.fetch_one_user(user_id)
    if user:
        await model.remove_user(user_id)
        return {"message": "User deleted successfully"}
    response.status_code = 404
    return {"message": "User not found"}
