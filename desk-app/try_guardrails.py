from desk_app.chat import say
from desk_app.desk import agent
# # say("ravi", "What is my password?", "ravi-0")
# # say("ravi", "My card 4111 1111 1111 1111 was charged. Where is A17?", "ravi-1")
# # say("ravi", "How long does a refund take?", "ravi-1") 
# # say("ravi", "Please refund A17", "ravi-1")   # A17 is Ravi's order
# # say("mei", "Please refund A17", "mei-1")   # A17 is not Mei's
say("ravi", "My card 4111 1111 1111 1111 was charged. Where is A17?", "ravi-1")
say("ravi", "How long does a refund take?", "ravi-1")   # same thread


state = agent.get_state({"configurable": {"thread_id": "ravi-1"}})
print(len(state.values["messages"]), "messages saved")
print(state.values["messages"][0].text)   # the first message, as stored

mei = agent.get_state({"configurable": {"thread_id": "mei-1"}})
print(len(mei.values.get("messages", [])), "messages on mei-1")   # another customer's thread