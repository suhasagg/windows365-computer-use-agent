from urllib.parse import urlparse
from app.config import settings
from app.risk import classify
class Policy:
    def decide(self,p,tool,args,approved=False):
        risk=classify(tool,args)
        if tool=="browser_navigate":
            host=(urlparse(str(args.get("url",""))).hostname or "").lower()
            if host not in settings.hosts:return "deny",risk,"browser host not allowlisted"
        if tool in {"execute_shell_command","execute_python_code"} and "computer:command" not in p.scopes:
            return "deny",risk,"missing command scope"
        if risk=="low" and "computer:read" in p.scopes:return "allow",risk,"read allowed"
        if risk=="medium" and "computer:act" in p.scopes:return "allow",risk,"bounded navigation allowed"
        if risk in {"high","critical"}:
            if "computer:act" not in p.scopes:return "deny",risk,"missing act scope"
            if not approved:return "approval_required",risk,"sensitive computer action"
            return "allow",risk,"approved"
        return "deny",risk,"scope/policy denied"
policy=Policy()
