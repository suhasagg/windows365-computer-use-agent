import uuid,httpx
from app.config import settings
try:
    from azure.identity.aio import DefaultAzureCredential
except Exception:
    DefaultAzureCredential=None

class W365MCPClient:
    def __init__(self):
        self.endpoint=settings.w365_mcp_endpoint; self.initialized=False
    async def _headers(self):
        h={"content-type":"application/json","accept":"application/json, text/event-stream"}
        if settings.w365_computer_id:h["x-ms-computerId"]=settings.w365_computer_id
        if self.endpoint and DefaultAzureCredential and settings.w365_token_scope:
            c=DefaultAzureCredential()
            try:h["authorization"]="Bearer "+(await c.get_token(settings.w365_token_scope)).token
            finally:await c.close()
        return h
    async def _rpc(self,method,params=None,notification=False):
        if not self.endpoint:return self._fixture(method,params or {})
        body={"jsonrpc":"2.0","method":method}
        if not notification:body["id"]=str(uuid.uuid4())
        if params is not None:body["params"]=params
        async with httpx.AsyncClient(timeout=settings.tool_timeout_seconds,follow_redirects=False) as c:
            r=await c.post(self.endpoint,headers=await self._headers(),json=body)
            if notification:return {"ok":r.status_code<300}
            r.raise_for_status();return r.json()
    async def initialize(self):
        if self.initialized:return
        await self._rpc("initialize",{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"enterprise-cua","version":"1.0"}})
        await self._rpc("notifications/initialized",{},True);self.initialized=True
    async def list_tools(self):
        await self.initialize();return await self._rpc("tools/list",{})
    async def call(self,name,args=None):
        await self.initialize();return await self._rpc("tools/call",{"name":name,"arguments":args or {}})
    def _fixture(self,method,params):
        if method=="initialize":return {"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}}}}
        if method=="tools/list":
            names=["take_screenshot","analyze_screen","browser_navigate","browser_get_page_state",
                   "click","type_text","press_keys","get_windows","activate_window",
                   "execute_shell_command","execute_python_code","wait_milliseconds"]
            return {"result":{"tools":[{"name":n,"description":"local fixture"} for n in names]}}
        if method=="tools/call":
            n=params.get("name");a=params.get("arguments",{})
            if n=="take_screenshot":return {"result":{"content":[{"type":"text","text":"fixture screenshot captured"}],"fixture":True}}
            if n=="analyze_screen":return {"result":{"fullText":"Demo desktop - no real Cloud PC connected","averageConfidence":1.0,"boxes":[]}}
            if n=="browser_get_page_state":return {"result":{"url":"https://example.com","title":"Example","dom":"<main>Example</main>","tabs":[]}}
            return {"result":{"tool":n,"arguments":a,"fixture":True,"success":True}}
        return {"ok":True}
w365=W365MCPClient()
