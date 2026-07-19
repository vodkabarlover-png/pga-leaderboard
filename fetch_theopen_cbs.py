import requests
from bs4 import BeautifulSoup
import json

INDEX_URL = "https://www.cbssports.com/golf/leaderboard/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def parse_score(v):
    v = v.strip()
    if v in ("", "-", "—"):
        return None
    try:
        return int(v)
    except:
        return None

def find_open_url():
    resp = requests.get(INDEX_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if "open" in href and "leaderboard" in href:
            return "https://www.cbssports.com" + a["href"]

    return None

def main():
    open_url = find_open_url()

    if not open_url:
        print("Could not locate The Open URL on CBS")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    print("Found Open URL:", open_url)

    resp = requests.get(open_url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
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

    players = []

    # CBS uses this class for ALL leaderboard rows (expanded + collapsed)
    rows = tbody.find_all("tr", class_="GolfLeaderboard-bodyTr")

    for row in rows:
        cells = row.find_all("td")

        # Skip toggle-only rows
        if len(cells) < 12:
            continue

        position = cells[1].get_text(strip=True)

        # Extract long player name
        name_cell = cells[3]
        long_name = name_cell.find("span", class_="CellPlayerName--long")
        if long_name:
            name = long_name.get_text(strip=True)
        else:
            name = name_cell.get_text(strip=True)

        r1 = parse_score(cells[7].get_text())
        r2 = parse_score(cells[8].get_text())
        r3 = parse_score(cells[9].get_text())
        r4 = parse_score(cells[10].get_text())
        total = parse_score(cells[11].get_text())

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

    print("The Open leaderboard updated successfully.")

if __name__ == "__main__":
    main()
