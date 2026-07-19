import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.cbssports.com/golf/leaderboard/the-open/"

def parse_score(value):
    value = value.strip()
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

    players = []

    # CBS uses a table with class "TableBase-table"
    table = soup.find("table", class_="TableBase-table")
    if not table:
        print("Could not locate CBS leaderboard table")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    tbody = table.find("tbody")
    if not tbody:
        print("CBS table found, but no tbody")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 8:
            continue

        # CBS column order:
        # 0 = POS
        # 1 = PLAYER
        # 2 = R1
        # 3 = R2
        # 4 = R3
        # 5 = R4
        # 6 = TOTAL
        # 7 = TODAY (ignored)

        position = cells[0].get_text(strip=True)
        name = cells[1].get_text(strip=True)

        r1 = parse_score(cells[2].get_text())
        r2 = parse_score(cells[3].get_text())
        r3 = parse_score(cells[4].get_text())
        r4 = parse_score(cells[5].get_text())
        total = parse_score(cells[6].get_text())

        players.append({
            "position": position,
            "name": name,
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "total": total
        })

    with open("theopen.json", "w") as f:
        json.dump({"players": players}, f, indent=2)

if __name__ == "__main__":
    main()