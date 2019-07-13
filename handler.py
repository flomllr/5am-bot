from pytz import timezone
from timezonefinder import TimezoneFinder
from database import DB

db = DB()
tf = TimezoneFinder()

def timezone_handler(user_id, latitude, longitude):
    timezone = tf.timezone_at(lng=longitude, lat=latitude)
    db.save_timezone(user_id, timezone)


def five_am_handler(chat, user, time):
    # Get user timezone and calculate current date
    user_id = str(user.id)
    tz = db.get_timezone(user_id)
    _date = time.astimezone(tz)
    hour = _date.hour
    minute = _date.minute
    print("Date:", _date)
    print("Hour:", hour)

    # Check if message arrived between 5am and 5:59 am
    if hour < 5:
        return "You're too early. Please send your update between 5:00 and 5:59."
    elif hour > 5:
        return "Dude, it's {}:{}. You're too late.".format(hour, minute)

    # Message arrived in the correct timeframe
    year, week, _ = _date.isocalendar()

    # Define ids
    chat_id = str(chat.id)
    week_id = "%s_%s" % (year, week)

    # Check if user woke up already
    history = db.get_history(chat_id, week_id, user_id)
    print(history)
    today = _date.strftime('%Y-%m-%d')
    if today in history:
        return "You can only wake up once per day."

    # Update the db
    score = db.save_score(chat_id, week_id, user)
    return "Nice! Your new score is %s of 3" % (score)
