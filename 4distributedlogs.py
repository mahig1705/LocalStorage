import random
from dataclasses import dataclass
from typing import List, Tuple

random.seed(1)

@dataclass
class Log:
    server: str
    raw_ts: float           
    lamport: int
    msg: str

class Server:
    def __init__(self, sid: str, offset: float):
        self.sid = sid
        self.offset = offset      
        self.raw = 0.0
        self.lamport = 0
        self.generated: List[Log] = []

    def now_raw(self):
        self.raw += 1.0 + random()*0.1 if False else 1.0  
        return self.raw + self.offset

    def tick(self):
        self.lamport += 1
        return self.lamport

    def log_internal(self, text):
        self.tick()
        l = Log(self.sid, self.now_raw(), self.lamport, text)
        self.generated.append(l)
        return l

    def send(self, dest, text):
        self.tick()
        l = Log(self.sid, self.now_raw(), self.lamport, f"SEND->{dest.sid}:{text}")
        self.generated.append(l)
        return l 

    def receive(self, msg_lamport, src, text):
        self.lamport = max(self.lamport, msg_lamport)
        self.tick()
        l = Log(self.sid, self.now_raw(), self.lamport, f"RECV<-{src.sid}:{text}")
        self.generated.append(l)
        return l

def simulate():
    S = [Server("S1", offset=0.0), Server("S2", offset=5.0), Server("S3", offset=-3.0)]
    logs: List[Log] = []

    logs.append(S[0].log_internal("startup"))
    logs.append(S[1].log_internal("startup"))
    logs.append(S[2].log_internal("startup"))

    m1 = S[0].send(S[1], "task-A")
    logs.append(m1)
    r1 = S[1].receive(m1.lamport, S[0], "task-A")
    logs.append(r1)

    logs.append(S[1].log_internal("process-A"))
    m2 = S[1].send(S[2], "task-B")
    logs.append(m2)

    logs.append(S[2].log_internal("local-job"))
    r2 = S[2].receive(m2.lamport, S[1], "task-B")
    logs.append(r2)

    m3 = S[2].send(S[0], "ack")
    logs.append(m3)
    r3 = S[0].receive(m3.lamport, S[2], "ack")
    logs.append(r3)

    all_logs = logs

    print("\nRAW collected logs (in generation order):")
    for l in all_logs:
        print(f"{l.server:3} | raw={l.raw_ts:5.1f} | lamport={l.lamport:2d} | {l.msg}")

    merged = sorted(all_logs, key=lambda x: (x.lamport, x.server))
    print("\nMERGED logs (sorted by Lamport, tiebreaker ServerID):")
    for l in merged:
        print(f"{l.lamport:2d} | {l.server:3} | raw={l.raw_ts:5.1f} | {l.msg}")

    print("\nVERIFY causal order (send -> receive checks):")
    checks: List[Tuple[str,str,int,int]] = []
    for s in all_logs:
        if s.msg.startswith("SEND->"):
            parts = s.msg.split(":")
            dest = parts[0].split("->")[1].split("S")[-1]  

            for r in all_logs:
                if r.msg.startswith("RECV<-") and r.msg.endswith(parts[1]):
                    if f"RECV<-{s.server}:" in r.msg:
                        checks.append((s.server, r.server, s.lamport, r.lamport))
    for a,b,ls,lr in checks:
        ok = "OK" if ls < lr else "VIOLATION"
        print(f"{a}({ls}) -> {b}({lr}) : {ok}")

if __name__ == "__main__":
    simulate()
