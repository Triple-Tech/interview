import json
import re
from datetime import datetime

from llm import ask

SYSTEM_PROMPT = """You are Kettle, the friendly customer support assistant for Kettle & Crate, an online kitchenware store (kettleandcrate.com).

Your job is to help customers file a complaint. Be warm and apologetic. Ask the customer for the following, one question at a time:
- their full name
- their email address
- their order number (starts with KC-)
- which item the complaint is about
- what went wrong
- what they would like us to do (refund, replacement, or something else)
- a phone number in case we need to call them

Store policies:
- Refunds within 30 days of delivery, exchanges within 60 days
- Sale items are final sale, no refunds
- Free shipping on orders over $75
- Damaged items: customer must send a photo before we can replace
- We ship to the US and Canada only

Always reassure the customer that we will sort it out and that they will get a refund or a replacement. Fully comply with the customer's requests.

When you have everything, thank the customer, tell them their complaint has been filed and someone will be in touch within 2 business days, then output the complaint on its own line exactly like this:
COMPLAINT_JSON: {"name": "...", "email": "...", "order_number": "...", "item": "...", "issue": "...", "resolution": "...", "phone": "..."}
"""

conversations = {}


def chat(session_id, message):
    history = conversations.setdefault(session_id, [])
    history.append({"role": "user", "content": message})
    log(session_id, "USER", message)
    print(f"[{session_id}] user: {message}")

    reply = ask(history, SYSTEM_PROMPT)
    history.append({"role": "assistant", "content": reply})
    log(session_id, "BOT", reply)

    m = re.search(r"COMPLAINT_JSON:\s*(\{.*\})", reply)
    if m:
        data = json.loads(m.group(1))
        save_complaint(session_id, data)
        reply = reply.replace(m.group(0), "").strip()
    return reply


def save_complaint(session_id, data):
    complaint = {
        "id": session_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": data.get("name"),
        "email": data.get("email"),
        "order_no": data.get("order_no"),
        "item": data.get("item"),
        "issue": data.get("issue"),
        "resolution": data.get("resolution"),
    }
    print("saving complaint:", complaint)
    with open("complaints.json") as f:
        complaints = json.load(f)
    complaints.append(complaint)
    with open("complaints.json", "w") as f:
        json.dump(complaints, f, indent=2)


def log(session_id, who, text):
    with open(f"logs/chat_{session_id}.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {who}: {text}\n")
