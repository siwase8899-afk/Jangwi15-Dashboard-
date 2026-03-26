import json
import time
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import re

DB_FILE = "Tracking/scraped_items.json"

TARGET_BLOGS = {
    "tkrhk2075": "태광공인",
    "114newtown": "114뉴타운",
    "anchang0114": "안창"
}

def init_db():
    if not os.path.exists(DB_FILE):
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_db():
    init_db()
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_rss_items(blog_id, broker_name):
    url = f"https://rss.blog.naver.com/{blog_id}.xml"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    items = []
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall('./channel/item'):
            title = item.find('title').text or ""
            link = item.find('link').text or ""
            
            # STRICT FILTER: Must have 15구역 in TITLE (ignore description to avoid keyword stuffing)
            if "장위15" in title or "15구역" in title or "장위 15" in title:
                
                # STRICT EXCLUSION: Ignore mixed posts like "14구역 vs 15구역" or other zones
                if "14구역" in title or "13구역" in title or "11구역" in title or "12구역" in title:
                    continue
                
                clean_link = link.split('?')[0].replace("blog.naver.com", "m.blog.naver.com")
                
                investment = "확인 요망"
                if "급매" in title: investment = "급매"
                match = re.search(r'([0-9\.]+억)', title)
                if match: investment = match.group(1)
                
                post_id = clean_link.split('/')[-1]
                items.append({
                    "id": f"{blog_id}_{post_id}",
                    "title": f"[{broker_name}] {title}",
                    "price": "-",
                    "deposit": "-",
                    "actual_investment": investment,
                    "source": clean_link,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
    except Exception as e:
        print(f"Failed to fetch RSS for {blog_id}: {e}")
        
    return items

def run():
    print("Running STRICT RSS scraper for GitHub Actions...")
    db = load_db()
    existing_ids = {item['id'] for item in db}
    
    new_items = []
    for blog_id, broker_name in TARGET_BLOGS.items():
        new_items.extend(fetch_rss_items(blog_id, broker_name))
    
    added_count = 0
    for item in new_items:
        if item['id'] not in existing_ids:
            db.insert(0, item)
            added_count += 1
            
    print(f"Found {added_count} new STRICT 15구역 posts.")
    save_db(db[:50])
    print("Scraping completed.")

if __name__ == "__main__":
    run()
