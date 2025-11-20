class Server:
    def __init__(self, sid):
        self.sid = sid
        self.balance = 100
        self.lamport = 0
        self.alive = True
        self.leader = None

    def tick(self):
        self.lamport += 1
        return self.lamport

    def apply(self, amt, seq):
        self.balance += amt
        print(f"Server {self.sid} applied transaction {seq}: new balance {self.balance}")


def ring_election(servers):
    max_id = None
    for s in servers:
        if s.alive:
            if max_id is None or s.sid > max_id:
                max_id = s.sid
    if max_id is not None:
        print(f"New Leader elected: Server {max_id}")
    return max_id


def leader_broadcast(leader, servers, amount):
    leader.tick()
    seq = leader.lamport
    print(f"Leader Server {leader.sid} assigns transaction {seq} with amount {amount}")
    for s in servers:
        if s.alive:
            s.apply(amount, seq)


if __name__ == "__main__":
    S1 = Server(1)
    S2 = Server(2)
    S3 = Server(3)

    servers = [S1, S2, S3]

    leader_id = ring_election(servers)
    leader = [s for s in servers if s.sid == leader_id][0]
    leader_broadcast(leader, servers, 50)

    print("leader crashed")
    leader.alive = False

    leader_id = ring_election(servers)
    leader = [s for s in servers if s.sid == leader_id][0]
    leader_broadcast(leader, servers, -20)

    print("Final Balances:")
    for s in servers:
        if s.alive:
            print(f"Server {s.sid}: Balance {s.balance}")
