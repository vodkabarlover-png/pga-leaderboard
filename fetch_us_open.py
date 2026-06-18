import cloudscraper
from bs4 import BeautifulSoup
import json
import time

URL = "https://www.usopen.com/scoring.html"

def parse_score(value):
    value = value.strip().upper()
    if value in ("E", "EVEN", ""):
        return 0
    try:
        return int(value)
    except:
        return None

def fetch_us_open():
    print("Fetching U.S. Open leaderboard...")

    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )

    html = scraper.get(URL).text
    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table")

    # ALWAYS WRITE A FILE
    if not table:
        print("Leaderboard not available yet — writing empty file.")
        with open("usopen.json", "w") as f:
            json.dump({"players": []}, f, indent=2)
        return False

    rows = table.find_all("tr")
    leaderboard = []

    for row in rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 6:
            continue

        leaderboard.append({
            "pos": cols[0],
            "name": cols[1],
            "r1": parse_score(cols[3]),
            "r2": parse_score(cols[4]),
            "r3": parse_score(cols[5]),
            "r4": parse_score(cols[6]) if len(cols) > 6 else None,
            "total": parse_score(cols[7]) if len(cols) > 7 else None
        })

    with open("usopen.json", "w") as f:
        json.dump({"players": leaderboard}, f, indent=2)

    print("Updated usopen.json")
    return True

# Loop every 5 minutes
while True:
    try:
        fetch_us_open()
    except Exception as e:
        print("Unexpected error:", e)
    time.sleep(300)