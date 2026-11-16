"""DeskModel: the desk's scripted stand-in, for exact, key-free tests.

One rule: a message with an order id like A17 goes to the order tools
(ShopModel's logic), and anything else goes to search_policies.
"""

import re

from langchain.messages import AIMessage, ToolMessage

from .shop_model import ShopModel


class DeskModel(ShopModel):
    def decide(self, messages):
        last = messages[-1]
        if isinstance(last, ToolMessage) or re.search(r"\b[A-Z]\d+\b", last.text):
            return super().decide(messages)  # tool results, or an order question
        if "search_policies" in [t.name for t in self.tools]:
            call = {"name": "search_policies", "args": {"query": last.text}, "id": "call_policy"}
            return AIMessage("", tool_calls=[call])
        return super().decide(messages)
