import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://www.theopen.com/leaderboard"

def fetch_open():
    print("Fetching The Open leaderboard...")

    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    players = []

    rows = soup.select(".leaderboard-player")
    for row in rows:
        name = row.select_one(".player-name")
        pos = row.select_one(".player-position")
        score = row.select_one(".player-score")
        today = row.select_one(".player-today")
        thru = row.select_one(".player-thru")
        tee = row.select_one(".player-tee-time")

        players.append({
            "name": name.text.strip() if name else None,
            "position": pos.text.strip() if pos else None,
            "score": score.text.strip() if score else None,
            "today": today.text.strip() if today else None,
            "thru": thru.text.strip() if thru else None,
            "tee_time": tee.text.strip() if tee else None
        })

    data = {
        "tournament": "The Open Championship",
        "round": None,
        "players": players
    }

    with open("Leaderboard.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Updated Leaderboard.json")

while True:
    try:
        fetch_open()
    except Exception as e:
        print("Error:", e)
    time.sleep(300)
