from app.policy import policy
from app.audit import audit
from app.w365.client import w365
from app.trajectory import trajectory
class SecurityGateway:
    async def invoke(self,p,run_id,tool,args,approved=False):
        decision,risk,reason=policy.decide(p,tool,args,approved)
        audit.add({"run_id":run_id,"tenant":p.tenant,"subject":p.subject,"tool":tool,"risk":risk,"decision":decision})
        trajectory.add(run_id,{"phase":"policy","tool":tool,"decision":decision,"risk":risk})
        if decision!="allow":return {"status":decision,"risk":risk,"reason":reason}
        try:
            out=await w365.call(tool,args)
            trajectory.add(run_id,{"phase":"action","tool":tool,"status":"ok","arguments":args})
            return {"status":"ok","risk":risk,"result":out}
        except Exception as e:
            trajectory.add(run_id,{"phase":"action","tool":tool,"status":"failed","error":type(e).__name__})
            return {"status":"failed","risk":risk,"reason":str(e)}
gateway=SecurityGateway()
