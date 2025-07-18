# genai/genai_explainer.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini (Flash model)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def get_risk_explanation(txn: dict) -> tuple[str, str]:
    """
    Given a risky transaction dictionary, returns:
    (reason for risk, mitigation suggestion)
    """
    prompt = f"""
You are a fraud analyst. Analyze the following transaction and provide:

1. Why this transaction may be risky
2. How to prevent such risks in the future

Transaction:
- Type: {txn['txn_type']}
- Amount: {txn['amount']}
- Source Account: {txn['source_account']}
- Destination Account: {txn['dest_account']}
- Status: {txn['status']}
- IP Address: {txn['ip_address']}
- Device ID: {txn['device_id']}
- Timestamp: {txn['timestamp']}

Give your response in the following format:
Reason: <brief explanation>
Mitigation: <preventive action>
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Parse based on keywords
        reason = "Not found"
        mitigation = "Not found"

        for line in text.splitlines():
            if line.lower().startswith("reason:"):
                reason = line.split(":", 1)[1].strip()
            elif line.lower().startswith("mitigation:"):
                mitigation = line.split(":", 1)[1].strip()

    except Exception as e:
        reason = "Failed to generate explanation"
        mitigation = str(e)

    return reason, mitigation
