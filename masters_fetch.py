import requests
import json
import time
import os

MASTERS_URL = "https://www.masters.com/en_US/scores/feeds/{year}/scores.json"
OUTPUT_FILE = "masters.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json,text/html",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.masters.com/",
}

def fetch_masters_json(year):
    url = MASTERS_URL.format(year=year)

    for attempt in range(5):
        try:
            print(f"Fetching Masters feed (attempt {attempt+1}/5)...")
            response = requests.get(url, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    print("Received non‑JSON response, retrying...")
            else:
                print(f"HTTP {response.status_code}, retrying...")

        except Exception as e:
            print(f"Error: {e}, retrying...")

        time.sleep(2)

    # Always return something
    return {"error": "Failed to fetch Masters leaderboard"}

def save_json(data, filename):
    print("DEBUG: Python working directory is:", os.getcwd())
    print(f"Saving file to: {os.getcwd()}/{filename}")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {filename}")

if __name__ == "__main__":
    year = time.localtime().tm_year
    masters_data = fetch_masters_json(year)
    save_json(masters_data, OUTPUT_FILE)
