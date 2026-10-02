from collections import defaultdict,deque
import time,hashlib,json
class ScreenshotHistory:
    def __init__(self):self.items=defaultdict(lambda:deque(maxlen=50))
    def add(self,run_id,payload):
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        ref=f"shot:{digest[:16]}";self.items[run_id].append({"ref":ref,"ts":time.time(),"payload":payload});return ref
    def list(self,run_id):return list(self.items[run_id])
screenshots=ScreenshotHistory()
