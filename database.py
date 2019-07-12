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

    """
    Returns a user within given chat, week and user
    """
    def find_user(self, chat_id, week_id, user_id):
        data = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").document(user_id).get()
        return data.to_dict()

    """
    Returns a history given chat, week and user
    """
    def get_history(self, chat_id, week_id, user_id):
        data = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").document(user_id).get()
        data = data.to_dict()
        history = data.get("history", []) if data else []
        return history

    """
    Saves score by incrementing existing one or initializing
    Also saves a history of days where the user scored
    """
    def save_score(self, chat_id, week_id, user):
        # Save user to user collection
        data = {"first_name": user["first_name"],
                "last_name": user["last_name"]}
        user_id = str(user["id"])
        self.db.collection(u"users").document(user_id).set(data)

        # Increment score of user or start with one if it doesn't exist
        old = self.find_user(chat_id, week_id, user_id)
        old_score = old.get("score", 0) if old else 0
        new_score = {"score": old_score + 1}
        self.db.collection(u"chats").document(chat_id).collection(u"weeks").document(
            week_id).collection(u"users").document(user_id).set(new_score, merge=True)

        # Add today to user history and initialize history if user doesn't have one
        old = self.get_history(chat_id, week_id, user_id)
        tz = pytz.timezone("Europe/Berlin")
        today = datetime.now(tz).strftime('%Y-%m-%d')
        print(today)
        old_history = old["history"] if old and old["history"] else []
        print(old_history)
        old_history.append(today)
        new_history = {"history": old_history}
        print(new_history)
        self.db.collection(u"chats").document(chat_id).collection(u"weeks").document(
            week_id).collection(u"users").document(user_id).set(new_history, merge=True)

        # Return the new score
        return new_score["score"]
