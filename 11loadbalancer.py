import threading
import time

def backend_server(name):
    while True:
        req = request_queue.pop(0) if request_queue else None
        if req:
            print(f"{name} processing {req}")
        time.sleep(0.5)

def round_robin(servers, requests):
    i = 0
    for req in requests:
        print(f"[LB] Sending {req} to {servers[i]}")
        request_queue.append(req)
        i = (i + 1) % len(servers)
        time.sleep(0.3)

servers = ["Server-1", "Server-2", "Server-3"]
request_queue = []

for s in servers:
    threading.Thread(target=backend_server, args=(s,), daemon=True).start()

incoming_requests = [f"Request-{i}" for i in range(1, 11)]
round_robin(servers, incoming_requests)

time.sleep(3)
