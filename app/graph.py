from typing import TypedDict,Any
from langgraph.graph import StateGraph,END
from app.orchestrator import computer_agent
class State(TypedDict,total=False):
    task:str;principal:Any;approved:bool;result:dict
async def node(s):
    s["result"]=await computer_agent.run(s["principal"],s["task"],s.get("approved",False));return s
b=StateGraph(State);b.add_node("computer_agent",node);b.set_entry_point("computer_agent");b.add_edge("computer_agent",END)
graph=b.compile()
