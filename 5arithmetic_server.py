from xmlrpc.server import SimpleXMLRPCServer

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b

print("Arithmetic RPC Server running on port 8000...")
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(add, "add")
server.register_function(sub, "sub")
server.register_function(mul, "mul")
server.serve_forever()
