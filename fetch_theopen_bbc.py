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

def extract_visible(cell):
    span = cell.find("span", {"aria-hidden": "true"})
    if span:
        return parse_score(span.get_text())
    return None

def main():
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # BBC changes class names daily — match ANY class containing "TableRowBody"
    rows = soup.find_all("tr", class_=lambda c: c and "TableRowBody" in c)

    players = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 11:
            continue

        position = cells[0].get_text(strip=True)

        name_span = cells[1].find("span", class_="ssrcss-1qmgl5j-FullName")
        name = name_span.get_text(strip=True) if name_span else cells[1].get_text(strip=True)

        r1 = extract_visible(cells[5])
        r2 = extract_visible(cells[6])
        r3 = extract_visible(cells[7])
        r4 = extract_visible(cells[8])
        total = extract_visible(cells[10])

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

    print(f"BBC Open leaderboard updated successfully with {len(players)} players.")

if __name__ == "__main__":
    main()
