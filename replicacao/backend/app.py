from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

logging.basicConfig(level=logging.INFO)

class Server:
    def __init__(self, name):
        self.name = name
        self.processed_data = []  # Lista de dados processados pelo servidor primário
        self.synchronized_data = []  # Lista de dados sincronizados pelos backups
        self.status = "blue"  # Default status for backups

    def process_request(self, request):
        self.processed_data.append(request)
        logging.info(f"{self.name} (status: {self.status}) processed request: {request}")
        self.emit_server_details_update()

    def synchronize(self, primary_processed_data, primary_synchronized_data):
        # Combine and sort data to keep synchronized_data in order without duplicates
        combined_data = primary_processed_data + primary_synchronized_data
        unique_sorted_data = sorted(set(combined_data), key=combined_data.index)
        self.synchronized_data = unique_sorted_data
        logging.info(f"{self.name} (status: {self.status}) synchronized with primary")
        self.emit_server_details_update()

    def emit_server_details_update(self):
        server_detail = {
            "name": self.name,
            "status": self.status,
            "processed_data": self.processed_data,
            "synchronized_data": self.synchronized_data
        }
        socketio.emit("server_details_updated", server_detail)

# Inicialização dos servidores
primary_server = Server("Primary")
primary_server.status = "green"  # Initial primary server is green
backup_server1 = Server("Backup1")
backup_server2 = Server("Backup2")

backups = [backup_server1, backup_server2]
all_servers = [primary_server, backup_server1, backup_server2]  # Track all servers

# Função para processar uma requisição
def handle_request(request, force_failure=False):
    global primary_server
    if force_failure:
        logging.info("Primary server failed! Promoting a backup...")
        primary_server.status = "red"  # Mark failed server as red
        failed_server_data = primary_server.processed_data
        failed_server_synchronized_data = primary_server.synchronized_data
        logging.info(f"{primary_server.name} (status: {primary_server.status})")
        
        # Promote the first backup to primary
        primary_server = backups.pop(0)
        primary_server.status = "green"  # New primary server is green
        primary_server.synchronize(failed_server_data, failed_server_synchronized_data)
        
        # Add the new request to the processed data of the new primary
        primary_server.process_request(request)
        
        # Create a new backup
        new_backup = Server(f"Backup{len(all_servers)}")
        new_backup.synchronize(primary_server.processed_data, primary_server.synchronized_data)  # Synchronize the new backup with primary
        backups.append(new_backup)
        all_servers.append(new_backup)
        
        logging.info(f"New primary is {primary_server.name} (status: {primary_server.status})")
        
        # Synchronize all existing backups with the new primary
        for backup in backups:
            backup.synchronize(primary_server.processed_data, primary_server.synchronized_data)
            if request not in backup.synchronized_data:
                backup.synchronized_data.append(request)  # Add the new request to synchronized data
                backup.synchronized_data = sorted(backup.synchronized_data)
        
    else:
        primary_server.process_request(request)
        for backup in backups:
            backup.synchronize(primary_server.processed_data, primary_server.synchronized_data)
            if request not in backup.synchronized_data:
                backup.synchronized_data.append(request)  # Add the new request to synchronized data
                backup.synchronized_data = sorted(backup.synchronized_data)                
    
    emit('request_processed', get_servers_dict(), broadcast=True)

def get_servers_dict():
    return {
        server.name: {
            "status": server.status,
            "processed_data": server.processed_data,
            "synchronized_data": remove_duplicates(server.synchronized_data)
        } for server in all_servers
    }

def remove_duplicates(data):
    return list(dict.fromkeys(data))

@app.route('/servers')
def servers():
    return jsonify(get_servers_dict())

@socketio.on('send_request')
def on_send_request(data):
    handle_request(data['request'])

@socketio.on('send_fault_request')
def on_send_fault_request(data):
    handle_request(data['request'], force_failure=True)

@socketio.on('fetch_server_details')
def fetch_server_details(server_name):
    for server in all_servers:
        if server.name == server_name:
            server.emit_server_details_update()
            return

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
