from bson import Binary

from Models.UserDTO import User
from bson import json_util

import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi import Response

from uuid import UUID, uuid4

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:password@localhost:27019/?authSource=admin")

# declare the database
database = client.fastapidb
collection = database.get_collection("users_collection")


async def fetch_one_user(user_id: UUID):
    binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
    document = await collection.find_one({"id": binary_uuid})
    if document:
        return {
            "id": user_id,
            "fullname": document['fullname'],
            "username": document['username'],
            "email": document['email'],
            "password": document['password'],
            "address": document['address']
        }
    return None


async def fetch_all_users():
    documents = []
    cursor = collection.find({})
    async for document in cursor:
        documents.append({
            "id": document['id'].hex(),
            "fullname": document['fullname'],
            "username": document['username'],
            "email": document['email'],
            "password": document['password'],
            "address": document['address']
        })
    return documents


async def create_user(user: User):
    user.id = user.id or uuid4()  # Generate a UUID if not provided
    document = user.dict()
    document['id'] = Binary.from_uuid(user.id)  # Convert UUID to bson.Binary
    await collection.insert_one(document)
    return document


async def update_user(user_id: UUID, data: dict):
    binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
    await collection.update_one({"id": binary_uuid}, {"$set": data})
    document = await collection.find_one({"id": binary_uuid})
    return {
        "id": user_id,
        "fullname": document['fullname'],
        "username": document['username'],
        "email": document['email'],
        "password": document['password'],
        "address": document['address']
    }


async def remove_user(user_id: UUID):
    binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
    await collection.delete_one({"id": binary_uuid})
    return True
