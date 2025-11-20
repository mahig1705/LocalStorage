class Node:
    def __init__(self,pid):
        self.pid=pid
        self.alive=True

def bully_election(nodes,initiator):
    print(f"Node {initiator.pid} initiates election")

    higher=[n for n in nodes if n.pid>initiator.pid and n.alive]

    if not higher:
        print(f"Node {initiator.pid} becomes the leader")
        return initiator.pid

    print(f"Node {initiator.pid} sends ELECTION message to: {[n.pid for n in higher]}")

    responders = [n for n in higher if n.alive]
    print(f"Alive higher nodes responding: {[n.pid for n in responders]}")

    new_initiator = responders[-1]
    return bully_election(nodes, new_initiator)

nodes=[Node(1),Node(2),Node(3),Node(4),Node(5)]

print("Initial Coordinator is Node 5\n")

nodes[4].alive = False
print("Node 5 FAILED\n")

coordinator = bully_election(nodes, nodes[0])
print(f"\nFinal Coordinator: Node {coordinator}")