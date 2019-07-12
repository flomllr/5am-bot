import motor
import config
from motor import motor_asyncio


class DB(object):
    @staticmethod
    def init():
        client = motor.motor_asyncio.AsyncIOMotorClient(
            config.ATLAS_CONNECTION)
        database = client['5am-db']

    @staticmethod
    async def do_insert_one(self, collection, data):
        await self.database.client[collection].insert_one(data)

    @staticmethod
    async def do_find_one(self, collection, query):
        data = await self.database.client[collection].find_one(query)
        return data
