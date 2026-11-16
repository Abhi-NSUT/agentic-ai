from langchain.agents.middleware import before_agent
from langchain.messages import AIMessage


@before_agent(can_jump_to=["end"])
def no_passwords(state, runtime):
    if "password" in state["messages"][-1].text.lower():
        answer = AIMessage("I cannot help with passwords. Please use the reset link.")
        return {"messages": [answer], "jump_to": "end"}   # end before the model