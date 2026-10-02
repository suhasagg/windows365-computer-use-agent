import re
PATTERNS={"private_key":r"-----BEGIN [A-Z ]*PRIVATE KEY-----","bearer":r"Bearer\s+[A-Za-z0-9._-]{20,}"}
def inspect(text):
    hits=[k for k,p in PATTERNS.items() if re.search(p,text or "",re.I)]
    return {"blocked":bool(hits),"hits":hits}
