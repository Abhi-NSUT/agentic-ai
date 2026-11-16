"""DeskModel: the desk's scripted stand-in, for exact, key-free tests.

One rule: a message with an order id like A17 goes to the order tools
(ShopModel's logic), and anything else goes to search_policies.
"""

import re

from langchain.messages import AIMessage
from .shop_model import ShopModel


class DeskModel(ShopModel):
    def decide(self, messages):
        last = messages[-1]
        if last.type == "tool" and last.text == "No policy covers this.":
            return AIMessage("Our policies do not cover that. A person will reply.")
        if last.type == "tool" or re.findall(r"\b[A-Z]\d+\b", last.text):
            return super().decide(messages)
        query = {"name": "search_policies", "args": {"query": last.text}, "id": "call_p"}
        return AIMessage("", tool_calls=[query])

