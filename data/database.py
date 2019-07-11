import motor
from motor import motor_asyncio

mongo_username =
database_client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://admin:admin123@5am-cluster-grwhk.gcp.mongodb.net/test?retryWrites=true&w=majority")
