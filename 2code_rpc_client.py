from xmlrpc.client import ServerProxy
proxy = ServerProxy("http://localhost:9000")

tasks = [
    "4 + 7",
    "10 * 12",
    "sorted([5,3,8,1])",
    "'hello'.upper()",
    "len('test123')",
]

for t in tasks:
    print(f"\nSending task: {t}")
    result = proxy.run(t)
    print("Result:", result)
