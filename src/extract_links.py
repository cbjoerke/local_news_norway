import feedparser
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_old_links(filename):
    with open(f"data/{filename}.json", "r") as f:
        data = json.load(f)
    return data["links"]

def fetch_new_links(url, newspaper):
    rss = feedparser.parse(url)
    data = {
        "newspaper" : newspaper,
        "links" : [],
    }
    for entry in rss["entries"]:
        link = entry["link"]
        data["links"].append(link)
    return data

def check_updates(old_links, new_links):
    links = [link for link in new_links["links"] if link not in old_links]
    return links

def notify_slack(links, county):
    if county == "Østfold":
        webhook = os.environ.get("WEBHOOK_OSTFOLD")
    if county == "Buskerud":
        webhook = os.environ.get("WEBHOOK_BUSKERUD")
    if county == "Oslo og Akershus":
        webhook = os.environ.get("WEBHOOK_OSLO_AKERSHUS")
    
    for link in links:
        payload = {"text" : link}
        response = requests.post(webhook, json=payload)
        print(f"Notification sent for {link}: {response.status_code}")
        
def save_to_json(new_links, filename):
    with open(f"data/{filename}.json", "w") as f:
        json.dump(new_links, f, indent=4)

def rss_process(url, newspaper, filename, county):
    old_links = fetch_old_links(filename)
    new_links = fetch_new_links(url, newspaper)
    links = check_updates(old_links, new_links)
    if links:
        notify_slack(links, county)
    save_to_json(new_links, filename)
    return print("Done")