from collections import defaultdict,deque
import time
class TrajectoryStore:
    def __init__(self):self.runs=defaultdict(lambda:deque(maxlen=200))
    def add(self,run_id,event):self.runs[run_id].append({"ts":time.time(),**event})
    def get(self,run_id):return list(self.runs[run_id])
trajectory=TrajectoryStore()
