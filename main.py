from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Ticket(BaseModel):
    ticket_id: str
    channel: Optional[str] = None
    locale: Optional[str] = None
    message: str

PHISHING   = ["otp", "pin", "password", "asking my", "asking for", "verify your", "share your"]
WRONG_TX   = ["wrong number", "wrong recipient", "wrong account", "sent to wrong", "transferred to wrong"]
PAY_FAIL   = ["payment fail", "failed", "balance deducted", "transaction fail", "deducted but"]
REFUND     = ["refund", "changed my mind", "cancel", "get my money back", "return my money"]

SUMMARIES = {
    "phishing_or_social_engineering": "Customer reports a suspicious contact requesting sensitive account information; flagged as a potential fraud attempt.",
    "wrong_transfer":   "Customer reports sending funds to an unintended recipient and is requesting a recovery or reversal.",
    "payment_failed":   "Customer reports a failed transaction where the account balance may have been deducted; reversal may be required.",
    "refund_request":   "Customer is requesting a refund for a recent transaction.",
    "other":            "Customer submitted a general support inquiry that requires agent review.",
}

def classify(msg: str):
    m = msg.lower()
    if any(k in m for k in PHISHING):
        return "phishing_or_social_engineering", "critical", "fraud_risk"
    if any(k in m for k in WRONG_TX):
        return "wrong_transfer", "high", "dispute_resolution"
    if any(k in m for k in PAY_FAIL):
        return "payment_failed", "high", "payments_ops"
    if any(k in m for k in REFUND):
        return "refund_request", "low", "customer_support"
    return "other", "low", "customer_support"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sort-ticket")
def sort_ticket(t: Ticket):
    case_type, severity, department = classify(t.message)
    human_review = (severity == "critical" or case_type == "phishing_or_social_engineering")
    return {
        "ticket_id": t.ticket_id,
        "case_type": case_type,
        "severity": severity,
        "department": department,
        "agent_summary": SUMMARIES[case_type],
        "human_review_required": human_review,
        "confidence": 0.83
    }