from flask import Flask, request, jsonify
import threading, time, uuid

app = Flask(__name__)

KEY_TTL = 300       
UNBLOCK_TIME = 60    
keys = {}            
lock = threading.Lock()


@app.route("/create", methods=["POST"])
def create():
    k = str(uuid.uuid4())
    with lock:
        keys[k] = {"last": time.time(), "blocked_at": None}
    return jsonify({"key": k})


@app.route("/get", methods=["POST"])
def get():
    with lock:
        for k, v in keys.items():
            if v["blocked_at"] is None:
                v["blocked_at"] = time.time()
                return jsonify({"key": k})
    return jsonify({"error": "no available keys"}), 404


@app.route("/unblock", methods=["POST"])
def unblock():
    k = request.json.get("key")
    with lock:
        if k in keys:
            keys[k]["blocked_at"] = None
            return jsonify({"status": "unblocked"})
    return jsonify({"error": "key not found"}), 404


@app.route("/keepalive", methods=["POST"])
def keepalive():
    k = request.json.get("key")
    with lock:
        if k in keys:
            keys[k]["last"] = time.time()
            return jsonify({"status": "alive"})
    return jsonify({"error": "key not found"}), 404


@app.route("/status")
def status():
    return jsonify(keys)

def cleaner():
    while True:
        now = time.time()
        with lock:
            expired = []
            for k, v in list(keys.items()):
                if now - v["last"] > KEY_TTL:
                    expired.append(k)
                if v["blocked_at"] and now - v["blocked_at"] > UNBLOCK_TIME:
                    v["blocked_at"] = None
            for k in expired:
                del keys[k]
        time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=cleaner, daemon=True).start()
    app.run(debug=True, threaded=True)
