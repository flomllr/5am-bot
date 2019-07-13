
from datetime import datetime
from pytz import timezone
from database import DB

db = DB()


def five_am_handler(chat, user, time):
    print(chat, user, time)
    tz = timezone("Europe/Berlin")
    _date = time.astimezone(tz)
    hour = _date.hour
    minute = _date.minute
    print("Date:", _date)
    print("Hour:", hour)

    # Check if message arrived between 5am and 5:59 am
    if hour < 5:
        return "You're too early. Please send your update between 5:00 and 5:59."
    elif hour > 5:
        return "Dude, it's {}:{:0>2}. You're too late.".format(hour, minute)

    # Message arrived in the correct timeframe
    year, week, _ = _date.isocalendar()

    # Define ids
    chat_id = str(chat.id)
    week_id = "%s_%s" % (year, week)
    user_id = str(user.id)

    # Check if user woke up already
    history = db.get_history(chat_id, week_id, user_id)
    print(history)
    today = _date.strftime('%Y-%m-%d')
    if today in history:
        return "You can only wake up once per day."

    # Update the db
    score = db.save_score(chat_id, week_id, user)
    return "Nice! Your new score is %s of 3" % (score)
