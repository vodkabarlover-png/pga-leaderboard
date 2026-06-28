import requests
import json

URL = "https://www.theopen.com/api/leaderboard"

def fetch_theopen():
    print("Fetching The Open leaderboard...")

    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()

        players_raw = data.get("Leaderboard", {}).get("Players", [])
        players = []

        for p in players_raw:
            players.append({
                "pos": p.get("Position", ""),
                "name": f"{p.get('FirstName', '')} {p.get('LastName', '')}",
                "r1": p.get("Round1", ""),
                "r2": p.get("Round2", ""),
                "r3": p.get("Round3", ""),
                "r4": p.get("Round4", ""),
                "total": p.get("Total", "")
            })

        with open("theopen.json", "w") as f:
            json.dump({"players": players}, f, indent=2)

        print("theopen.json updated successfully.")

    except Exception as e:
        print("Error fetching The Open leaderboard:", e)

if __name__ == "__main__":
    fetch_theopen()