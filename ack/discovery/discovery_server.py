from flask import Flask, request, jsonify
import threading
import time
import uuid

app = Flask(__name__)
receivers = {}

def cleanup():
    while True:
        current_time = time.time()
        to_remove = [key for key, value in receivers.items() if current_time - value['last_seen'] > 30]  # 30 seconds timeout
        for key in to_remove:
            print(f"Receiver {key} timed out", flush=True)
            del receivers[key]
        time.sleep(5)

        
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    receiver_id = str(uuid.uuid4())  # Generate a unique ID
    receivers[receiver_id] = {'host': data['host'], 'port': data['port'], 'last_seen': time.time(), 'id': receiver_id}
    print(f"Receiver {receiver_id} registered on port {data['port']}", flush=True)
    return jsonify({"message": "Receiver registered", "id": receiver_id}), 201

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    print("Heartbeat received", flush=True)
    print(receivers, flush=True)
    data = request.json
    if data['id'] in receivers:
        receivers[data['id']]['last_seen'] = time.time()
    return jsonify({"message": "Heartbeat received"}), 200

@app.route('/receivers', methods=['GET'])
def get_receivers():
    return jsonify(list(receivers.values())), 200

if __name__ == '__main__':
    print("Starting discovery server...")
    threading.Thread(target=cleanup, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
