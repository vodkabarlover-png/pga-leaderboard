import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.espn.com/golf/leaderboard"

def parse_score(value):
    if value in ("", "-", "—", None):
        return None
    try:
        return int(value)
    except:
        return None

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    resp = requests.get(URL, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # ESPN embeds leaderboard JSON inside a <script> tag
    script_tags = soup.find_all("script")

    json_blob = None
    for tag in script_tags:
        if tag.string and "leaderboard" in tag.string.lower():
            json_blob = tag.string
            break

    if not json_blob:
        print("Could not locate embedded ESPN JSON")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    # Extract JSON object from inside JS
    match = re.search(r"window\.__espn_leaderboard\s*=\s*(\{.*?\});", json_blob, re.DOTALL)
    if not match:
        print("Could not extract ESPN JSON")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    data = json.loads(match.group(1))

    players = []

    # ESPN JSON structure: data["events"][0]["leaderboard"]
    leaderboard = data.get("events", [{}])[0].get("leaderboard", [])

    for p in leaderboard:
        players.append({
            "position": p.get("pos"),
            "name": p.get("athlete", {}).get("displayName"),
            "r1": parse_score(p.get("rounds", [{}])[0].get("score")),
            "r2": parse_score(p.get("rounds", [{}])[1].get("score")),
            "r3": parse_score(p.get("rounds", [{}])[2].get("score")),
            "r4": parse_score(p.get("rounds", [{}])[3].get("score")),
            "total": parse_score(p.get("total"))
        })

    with open("theopen.json", "w") as f:
        json.dump({"players": players}, f, indent=2)

if __name__ == "__main__":
    main()
