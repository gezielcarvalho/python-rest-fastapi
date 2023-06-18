from bson import Binary
from Models.UserDTO import UserDTO
import motor.motor_asyncio
from uuid import UUID, uuid4


class Model:

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://root:password@localhost:27019/?authSource=admin")
        # declare the database
        self.database = self.client.fastapidb
        self.collection = self.database.get_collection("users_collection")

    async def fetch_one_user(self, user_id: UUID):
        binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
        document = await self.collection.find_one({"id": binary_uuid})
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

    async def fetch_all_users(self):
        documents = []
        cursor = self.collection.find({})
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

    async def create_user(self, user: UserDTO):
        user.id = user.id or uuid4()  # Generate a UUID if not provided
        document = user.dict()
        document['id'] = Binary.from_uuid(user.id)  # Convert UUID to bson.Binary
        await self.collection.insert_one(document)
        return document

    async def update_user(self, user_id: UUID, data: dict):
        binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
        await self.collection.update_one({"id": binary_uuid}, {"$set": data})
        document = await self.collection.find_one({"id": binary_uuid})
        return {
            "id": user_id,
            "fullname": document['fullname'],
            "username": document['username'],
            "email": document['email'],
            "password": document['password'],
            "address": document['address']
        }

    async def remove_user(self, user_id: UUID):
        binary_uuid = Binary.from_uuid(user_id)  # Convert UUID to bson.Binary
        await self.collection.delete_one({"id": binary_uuid})
        return True
