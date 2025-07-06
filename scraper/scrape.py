import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

START_URL = "https://mosdac.gov.in/"
MAX_DEPTH = 2

visited = set()
results = []

def is_valid(url):
    parsed = urlparse(url)
    return parsed.netloc == "mosdac.gov.in"

def scrape(url, depth):
    if depth > MAX_DEPTH or url in visited:
        return
    print(f"Scraping: {url}")
    visited.add(url)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed: {url} — {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # safer title extraction
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = "Untitled"

    text = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

    if len(text) > 100:
        results.append({
            "url": url,
            "title": title,
            "text": text
        })

    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if is_valid(next_url):
            scrape(next_url, depth + 1)

# Run crawler
scrape(START_URL, 0)

# Save results
with open("mosdac_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
    
print(f"\n Saved {len(results)} pages to mosdac_data.json")

