# scoring.py

def calculate_keyword_score(keyword_result):
    score = 0

    urgency_flags = keyword_result.get("urgency_flags", [])
    credential_flags = keyword_result.get("credential_request_flags", [])
    attachment_flags = keyword_result.get("attachment_flags", [])

    # Urgency language
    score += min(len(urgency_flags) * 8, 24)

    # Requests for passwords, credentials, banking info, etc.
    score += min(len(credential_flags) * 15, 30)

    # Suspicious attachment language
    score += min(len(attachment_flags) * 8, 16)

    return min(score, 50)


def calculate_score(result, keyword_result=None):
    score = 0

    # No HTTPS
    if not result.get("https", True):
        score += 15

    # Suspicious TLD (.tk, .xyz, etc.)
    if result.get("suspicious_tld"):
        score += 25

    # Brand impersonation (PayPal, Microsoft, etc.)
    if result.get("brand_impersonation"):
        score += 35

    # Typosquatting (paypa1, goog1e, micr0soft)
    if result.get("uses_typosquatting"):
        score += 35

    # Direct IP address instead of domain
    if result.get("ip_address"):
        score += 25

    # Extremely long URLs
    if result.get("long_url"):
        score += 5

    # Email content analysis
    if keyword_result:
        score += calculate_keyword_score(keyword_result)

    return min(score, 100)


def get_label(score):
    if score < 25:
        return "Safe"
    elif score < 60:
        return "Suspicious"
    else:
        return "Dangerous"


def get_risk_level(score):
    if score < 25:
        return {
            "label": "Safe",
            "color": "green",
            "description": "No significant phishing indicators detected."
        }

    elif score < 60:
        return {
            "label": "Suspicious",
            "color": "yellow",
            "description": "Some phishing indicators were detected. Proceed with caution."
        }

    else:
        return {
            "label": "Dangerous",
            "color": "red",
            "description": "Multiple phishing indicators detected. Avoid interacting with this content."
        }
