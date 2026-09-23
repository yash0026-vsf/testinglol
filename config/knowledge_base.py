# Simple mocked Knowledge Base for Vercel deployment (no heavy DB)

COMPANY_POLICIES = {
    "refund": "Refund Policy: Customers are eligible for a full refund within 30 days of purchase if the product is defective. Otherwise, only a 50% refund is available. No refunds after 30 days.",
    "sla": "Technical SLA: We guarantee 99.9% uptime. If downtime exceeds 0.1% in a month, customers receive a 10% credit.",
    "shipping": "Shipping Policy: Standard shipping takes 3-5 business days. Expedited takes 1-2 days.",
    "escalation": "Escalation Policy: Always apologize first. If the user mentions legal action or the press, escalate immediately."
}

def retrieve_knowledge(query: str) -> str:
    """Very basic semantic/keyword retriever."""
    query = query.lower()
    results = []
    
    if "refund" in query or "money" in query or "cancel" in query:
        results.append(COMPANY_POLICIES["refund"])
    if "down" in query or "sla" in query or "credit" in query or "guarantee" in query:
        results.append(COMPANY_POLICIES["sla"])
    if "ship" in query or "delivery" in query:
        results.append(COMPANY_POLICIES["shipping"])
    
    if not results:
        return "No specific company policy found for this query."
        
    return "\n\n".join(results)
