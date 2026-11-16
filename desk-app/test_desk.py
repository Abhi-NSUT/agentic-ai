from uuid import uuid4

from desk_app.desk import agent
from desk_app.desk_tools import Customer


def ask(who, text):
    config = {"configurable": {"thread_id": str(uuid4())}}   # a new thread for every call
    result = agent.invoke({"messages": [{"role": "user", "content": text}]}, config,
                          context=Customer(who), version="v2")
    return result.value["messages"][-1].text


def test_an_order_is_answered_to_its_owner():
    assert "shipped" in ask("ravi", "Where is A17?")


def test_another_customers_order_is_refused():
    assert "not one of your orders" in ask("mei", "Where is A17?")


def test_a_policy_question_is_answered_from_the_documents():
    assert "5 working days" in ask("ravi", "How long does a refund take?")


def test_an_uncovered_question_is_refused():
    assert "A person will reply" in ask("ravi", "Do you sell gift cards?")


def test_passwords_never_reach_the_model():
    assert "reset link" in ask("ravi", "What is my password?")
