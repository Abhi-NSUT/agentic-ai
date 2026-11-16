"""ShopModel: a scripted stand-in chat model (from the "Parallel tool calls" lesson).

It needs no API key and always puts every tool call in one AI message.
"""

import re

from langchain.chat_models import BaseChatModel
from langchain.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class ShopModel(BaseChatModel):
    tools: list = []

    @property
    def _llm_type(self):
        return "shop"

    def bind_tools(self, tools, **kwargs):
        return self.model_copy(update={"tools": tools})  # a copy holding the tools

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        message = self.decide(messages)  # the reply comes from decide
        return ChatResult(generations=[ChatGeneration(message=message)])

    def decide(self, messages):
        results = []  # the tool results at the end
        for m in reversed(messages):
            if not isinstance(m, ToolMessage):
                break
            results.insert(0, m.text)
        if results:  # results are back: answer with them
            return AIMessage(" ".join(results))

        text = messages[-1].text
        orders = re.findall(r"\b[A-Z]\d+\b", text)
        tool = "refund_order" if "refund" in text.lower() else "lookup_order"
        if orders and tool in [t.name for t in self.tools]:  # one call per order id
            calls = [{"name": tool, "args": {"order_id": o}, "id": f"call_{o}"}
                     for o in orders]
            return AIMessage("", tool_calls=calls)
        if orders:  # that tool is not bound
            return AIMessage(f"I have no way to look up {orders[0]} yet.")
        return AIMessage("Hello. Which order is this about?")
