import uuid
from app.planner import planner
from app.gateway import gateway
from app.screenshots import screenshots
from app.trajectory import trajectory
from app.verifier import verifier
from app.config import settings
class ComputerAgent:
    async def run(self,p,task,approved=False):
        run_id=str(uuid.uuid4());plan=planner.compile(task);results=[];obs=[]
        trajectory.add(run_id,{"phase":"plan","plan":plan.model_dump()})
        for i,step in enumerate(plan.steps[:settings.max_steps]):
            x=await gateway.invoke(p,run_id,step.tool,step.arguments,approved)
            ref=None
            if step.tool in {"take_screenshot","browser_get_page_state","zoom_region"} and x["status"]=="ok":
                ref=screenshots.add(run_id,x["result"]);obs.append(x["result"])
            if step.tool=="analyze_screen" and x["status"]=="ok":obs.append(x["result"])
            results.append({"step":step.model_dump(),"outcome":x,"screenshot_ref":ref})
            if x["status"] in {"approval_required","denied","failed"}:
                return {"run_id":run_id,"status":x["status"],"plan":plan.model_dump(),"results":results,
                        "trajectory":trajectory.get(run_id),"screenshots":screenshots.list(run_id)}
        v=verifier.verify(obs,trajectory.get(run_id))
        return {"run_id":run_id,"status":"succeeded" if v["verified"] else "verification_failed",
                "plan":plan.model_dump(),"results":results,"verification":v,
                "trajectory":trajectory.get(run_id),"screenshots":screenshots.list(run_id)}
computer_agent=ComputerAgent()
