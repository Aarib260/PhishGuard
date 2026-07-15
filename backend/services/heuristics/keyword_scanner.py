import re

URGENCY_PHRASES = [
    "act now",
    "act immediately",
    "urgent action required",
    "immediate action required",
    "your account will be suspended",
    "account suspended",
    "account locked",
    "verify immediately",
    "respond within 24 hours",
    "within 24 hours",
    "within 48 hours",
    "security alert",
    "unusual activity detected",
    "unauthorized login attempt",
    "payment declined",
    "your payment failed",
    "update your billing",
    "update your payment",
    "claim your prize",
    "you have won",
    "final warning",
    "last chance",
]

CREDENTIAL_REQUEST_PHRASES = [
    "enter your password",
    "provide your password",
    "confirm your password",
    "verify your password",
    "verify your account",
    "verify your identity",
    "confirm your identity",
    "log in to continue",
    "sign in to continue",
    "confirm your credentials",
    "update your account information",
    "reset your password",
    "enter your card number",
    "enter your pin",
    "enter your ssn",
    "social security number",
    "banking details",
    "credit card information",
]

ATTACHMENT_FLAGS = [
    "see attached invoice",
    "open the attachment",
    "download the attached file",
    "attached document",
    "view attachment",
    "attached pdf",
    "attached zip file",
    "attached file",
    "review the attachment",
    "invoice attached",
]

def scan_keywords(text: str) -> dict:
    text_lower = text.lower()

    urgency_matches = [p for p in URGENCY_PHRASES if p in text_lower]
    credential_matches = [p for p in CREDENTIAL_REQUEST_PHRASES if p in text_lower]
    attachment_matches = [p for p in ATTACHMENT_FLAGS if p in text_lower]

    contains_link = bool(re.search(r"https?://", text_lower))

    return {
        "urgency_flags": urgency_matches,
        "credentials_request_flags":credential_matches,
        "attachment_flags": attachment_matches,
        "conatins_link": contains_link,
    }
