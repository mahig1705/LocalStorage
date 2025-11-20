import socket

client = socket.socket()
client.connect(("127.0.0.1", 5000))

while True:
    msg = input("You: ")
    if msg == "exit":
        break
    client.send(msg.encode())
    print("Server:", client.recv(1024).decode())

client.close()
