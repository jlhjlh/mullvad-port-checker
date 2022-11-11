import json
import os
import subprocess

from dotenv import load_dotenv
import requests

# set up in crontab
# /home/USER/mullvad-port-checker/venv/bin/python3 /home/USER/mullvad-port-checker/check-port.py >> output.log

###############################################
# initialize vars and get the script rolling!
###############################################

# load .env vars which contains my tokens
load_dotenv()
PUSHOVER_USER_TOKEN = os.getenv("PUSHOVER_USER_TOKEN")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
PORT = os.getenv("PORT")


result = subprocess.run(
    f"/usr/bin/docker exec qbittorrent curl -s https://am.i.mullvad.net/port/{PORT}",
    shell=True,
    stdout=subprocess.PIPE,
)
mullvad_response = json.loads(result.stdout)
print(mullvad_response)

if mullvad_response["reachable"] == False:
    print(f"Mullvad port {PORT} is closed.")
    
    url = "https://api.pushover.net/1/messages.json"
    params = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_TOKEN,
        "message": f"Mullvad port {PORT} is closed.",
    }

    pushover_response = requests.post(url, params=params)
    print(f"Response from Pushover: {pushover_response.text}")
