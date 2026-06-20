"""
Run once to populate the DB with initial mock data.
  cd backend
  python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models import activities, finance, thesis

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_experiences():
    if db.query(activities.Experience).count():
        print("experiences: already seeded, skip")
        return
    db.add_all([
        activities.Experience(
            type="leadership",
            title="大一國文助教",
            organization="國立臺中科技大學 通識教育中心",
            period="2021/04 – 2023/06",
            contribution="擔任大一國文課程助教，協助教授備課與批改作業；每週帶領學生討論文學作品，培養學生語文表達能力；期末協助規劃成果展...",
            photos="[]",
        ),
        activities.Experience(
            type="club",
            title="GDSC 美術組核心幹部",
            organization="國立中央大學",
            period="2023/09 – 2024/01",
            contribution="負責社群媒體視覺設計與活動文宣，統籌 Google Developer Student Club 美術組運作；協助舉辦技術工作坊海報設計，提升社員招募轉換率...",
            photos="[]",
        ),
    ])
    db.commit()
    print("experiences: seeded 2 rows")


def seed_travel():
    if db.query(activities.TravelEntry).count():
        print("travel_entries: already seeded, skip")
        return
    db.add_all([
        activities.TravelEntry(country="臺灣", city="台北", continent="Asia",  visited_at="2003-01-01"),
        activities.TravelEntry(country="日本", city="東京", continent="Asia",  visited_at="2019-08-01"),
        activities.TravelEntry(country="澳大利亞", city="雪梨", continent="Australia", visited_at="2023-01-01"),
    ])
    db.commit()
    print("travel_entries: seeded 3 rows")


def seed_holdings():
    if db.query(finance.Holding).count():
        print("holdings: already seeded, skip")
        return
    db.add_all([
        finance.Holding(symbol="00713", name="元大台灣高息低波", currency="TWD", broker="國泰世華", shares=264,  avg_price=51.77, market_price=59.80, dividend=313),
        finance.Holding(symbol="00881", name="國泰台灣科技領頭", currency="TWD", broker="國泰世華", shares=281,  avg_price=34.98, market_price=53.00, dividend=424),
        finance.Holding(symbol="00922", name="國泰台灣領袖50",   currency="TWD", broker="國泰世華", shares=352,  avg_price=27.96, market_price=38.97, dividend=629),
        finance.Holding(symbol="奈米投_Level1", name="奈米投 Level 1", currency="USD", broker="富邦", shares=1, avg_price=50.11,  market_price=50.11,  dividend=0),
        finance.Holding(symbol="奈米投_Level2", name="奈米投 Level 2", currency="USD", broker="富邦", shares=1, avg_price=101.40, market_price=101.40, dividend=0),
        finance.Holding(symbol="奈米投_Level3", name="奈米投 Level 3", currency="USD", broker="富邦", shares=1, avg_price=300.00, market_price=307.40, dividend=0),
    ])
    db.commit()
    print("holdings: seeded 6 rows")


def seed_thesis():
    if not db.query(thesis.ThesisNote).count():
        db.add(thesis.ThesisNote(content="碩論注意事項、教授建議"))
        db.commit()
        print("thesis_note: seeded")
    else:
        print("thesis_note: already seeded, skip")

    if not db.query(thesis.ThesisIdea).count():
        db.add_all([
            thesis.ThesisIdea(title="想法一", content="關於 AIS 與 AI 整合的研究方向...", status="pending"),
            thesis.ThesisIdea(title="想法二", content="研究生成式 AI 對財務報表分析的影響...", status="approved"),
            thesis.ThesisIdea(title="想法三", content="某個方向無法執行的原因...", status="rejected"),
        ])
        db.commit()
        print("thesis_ideas: seeded 3 rows")
    else:
        print("thesis_ideas: already seeded, skip")

    if not db.query(thesis.ThesisPaper).count():
        db.add(thesis.ThesisPaper(
            topic="LLM",
            name="The impact of generative AI on information processing: Evidence from the ban of ChatGPT in Italy.",
            journal="Journal of Accounting and Economics",
            authors="Bertomeu, J., Lin, Y., Liu, Y., & Ni, Z.",
            year=2025,
            purpose="本論文的研究目的旨在探討「生成式人工智慧（如ChatGPT）的出現與應用，是否影響資本市場的資訊處理效率」...",
            contribution="1. 縮減文字空間：首創利用「義大利禁用ChatGPT」的自然實驗，提供生成式AI影響資本市場資訊效率的因果證據...",
        ))
        db.commit()
        print("thesis_papers: seeded 1 row")
    else:
        print("thesis_papers: already seeded, skip")


if __name__ == "__main__":
    seed_experiences()
    seed_travel()
    seed_holdings()
    seed_thesis()
    db.close()
    print("\nDone. DB seeded.")
