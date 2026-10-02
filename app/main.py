from fastapi import FastAPI,Depends,Query
from fastapi.responses import Response
from prometheus_client import Counter,generate_latest,CONTENT_TYPE_LATEST
from app.models import ComputerRequest
from app.security import principal
from app.orchestrator import computer_agent
from app.w365.client import w365
from app.trajectory import trajectory
from app.screenshots import screenshots
from app.audit import audit
RUNS=Counter("computer_agent_runs_total","Computer agent runs",["status"])
app=FastAPI(title="Windows 365 Computer-Use Agent",version="1.0.0")
@app.get("/health/live")
async def live():return {"status":"ok"}
@app.get("/v1/tools")
async def tools(p=Depends(principal)):return await w365.list_tools()
@app.post("/v1/run")
async def run(r:ComputerRequest,approved:bool=Query(False),p=Depends(principal)):
    x=await computer_agent.run(p,r.task,approved);RUNS.labels(x["status"]).inc();return x
@app.get("/v1/runs/{run_id}/trajectory")
async def traj(run_id:str,p=Depends(principal)):return trajectory.get(run_id)
@app.get("/v1/runs/{run_id}/screenshots")
async def shots(run_id:str,p=Depends(principal)):return screenshots.list(run_id)
@app.get("/v1/audit")
async def aud(p=Depends(principal)):return [x for x in audit.events if x.get("tenant")==p.tenant or "tenant" not in x]
@app.get("/metrics")
async def metrics():return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
