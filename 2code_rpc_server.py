from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def execute_code(code_string):
    try:
        local_env = {}
        print(f"[SERVER] Executing code: {code_string}")

        result = eval(code_string, {}, local_env)
        return result

    except Exception as e:
        return f"Error during execution: {e}"

server = ThreadedRPCServer(("localhost", 9000), allow_none=True)
print("Remote Code Execution RPC Server running on port 9000...")

server.register_function(execute_code, "run")
server.serve_forever()
