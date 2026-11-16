from dataclasses import dataclass

from langchain.tools import ToolRuntime, tool

# order id -> (owner, status)
ORDERS = {"A17": ("ravi", "shipped on 3 March"), "C40": ("mei", "waiting for stock")}


@dataclass
class Customer:
    name: str  # who is asking, set by your code, never by the model


@tool
def lookup_order(order_id: str, runtime: ToolRuntime[Customer]) -> str:
    """Look up one of the customer's orders by its id, such as A17."""
    owner, status = ORDERS.get(order_id, (None, None))
    if owner != runtime.context.name:  # someone else's order, or no such order
        return f"{order_id} is not one of your orders."
    return f"{order_id} {status}."


@tool
def refund_order(order_id: str, runtime: ToolRuntime[Customer]) -> str:
    """Refund one of the customer's orders in full. This cannot be undone."""
    owner, _ = ORDERS.get(order_id, (None, None))
    if owner != runtime.context.name:
        return f"{order_id} is not one of your orders, so it cannot be refunded."
    return f"Refunded {order_id}."
