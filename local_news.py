from src.extract_links import rss_process, notify_slack
from src.newspapers import news
import os
from dotenv import load_dotenv
load_dotenv()

for newspaper, value in news.items():
    url = value.get("url")
    county = value.get("county")
    filename = newspaper.replace(' ', '_').lower()

    print(f"Sjekker {newspaper}...")

    try:
        rss_process(url, newspaper, filename, county)
    
    except Exception as e:
        error = f"Feilmelding for {newspaper}: {e}"
        webhook = os.environ.get("WEBHOOK_ERROR")
        notify_slack(error, webhook)
        print(error)

print("[*] Ferdig med å sjekke lokalavisene.")