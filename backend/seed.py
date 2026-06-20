"""
Run once to populate the DB with initial mock data.
  cd backend
  python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from datetime import date
from app.database import SessionLocal, engine, Base
from app.models import activities, finance, thesis, social, literature

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
            start_date=date(2021, 4, 1),
            end_date=date(2023, 6, 30),
            contribution="擔任大一國文課程助教，協助教授備課與批改作業；每週帶領學生討論文學作品，培養學生語文表達能力；期末協助規劃成果展...",
            photos="[]",
        ),
        activities.Experience(
            type="club",
            title="GDSC 美術組核心幹部",
            organization="國立中央大學",
            start_date=date(2023, 9, 1),
            end_date=date(2024, 1, 31),
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
        activities.TravelEntry(country="臺灣", city="台北", continent="Asia",  visited_at=date(2003, 1, 1)),
        activities.TravelEntry(country="日本", city="東京", continent="Asia",  visited_at=date(2019, 8, 1)),
        activities.TravelEntry(country="澳大利亞", city="雪梨", continent="Australia", visited_at=date(2023, 1, 1)),
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


def seed_social():
    import json
    if db.query(social.SocialActivity).count():
        print("social_activities: already seeded, skip")
        return
    db.add_all([
        social.SocialActivity(
            name="國際扶輪青年服務計畫",
            organization="國際扶輪社 3480 地區",
            esg_type="Social",
            sdg_numbers=json.dumps([3, 4, 10]),
            period_from=date(2022, 7, 1),
            period_to=date(2023, 6, 30),
            contribution="參與社區弱勢兒童課輔計畫，協助規劃教學活動並擔任志工講師。",
            reflection="在與孩子互動的過程中，深刻體會教育資源分配不均的問題，也啟發我對 ESG 社會面議題的關注。",
        ),
        social.SocialActivity(
            name="淨灘行動 × 海洋守護者",
            organization="黑潮海洋文教基金會",
            esg_type="Environmental",
            sdg_numbers=json.dumps([14, 13]),
            period_from=date(2023, 4, 22),
            period_to=date(2023, 4, 22),
            contribution="參與東部海岸淨灘活動，協助清除海灘廢棄物並進行數據記錄。",
            reflection="海洋廢棄物問題超乎想像，這次經驗讓我更重視企業供應鏈的環境責任。",
        ),
    ])
    db.commit()
    print("social_activities: seeded 2 rows")


def seed_literature():
    if db.query(literature.LiteratureWork).count():
        print("literature_works: already seeded, skip")
        return
    work = literature.LiteratureWork(
        title="秋天的側臉",
        age_written=16,
        period=date(2018, 10, 1),
        awards="全國學生文學獎 散文組 佳作",
        summary="以秋日午後的校園為背景，描寫一段短暫的青春相遇，探索記憶與遺忘的辯證關係。",
        full_text=None,
    )
    db.add(work)
    db.commit()
    db.refresh(work)
    print(f"literature_works: seeded 1 row (id={work.id})")

    if db.query(literature.TimelineEvent).count():
        print("timeline_events: already seeded, skip")
        return
    db.add_all([
        literature.TimelineEvent(
            grade_label="高中 / 高一",
            award_title="全國學生文學獎",
            result="散文組 佳作",
            date=date(2018, 10, 20),
            work_id=work.id,
        ),
        literature.TimelineEvent(
            grade_label="大學 / 大二",
            award_title="教育部文藝創作獎",
            result="小說組 入選",
            date=date(2022, 5, 15),
            work_id=None,
        ),
    ])
    db.commit()
    print("timeline_events: seeded 2 rows")


if __name__ == "__main__":
    seed_experiences()
    seed_travel()
    seed_holdings()
    seed_thesis()
    seed_social()
    seed_literature()
    db.close()
    print("\nDone. DB seeded.")
