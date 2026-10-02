from app.policy import policy
from app.security import Principal
p=Principal("u","t",frozenset({"computer:read","computer:act","computer:command"}))
def test_screenshot_read():assert policy.decide(p,"take_screenshot",{},False)[0]=="allow"
def test_click_approval():assert policy.decide(p,"click",{"x":1,"y":1},False)[0]=="approval_required"
def test_command_approval():assert policy.decide(p,"execute_shell_command",{"command":"where python"},False)[0]=="approval_required"
def test_browser_allowlist():assert policy.decide(p,"browser_navigate",{"url":"https://evil.invalid"},False)[0]=="deny"
