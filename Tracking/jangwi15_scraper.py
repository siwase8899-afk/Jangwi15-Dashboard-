import json
import time
import os
import random

DB_FILE = "Tracking/scraped_items.json"

TARGET_BLOGS = [
    "https://blog.naver.com/tkrhk2075",       # 태광공인
    "https://blog.naver.com/114newtown",      # 114뉴타운
    "https://blog.naver.com/anchang0114",     # 안창
]

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

def dummy_scrape():
    # Adding query parameters or explicit post paths if possible
    return [
        {
            "id": f"dummy_1_{int(time.time())}",
            "title": "[태광공인] 장위 15구역 대지지분 8평 빌라, 급매",
            "price": "5.5억",
            "deposit": "1.0억",
            "actual_investment": "4.5억",
            "source": "https://m.blog.naver.com/tkrhk2075",
            "date": time.strftime("%Y-%m-%d %H:%M")
        },
        {
            "id": f"dummy_2_{int(time.time())}",
            "title": "[안창] 실투 3.8억! 15구역 구옥, 전세 안고",
            "price": "4.2억",
            "deposit": "0.4억",
            "actual_investment": "3.8억",
            "source": "https://m.blog.naver.com/anchang0114",
            "date": time.strftime("%Y-%m-%d %H:%M")
        },
        {
            "id": f"dummy_3_{int(time.time())}",
            "title": "[검색 상위] 장위15 뚜껑 매물, 초기자본 4억",
            "price": "4.5억",
            "deposit": "0.5억",
            "actual_investment": "4.0억",
            "source": "https://m.blog.naver.com/lucky777jangwi",
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
    ]

def run():
    print("Running scraper for GitHub Actions...")
    db = load_db()
    existing_ids = {item['id'] for item in db}
    
    new_items = dummy_scrape()
    
    for item in new_items:
        if item['id'] not in existing_ids:
            db.insert(0, item)
            
    # Save the updated DB
    save_db(db[:50])
    print("Scraping completed.")

if __name__ == "__main__":
    run()
