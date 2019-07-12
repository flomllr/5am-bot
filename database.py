import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime
import pytz

import config


class DB(object):

    def __init__(self):
        cred = credentials.Certificate(config.SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def find_user(self, chat_id, week_id, user_id):
        data = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").document(user_id).get()
        return data.to_dict()

    def get_history(self, chat_id, week_id, user_id):
        data = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").document(user_id).get()
        history = data.to_dict()["history"]
        return history

    def save_score(self, chat_id, week_id, user):
        data = {"first_name": user["first_name"],
                "last_name": user["last_name"]}
        user_id = str(user["id"])
        self.db.collection(u"users").document(user_id).set(data)

        old = self.find_user(chat_id, week_id, user_id)
        old_score = old["score"] if old else 0
        new_score = {"score": old_score + 1}
        self.db.collection(u"chats").document(chat_id).collection(u"weeks").document(
            week_id).collection(u"users").document(user_id).set(new_score)

        old = self.get_history(chat_id, week_id, user_id)

        tz = pytz.timezone("Europe/Berlin")
        today = datetime.now(tz)
        old_history = old["history"] if old else today
        new_history = { "history": old_history.append(today)}
        self.db.collection(u"chats").document(chat_id).collection(u"weeks").document(
            week_id).collection(u"users").document(user_id).set(new_history)
