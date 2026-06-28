import requests
import json
import time

URL = "https://www.theopen.com/api/leaderboard"

def fetch_open():
    print("Fetching The Open leaderboard...")

    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()

    with open("Leaderboard.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Updated The open.json")

while True:
    try:
        fetch_open()
    except Exception as e:
        print("Error:", e)
    time.sleep(300)