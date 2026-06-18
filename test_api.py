import requests

url = "https://feeds.theopen.com/leaderboard/leaderboard.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/json,text/html,*/*",
    "Referer": "https://www.theopen.com/",
    "Accept-Language": "en-GB,en;q=0.9",
    "Cache-Control": "no-cache",
}

r = requests.get(url, headers=headers)
print("Status:", r.status_code)
print("Preview:", r.text[:500])