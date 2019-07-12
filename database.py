import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import config


class DB(object):

    def __init__(self):
        cred = credentials.Certificate(config.SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def do_find_one(self, chat_id, week_id, user_id):
        data = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").document(user_id).get()
        return data.to_dict()

    def do_update_one(self, chat_id, week_id, user):
        data = {"first_name": user["first_name"],
                "last_name": user["last_name"]}
        user_id = str(user["id"])
        self.db.collection(u"users").document(user_id).set(data)
        old = self.do_find_one(chat_id, week_id, user_id)
        old_score = old["score"] if old else 0
        new = {"score": old_score + 1}
        self.db.collection(u"chats").document(chat_id).collection(u"weeks").document(
            week_id).collection(u"users").document(user_id).set(new)
        return new["score"]
