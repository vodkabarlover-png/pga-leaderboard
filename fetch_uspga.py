import requests
import json

TOURNAMENT_ID = "R2026023"
CLEAN_ID = TOURNAMENT_ID[3:]
URL = f"https://statdata.pgatour.com/r/{CLEAN_ID}/leaderboard-v2.json"

def fetch_uspga():
    print("Fetching PGA Championship leaderboard...")

    players = []

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        players_raw = data.get("leaderboard", {}).get("players", [])

        for p in players_raw:
            rounds = p.get("rounds", [])
            players.append({
                "pos": p.get("current_position", ""),
                "name": f"{p['player_bio']['first_name']} {p['player_bio']['last_name']}",
                "r1": rounds[0]["strokes"] if len(rounds) > 0 else "",
                "r2": rounds[1]["strokes"] if len(rounds) > 1 else "",
                "r3": rounds[2]["strokes"] if len(rounds) > 2 else "",
                "r4": rounds[3]["strokes"] if len(rounds) > 3 else "",
                "total": p.get("total", "")
            })

    except Exception as e:
        print("USPGA API offline — writing empty file.")
        players = []

    with open("uspga.json", "w") as f:
        json.dump({"players": players}, f, indent=2)

    print("uspga.json updated successfully.")

if __name__ == "__main__":
    fetch_uspga()
