def max_vc(a, b):
    return [max(x, y) for x, y in zip(a, b)]

class Proc:
    def __init__(self, pid, n):
        self.id = pid
        self.vc = [0]*n

    def internal(self):
        self.vc[self.id] += 1
        return list(self.vc)

    def send(self):
        self.vc[self.id] += 1
        return list(self.vc)

    def receive(self, msg):
        self.vc = max_vc(self.vc, msg)
        self.vc[self.id] += 1
        return list(self.vc)

P = [Proc(i, 3) for i in range(3)]
events = []

events.append(("e1", P[0].internal()))
msg1 = P[0].send(); events.append(("s1", msg1))
events.append(("r1", P[1].receive(msg1)))
events.append(("e2", P[1].internal()))
msg2 = P[1].send(); events.append(("s2", msg2))
events.append(("e3", P[2].internal()))
events.append(("r2", P[2].receive(msg2)))
events.append(("e4", P[0].internal()))

print("Events with Vector Clocks:")
for name, vc in events:
    print(f"{name:3}  {vc}")
