import socket, threading

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data: break
        response = data.upper()
        conn.send(response.encode())
    conn.close()
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket()
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Server running on port 5000...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
