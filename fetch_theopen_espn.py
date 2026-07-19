import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.espn.co.uk/golf/leaderboard"

def parse_score(value):
    value = value.strip()
    if value in ("", "-", "—"):
        return None
    try:
        return int(value)
    except ValueError:
        return None

def main():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    players = []

    # ESPN uses a table with class "Table__TBODY"
    tbody = soup.find("tbody", class_="Table__TBODY")
    if not tbody:
        print("Could not locate ESPN leaderboard table")
        data = {"players": []}
    else:
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 8:
                continue

            # ESPN column order:
            # 0 = POS
            # 1 = PLAYER
            # 2 = TODAY
            # 3 = THRU
            # 4 = R1
            # 5 = R2
            # 6 = R3
            # 7 = R4
            # 8 = TOTAL (sometimes 7 if R4 missing)

            position = cells[0].get_text(strip=True)
            name = cells[1].get_text(strip=True)

            r1 = parse_score(cells[4].get_text())
            r2 = parse_score(cells[5].get_text())
            r3 = parse_score(cells[6].get_text())
            r4 = parse_score(cells[7].get_text())

            # TOTAL may be at index 8 if present
            total = None
            if len(cells) > 8:
                total = parse_score(cells[8].get_text())

            players.append({
                "position": position,
                "name": name,
                "r1": r1,
                "r2": r2,
                "r3": r3,
                "r4": r4,
                "total": total
            })

        data = {"players": players}

    with open("theopen.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()