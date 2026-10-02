from typing import Any,Literal
from pydantic import BaseModel,Field
class ComputerRequest(BaseModel):
    task:str
    session_id:str|None=None
    context:dict[str,Any]=Field(default_factory=dict)
class Step(BaseModel):
    id:str
    kind:Literal["observe","browser","desktop","keyboard","command","verify","handoff"]
    tool:str
    arguments:dict[str,Any]=Field(default_factory=dict)
    risk:Literal["low","medium","high","critical"]="low"
    reason:str=""
class Plan(BaseModel):
    goal:str
    steps:list[Step]
class StepResult(BaseModel):
    step_id:str
    status:Literal["ok","failed","denied","approval_required","handoff_required"]
    result:Any=None
    error:str|None=None
    screenshot_ref:str|None=None
