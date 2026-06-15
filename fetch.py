import requests
import json
import time

URL = "https://statdata.pgatour.com/r/current/leaderboard-v2.json"

while True:
    print("Fetching leaderboard...")
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()

    with open("Leaderboard.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Updated Leaderboard.json")
    time.sleep(300)  # 5 minutes