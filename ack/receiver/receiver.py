import socket
import requests
import os
import threading
import time
import random

DISCOVERY_SERVER = "http://discovery_server:5000"
HOST = "0.0.0.0"
PORT = 0  # Let the OS pick an available port

def wait_for_discovery_server():
    while True:
        try:
            response = requests.get(f"{DISCOVERY_SERVER}/receivers")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        print("Waiting for discovery server...", flush=True)
        time.sleep(5)

def register_receiver(host, port):
    data = {
        "host": host,
        "port": port
    }
    response = requests.post(f"{DISCOVERY_SERVER}/register", json=data)
    print(f"Registered on discovery server: {response.json()}", flush=True)
    return response.json().get("id")

def send_heartbeat(receiver_id):
    while True:
        data = {
            "id": receiver_id
        }
        try:
            requests.post(f"{DISCOVERY_SERVER}/heartbeat", json=data)
        except:
            print("Failed to send heartbeat", flush=True)
        time.sleep(10)

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print(f"Received message: {request.decode()}", flush=True)

    # fake error
    # joga uma moeda e se der cara, não envia o ACK
    if random.choice([True, False]):
        print("Error: ACK not sent", flush=True)
        return

    client_socket.send("ACK".encode()) 
    print("Sent ACK", flush=True)
    client_socket.close()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    port = server.getsockname()[1]

    wait_for_discovery_server()
    
    receiver_id = register_receiver(socket.gethostname(), port)
    print(f"Receiver {receiver_id} registered on port {port}", flush=True)

    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(receiver_id,), daemon=True)
    heartbeat_thread.start()
    
    while True:
        client_socket, addr = server.accept()
        handle_client_connection(client_socket)
