import re
from fastapi import APIRouter

from services.heuristics.url_analysis import analyze_url
from services.heuristics.keyword_scanner import scan_keywords
from services.heuristics.scoring import (
    calculate_score,
    get_label
)

from services.llm_service import explain_result

from db import SessionLocal
from models.history import ScanHistory


router = APIRouter()

def extract_first_url(text: str):
    match = re.search(r"https?//\S+", text)
    return match.group(0) if match else None


@router.post("/scan")
def scan_url(data: dict):

    content = data.get("url") or data.get("content") or ""

    if not content.strip():
        return {"error": "No input provided."}
    
    # 1. Run keyword/manipulation-language scan on the raw text always
    keyword_result = scan_keywords(content)
    # 2. If the input is (or contains) a URL, run URL analysis on it too
    found_url = content.strip() if content.strip().startswith(("http://", "https://")) else extract_first_url(content)

    if found_url:
        url_analysis = analyze_url(found_url)
    else:
        url_analysis = {
            "domain": None,
            "https": True,
            "suspicious_tld": False,
            "ip_address": False,
            "long_url": False,
            "brand_impersonation": None,
            "uses_typosquatting": False,
        }

   
    # 2. Risk score
    score = calculate_score(url_analysis, keyword_result)


    # 3. Label
    label = get_label(score)



    # 4. AI explanation
    combined_analysis = {
        "url_analysis": url_analysis,
        "keyword_analysis": keyword_result,
    }

    ai_result = explain_result(
        combined_analysis,
        score,
        label,
        content
    )


    # 5. Save scan
    db = SessionLocal()


    new_scan = ScanHistory(
        url=content,
        risk_score=score,
        label=label,
        analysis=combined_analysis,
        explanation=ai_result["explanation"]
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    db.close()

    return {
        "id": new_scan.id,
        "url": content,
        "analysis": combined_analysis,
        "risk_score": score,
        "label": label,
        "ai_explanation": ai_result
    }

@router.get("/history")
def scan_history():


    db = SessionLocal()


    scans = (
        db.query(ScanHistory)
        .order_by(ScanHistory.id.desc())
        .limit(20)
        .all()
    )


    db.close()


    return scans