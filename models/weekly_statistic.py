import datetime

from database import DB

class WeeklyStatistic(object):

    def __init__(self, users, pot):
        self.users = users
        self.pot = pot
        self.created_at = datetime.datetime.utcnow()

    def insert(self):
        weekly_statistic_exists = await DB.do_find_one("5am", {"created_at": self.created_at})
        if not weekly_statistic_exists:
            DB.do_insert_one(collection="5am", data=self.json())

    def json(self):
        return {
            'users': [user.json() for user in self.users],
            'pot': self.pot,
            'created_at': self.created_at
        }
