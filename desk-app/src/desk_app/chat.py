from langgraph.types import Command
from .desk import Customer, agent


def say(who, text, thread):
    config = {"configurable": {"thread_id": thread}}
    result = agent.invoke({"messages": [{"role": "user", "content": text}]}, config,
                          context=Customer(who), version="v2")
    if result.interrupts:
        print(f"{who}: {text}\n  paused for approval: {result.interrupts[0].value['action_requests'][0]['args']}")
        result = agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config,
                              context=Customer(who), version="v2")
        text = "(approved)"
    print(f"{who}: {text}\n  desk: {result.value['messages'][-1].text}")
