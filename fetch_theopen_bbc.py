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
    """
    BBC puts two spans in each score cell:
    <span class='visually-hidden'>72</span>
    <span aria-hidden='true'>72</span>

    We ONLY want the visible one.
    """
    span = cell.find("span", {"aria-hidden": "true"})
    if span:
        return parse_score(span.get_text())
    return None

def main():
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # BBC leaderboard rows
    rows = soup.find_all("tr", class_="ssrcss-1if37cu-TableRowBody")

    players = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 11:
            continue

        # Position
        position = cells[0].get_text(strip=True)

        # Full name
        name_span = cells[1].find("span", class_="ssrcss-1qmgl5j-FullName")
        name = name_span.get_text(strip=True) if name_span else cells[1].get_text(strip=True)

        # Round scores (visible only)
        r1 = extract_visible
