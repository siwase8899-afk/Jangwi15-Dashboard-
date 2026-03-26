import json
import time
import os

DB_FILE = "Tracking/scraped_items.json"

# Expanded target list representing our Naver Blog search footprint
TARGET_BLOGS = [
    "https://blog.naver.com/tkrhk2075",       # 태광공인
    "https://blog.naver.com/114newtown",      # 114뉴타운
    "https://blog.naver.com/anchang0114",     # 안창
    "https://blog.naver.com/lucky777jangwi",  # [동적수집 가상] 네이버 검색 상위 1
    "https://blog.naver.com/jangwi15pro",     # [동적수집 가상] 네이버 검색 상위 2
    "https://blog.naver.com/realestate_top",  # [동적수집 가상] 네이버 검색 상위 3
    "https://blog.naver.com/invest_map",      # [동적수집 가상] 네이버 검색 상위 4
    "https://blog.naver.com/jangwi_story"     # [동적수집 가상] 네이버 검색 상위 5
]

def init_db():
    if not os.path.exists(DB_FILE):
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
    # Simulate finding new items from the expanded list
    return [
        {
            "id": f"dummy_1_{int(time.time())}",
            "title": "[태광공인] 장위 15구역 대지지분 8평 빌라, 급매",
            "price": "5.5억",
            "deposit": "1.0억",
            "actual_investment": "4.5억",
            "source": "https://blog.naver.com/tkrhk2075",
            "date": time.strftime("%Y-%m-%d %H:%M")
        },
        {
            "id": f"dummy_2_{int(time.time())}",
            "title": "[안창] 실투 3.8억! 15구역 구옥, 전세 안고",
            "price": "4.2억",
            "deposit": "0.4억",
            "actual_investment": "3.8억",
            "source": "https://blog.naver.com/anchang0114",
            "date": time.strftime("%Y-%m-%d %H:%M")
        },
        {
            "id": f"dummy_3_{int(time.time())}",
            "title": "[검색 상위] 장위15 뚜껑 매물, 초기자본 4억",
            "price": "4.5억",
            "deposit": "0.5억",
            "actual_investment": "4.0억",
            "source": "https://blog.naver.com/lucky777jangwi",
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
    ]

def run():
    print(f"Scraping Naver Blogs for Jangwi 15 from {len(TARGET_BLOGS)} sources...")
    db = load_db()
    existing_ids = {item['id'] for item in db}
    
    new_items = dummy_scrape()
    alerts = []
    
    for item in new_items:
        if item['id'] not in existing_ids:
            # We insert at the beginning so the newest is first on the dashboard
            db.insert(0, item)
            alerts.append(item)
            
    if alerts:
        # Keep only the latest 50 to avoid infinite growth
        save_db(db[:50])
        for alert in alerts:
            print(f"NEW_ALERT|{alert['title']}|{alert['actual_investment']}|{alert['source']}")
    else:
        print("NO_NEW_ITEMS")

if __name__ == "__main__":
    run()