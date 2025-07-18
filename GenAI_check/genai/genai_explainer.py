# genai/genai_explainer.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini model (flash for speed)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

def get_risk_explanation(txn: dict) -> tuple[str, str]:
    """
    Given a risky transaction (as dict), return (reason, mitigation).
    """
    prompt = f"""
You are an expert fraud analyst. Analyze the following transaction and explain:
1. Why this transaction may be risky.
2. What could be done to prevent such a fraud in the future.

Transaction Details:
- Type: {txn['txn_type']}
- Amount: {txn['amount']}
- Source Account: {txn['source_account']}
- Destination Account: {txn['dest_account']}
- Status: {txn['status']}
- IP Address: {txn['ip_address']}
- Device ID: {txn['device_id']}
- Timestamp: {txn['timestamp']}
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        parts = response.content.strip().split("\n")
        reason = next((line.split(":", 1)[1].strip() for line in parts if "risky" in line.lower()), "Risk explanation not found")
        mitigation = next((line.split(":", 1)[1].strip() for line in parts if "prevent" in line.lower()), "Mitigation suggestion not found")
    except Exception as e:
        reason = "GenAI explanation failed"
        mitigation = str(e)

    return reason, mitigation
