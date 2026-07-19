import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.bbc.co.uk/sport/golf/leaderboard"
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

def main():
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # BBC rows use this class:
    rows = soup.find_all("tr", class_="ssrcss-1if37cu-TableRowBody")

    players = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 11:
            continue

        position = cells[0].get_text(strip=True)

        # Full name is inside <span class="ssrcss-1qmgl5j-FullName">
        name_span = cells[1].find("span", class_="ssrcss-1qmgl5j-FullName")
        name = name_span.get_text(strip=True) if name_span else cells[1].get_text(strip=True)

        r1 = parse_score(cells[5].get_text())
        r2 = parse_score(cells[6].get_text())
        r3 = parse_score(cells[7].get_text())
        r4 = parse_score(cells[8].get_text())
        total = parse_score(cells[10].get_text())

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

    print("BBC Open leaderboard updated successfully.")

if __name__ == "__main__":
    main()