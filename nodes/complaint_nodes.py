from langchain_core.prompts import ChatPromptTemplate
from config.llm import get_llm
from graph.state import SupportState
from pydantic import BaseModel, Field

class ComplaintAnalysis(BaseModel):
    is_root_cause_identified: bool = Field(description="True if the root cause is fully understood, False if we need more info.")
    response_to_customer: str = Field(description="The response to the customer. Ask clarifying questions if the root cause is not identified. Otherwise, offer a resolution.")
    needs_human_escalation: bool = Field(description="True if the customer remains angry or demands a manager, False otherwise.")

COMPLAINT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI Complaint Investigator for a company.
    
Your goal is to perform a Root Cause Analysis (RCA) on the customer's complaint.
Do not just apologize; investigate *why* the failure happened.

If you do not have enough information to determine the root cause, ask the customer specific diagnostic questions.
If you understand the root cause, provide a detailed explanation and a resolution.
If the customer is highly agitated or demands a manager, set needs_human_escalation to true.

Current Conversation Context:
{context}

Customer Sentiment: {sentiment}
Customer Urgency: {urgency}
"""),
    ("human", "{customer_message}")
])

def process_complaint(state: SupportState) -> dict:
    llm = get_llm().with_structured_output(ComplaintAnalysis)
    chain = COMPLAINT_PROMPT | llm
    
    context_dict = state.get("context", {})
    sentiment = context_dict.get("sentiment", "neutral")
    urgency = context_dict.get("urgency", "low")
    
    # Simple context history
    messages = state.get("messages", [])[:-1]
    context_str = "\\n".join([f"{m.type}: {m.content}" for m in messages[-4:]]) if messages else "No history."

    result = chain.invoke({
        "customer_message": state["processed_message"],
        "context": context_str,
        "sentiment": sentiment,
        "urgency": urgency
    })
    
    if result.needs_human_escalation:
        return {
            "needs_human_escalation": True,
            "escalation_reason": "Customer is highly agitated or requested a manager.",
            "response": result.response_to_customer
        }
        
    return {
        "response": result.response_to_customer,
        "needs_human_escalation": False,
        "intent_resolved": result.is_root_cause_identified
    }
