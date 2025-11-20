class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True


def ring_election(processes, initiator_index):
    print(f"\nLeader crashed! Election started by Process {processes[initiator_index].pid}")

    n = len(processes)
    msg = []

    i = initiator_index
    while True:
        p = processes[i]
        if p.alive:
            msg.append(p.pid)
            print(f"Process {p.pid} passes message: {msg}")

        i = (i + 1) % n
        if i == initiator_index:
            break

    new_leader = max(msg)
    print(f"\nNew Coordinator is Process {new_leader}")
    return new_leader


processes = [Process(1), Process(2), Process(3), Process(4)]

print("Initial Leader is Process 4")

processes[3].alive = False
print("Process 4 FAILED")

ring_election(processes, initiator_index=1)
