"""The support desk agent, running on Groq's gpt-oss-120b."""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from .desk_tools import Customer, lookup_order, refund_order
from .search import search_policies

load_dotenv()  # reads GROQ_API_KEY from the root .env

SYSTEM_PROMPT = (
    "You are the support desk of a small online shop. "
    "Use lookup_order or refund_order for questions about the customer's orders, "
    "and search_policies for questions about shop rules. "
    "Answer in one or two short sentences, using only what the tools return. "
    "If a tool says an order is not one of the customer's orders, repeat that sentence as it is. "
    "Never add details the tools did not give."
)


def build_desk(model=None, tools=None):
    """Build the desk agent. Pass a stand-in model (such as DeskModel) to test without a key."""
    model = model or init_chat_model("groq:openai/gpt-oss-120b", temperature=0)
    tools = tools if tools is not None else [lookup_order, refund_order, search_policies]
    return create_agent(model, system_prompt=SYSTEM_PROMPT, tools=tools, context_schema=Customer)


def ask(desk, question, customer="ravi"):
    result = desk.invoke({"messages": [{"role": "user", "content": question}]},
                         context=Customer(customer))
    return result["messages"]


def run():
    desk = build_desk()
    for question in ["Where is A17?", "Is shipping free?", "Where is C40?"]:
        print(f"Q: {question}\nA: {ask(desk, question)[-1].text}\n")
