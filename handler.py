
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
    if hour < 11:
        return "You're too early. Please send your update between 5:00 and 5:59."
    elif hour > 11:
        return "Dude, it's {}:{}. You're too late.".format(hour, minute)

    # Message arrived in the correct timeframe
    year, week, _ = _date.isocalendar()

    # Update the db
    score = db.do_update_one(chat_id=str(chat.id), week_id="%s_%s" %
                             (year, week), user=user)
    return "Nice! Your new score is %s/3" % (score)
