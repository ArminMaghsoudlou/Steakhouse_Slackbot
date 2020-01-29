import yaml
import tinydb
import threading
import time
import os

from rtmbot import RtmBot

DB_FILE = '..\\team-auth\\teams.json'
db_last_changed = ''


def db_check_for_change():
    global db_last_changed
    change_time = os.path.getmtime(DB_FILE)
    if db_last_changed != change_time:
        db_last_changed = change_time
        return db_last_changed

    return False

def start_bot(token):
    print("Starting bot for token: {}".format(token))
    config = {
        "DEBUG": True,
        "SLACK_TOKEN": token,
        "ACTIVE_PLUGINS": ["plugins.runner.FeedsparqPlugin"],
        "FeedsparqPlugin": {"DEBUG": True}
    }
    print("The config file: {}".format(config))
    bot = RtmBot(config)
    bot.start()


def get_tokens_from_db():
    db = tinydb.TinyDB(DB_FILE)
    teams = db.all()
    db_check_for_change()
    return teams



# start_bot(teams[0]["bot_access_token"])
threads = {}
while True:
    time.sleep(1)
    # print("Slept for a sec")
    if db_check_for_change():
        # print("DB file has changed, starting new bots")
        teams = get_tokens_from_db()
        for team in teams:
            print("Starting bot for team: {}".format(team["name"]))
            threads[team["id"]] = threading.Thread(target=start_bot, args=(team["bot_access_token"],))
            threads[team["id"]].daemon = True
            threads[team["id"]].start()
    else:
        pass
        # print("No change in DB file - sleeping some more")




    
