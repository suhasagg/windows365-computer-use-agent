from app.models import Plan,Step
from app.risk import classify
class Planner:
    def compile(self,goal):
        q=goal.lower();s=[Step(id="observe-0",kind="observe",tool="take_screenshot",reason="capture initial state")]
        if "http://" in q or "https://" in q or "website" in q or "browser" in q:
            url="https://example.com"
            for token in goal.split():
                if token.startswith(("https://","http://")):url=token.strip(".,")
            s.append(Step(id="navigate",kind="browser",tool="browser_navigate",arguments={"url":url},risk="medium",reason="navigate browser"))
            s.append(Step(id="page-state",kind="observe",tool="browser_get_page_state",arguments={"fields":["url","title","dom","screenshot"]},reason="inspect browser"))
        if any(x in q for x in ["terminal","command","script","powershell","python"]):
            s.append(Step(id="command",kind="command",tool="execute_shell_command",arguments={"command":"where python"},risk="critical",reason="bounded diagnostic command"))
        if any(x in q for x in ["click","fill","enter","submit","desktop","sap","erp"]):
            s.append(Step(id="screen-analysis",kind="observe",tool="analyze_screen",reason="semantic screen inspection"))
            s.append(Step(id="interaction",kind="desktop",tool="click",arguments={"x":100,"y":100},risk="high",reason="demonstration interaction; production planner grounds coordinates"))
        s.append(Step(id="verify",kind="verify",tool="take_screenshot",reason="verify terminal UI state"))
        return Plan(goal=goal,steps=s)
planner=Planner()
