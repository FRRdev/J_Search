import motor.motor_asyncio

from src.config.settings import MONGO_DB_URI, MONGO_DB_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)

database = client.get_database(MONGO_DB_NAME)
