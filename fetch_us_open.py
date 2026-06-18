import requests
import json

URL = "https://ace-api.usga.org/scoring/v1/leaderboard.json?championship=uso&championship-year=2026"

def fetch_us_open():
    try:
        data = requests.get(URL, timeout=10).json()
        players = data.get("standings", [])

        with open("usopen.json", "w") as f:
            json.dump({"players": players}, f, indent=2)

        print("U.S. Open leaderboard updated.")
    except Exception as e:
        print("Error fetching U.S. Open leaderboard:", e)

if __name__ == "__main__":
    fetch_us_open()