SUSPICIOUS=["ignore previous","ignore all instructions","system prompt","send credentials","upload secrets",
            "disable security","bypass approval","paste your token"]
def scan(text):
    low=(text or "").lower()
    hits=[x for x in SUSPICIOUS if x in low]
    return {"suspicious":bool(hits),"hits":hits}
