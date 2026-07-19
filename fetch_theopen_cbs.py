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

    # Find all leaderboard links
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()

        # Look for any Open Championship link
        if "open" in href and "leaderboard" in href:
            return "https://www.cbssports.com" + a["href"]

    return None

def scrape_open(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", class_="TableBase-table")

    if not table:
        return []

    tbody = table.find("tbody")
    if not tbody:
        return []

    players = []

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        players.append({
            "position": cells[0].get_text(strip=True),
            "name": cells[1].get_text(strip=True),
            "r1": parse_score(cells[2].get_text()),
            "r2": parse_score(cells[3].get_text()),
            "r3": parse_score(cells[4].get_text()),
            "r4": parse_score(cells[5].get_text()),
            "total": parse_score(cells[6].get_text())
        })

    return players

def main():
    open_url = find_open_url()

    if not open_url:
        print("Could not locate The Open URL on CBS")
        with open("theopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return

    print("Found Open URL:", open_url)

    players = scrape_open(open_url)

    with open("theopen.json", "w") as f:
        json.dump({"players": players}, f, indent=2)

    print("The Open leaderboard updated.")

if __name__ == "__main__":
    main()