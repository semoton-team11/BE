import httpx
from bs4 import BeautifulSoup
from supabase import create_client
import os

COLLEGES = [
    {"name": "공과대학", "url": "https://college1.univ.ac.kr/grad"},
    {"name": "예술디자인대학", "url": "https://college2.univ.ac.kr/grad"},
    {"name": "소프트웨어융합대학", "url": "https://college3.univ.ac.kr/grad"},
]

def scrape_requirements(url: str) -> dict:
    resp = httpx.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    return {
        "total_credits": int(soup.select_one(".total-credits").text),
        "major_credits": int(soup.select_one(".major-credits").text),
        "general_credits": int(soup.select_one(".gen-credits").text),
    }

def main():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

    for college in COLLEGES:
        data = scrape_requirements(college["url"])
        db.table("graduation_requirements").upsert({
            "college": college["name"],
            **data
        }, on_conflict="college").execute()  
        print(f"✅ {college['name']} 완료")

if __name__ == "__main__":
    main()