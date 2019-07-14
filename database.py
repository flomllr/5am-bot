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
    Returns the timezone saved for the user, if it exists or defaults to Berlin
    """
    def get_timezone(self, user_id):
        data = self.db.collection(u"users").document(user_id).get()
        data = data.to_dict()
        timezone = data.get("timezone", "Europe/Berlin") if data else "Europe/Berlin"
        return timezone

    """
    Returns the scores of all users
    """
    def get_scores(self, chat_id, week_id):
        scores = self.db.collection(u"chats").document(chat_id).collection(
            u"weeks").document(week_id).collection(u"users").get()

        scores_dict = {}
        for score in scores:
            score_dict = score.to_dict()
            scores_dict[score.id] = score_dict

        users = self.db.collection(u"users").get()
        users_dict = {}
        for user in users:
            user_dict = user.to_dict()
            result_dict = {
                "first_name": user_dict["first_name"],
                "last_name": user_dict["last_name"],
                "score": scores_dict[user.id].get("score", 0) if user.id in scores_dict else 0
            }

            users_dict[user.id] = result_dict

        return users_dict


    """
    Saves score by incrementing existing one or initializing
    Also saves a history of days where the user scored
    """
    def save_score(self, chat_id, week_id, user):
        # Save user to user collection
        data = {"first_name": user["first_name"] if user["firstname"] else "",
                "last_name": user["last_name"] if user["last_name"] else ""}
        user_id = str(user["id"])
        self.db.collection(u"users").document(user_id).set(data, merge=True)

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

    """
    Saves the given timezone for the user
    """
    def save_timezone(self, user_id, timezone):
        data = { "timezone": timezone }
        self.db.collection(u"users").document(user_id).set(data, merge=True)


