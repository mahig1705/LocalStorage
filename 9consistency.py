import time
import threading

replicas = {
    "R1": {"x": 10},
    "R2": {"x": 10},
    "R3": {"x": 10}
}

def print_state(label):
    print(f"\n{label}")
    for r, store in replicas.items():
        print(f"{r}: {store}")

def propagate_update():
    time.sleep(3) 
    value = replicas["R1"]["x"]
    replicas["R2"]["x"] = value
    replicas["R3"]["x"] = value
    print_state("After Propagation (Eventual Consistency Achieved)")

if __name__ == "__main__":
    print_state("Initial State (Strongly Consistent)")

    replicas["R1"]["x"] = 99
    print_state("After Updating R1 Only (INCONSISTENT STATE)")

    t = threading.Thread(target=propagate_update)
    t.start()

    print("\nReading immediately (NOT consistent):")
    print(f"R1 reads x = {replicas['R1']['x']}")
    print(f"R2 reads x = {replicas['R2']['x']}")
    print(f"R3 reads x = {replicas['R3']['x']}")

    t.join()
