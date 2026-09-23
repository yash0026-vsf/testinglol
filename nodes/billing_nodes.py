from graph.state import SupportState
from config.llm import get_llm
from config.tools import refund_order, cancel_subscription
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class BillingResponse(BaseModel):
    response: str = Field(description="The response to the customer. Inform them if you used a tool.")

BILLING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a Billing Support Agent. You can refund orders or cancel subscriptions if the user asks.\nCall the appropriate tool if needed, then respond to the user."),
    ("human", "{customer_message}")
])

def _process_billing(state: SupportState) -> dict:
    llm = get_llm()
    # Bind the tools
    llm_with_tools = llm.bind_tools([refund_order, cancel_subscription])
    
    # First, let the LLM decide if it needs to call a tool
    msg = llm_with_tools.invoke(state["processed_message"])
    
    tool_results = []
    if msg.tool_calls:
        # Execute tools manually for simplicity
        for call in msg.tool_calls:
            if call["name"] == "refund_order":
                res = refund_order.invoke(call["args"])
                tool_results.append(res)
            elif call["name"] == "cancel_subscription":
                res = cancel_subscription.invoke(call["args"])
                tool_results.append(res)
                
    # Now get the final response
    context = "Tool Execution Results: " + " ".join(tool_results) if tool_results else "No tools executed."
    
    structured_llm = llm.with_structured_output(BillingResponse)
    chain = BILLING_PROMPT | structured_llm
    
    final_res = chain.invoke({"customer_message": state["processed_message"] + "\n\n" + context})
    
    return {
        "response": final_res.response,
        "intent_resolved": True,
        "needs_human_escalation": False
    }

def handle_duplicate_charge(state: SupportState) -> dict: return _process_billing(state)
def handle_refund_request(state: SupportState) -> dict: return _process_billing(state)
def handle_payment_failure(state: SupportState) -> dict: return _process_billing(state)
def handle_other_billing(state: SupportState) -> dict: return _process_billing(state)