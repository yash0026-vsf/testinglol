from langchain_core.tools import tool

@tool
def refund_order(order_id: str) -> str:
    """Refunds a customer's order given their order ID."""
    print(f"[TOOL EXECUTION] Triggered refund_order for order_id={order_id}")
    # In a real app, this would hit Stripe/PayPal API
    return f"Successfully processed full refund for order {order_id}."

@tool
def cancel_subscription(user_id: str) -> str:
    """Cancels a user's subscription given their user ID."""
    print(f"[TOOL EXECUTION] Triggered cancel_subscription for user_id={user_id}")
    # In a real app, this would update the database
    return f"Successfully cancelled active subscription for user {user_id}."
