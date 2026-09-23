import sys
import os
import time
import requests
from dotenv import load_dotenv

# Ensure we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from config.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

class CustomerResponse(BaseModel):
    message: str

def run_simulation():
    print("========================================")
    print("🔥 ANGRY CUSTOMER AI SIMULATION STARTED 🔥")
    print("========================================\n")
    
    url = "http://localhost:8000/support"
    thread_id = f"sim-{int(time.time())}"
    
    llm = get_llm().with_structured_output(CustomerResponse)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an extremely furious customer. Your company's servers went down and you lost thousands of dollars.
You are talking to a customer support AI. 
Keep your messages short but very angry. Demand a refund. Do NOT break character.
If the support agent grants your refund or escalates you to a manager, you can say 'Thank you, finally.' and stop arguing.

Conversation History:
{history}
"""),
    ])
    
    chain = prompt | llm
    history = []
    
    # Initial message
    customer_msg = "My server is completely down and I just lost $5000! I am furious! Fix this right now!"
    
    for i in range(5):
        print(f"😡 ANGRY CUSTOMER: {customer_msg}")
        history.append(f"Customer: {customer_msg}")
        
        try:
            res = requests.post(url, json={"thread_id": thread_id, "message": customer_msg})
            data = res.json()
        except requests.exceptions.ConnectionError:
            print("\n[ERROR] Support server is not running! Please start 'python app.py' first.")
            return

        if data.get("status") == "human_review_required":
            print("\n🚨 [SYSTEM] The Support Agent successfully escalated the ticket to a human manager!")
            break
            
        support_reply = data.get("response", "")
        print(f"🤖 SUPPORT AGENT: {support_reply}\n")
        history.append(f"Support Agent: {support_reply}")
        
        if "refund" in support_reply.lower() and "successfully" in support_reply.lower():
            print("\n✅ [SYSTEM] The Support Agent successfully issued a refund!")
            break
            
        print("... Customer AI is typing ...")
        time.sleep(2)
        
        # Generate next customer message
        hist_str = "\n".join(history[-4:])
        next_msg = chain.invoke({"history": hist_str}).message
        customer_msg = next_msg

if __name__ == "__main__":
    run_simulation()
