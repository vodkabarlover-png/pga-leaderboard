import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.espn.com/golf/leaderboard"

def parse_score(value):
    if value in ("", "-", "—", None):
        return None
    try:
        return int(value)
    except:
        return None

def main():
    headers = {
        "User-Agent": "Mozilla