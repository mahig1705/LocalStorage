import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print("5 + 3 =", proxy.add(5, 3))
print("10 - 4 =", proxy.sub(10, 4))
print("6 * 7 =", proxy.mul(6, 7))
