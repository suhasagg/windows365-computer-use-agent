import time,hashlib,json
class Audit:
    def __init__(self):self.events=[]
    def add(self,e):
        prior=self.events[-1]["hash"] if self.events else "GENESIS"
        x={"ts":time.time(),**e,"prior":prior}
        x["hash"]=hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
        self.events.append(x);return x
audit=Audit()
