import requests
import socket
import time
import os

DISCOVERY_SERVER = "http://discovery_server:5000"
ACK_TIMEOUT = 5 # seconds
def discover_receivers():
    response = requests.get(f"{DISCOVERY_SERVER}/receivers")
    receivers = response.json()
    
    return receivers

def send_message(receiver, message):
    # Send message to receiver. if no ACK is received in ACK_TIMEOUT seconds, retries sending the message
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((receiver['host'], receiver['port']))
            print(f"Sending message to receiver {receiver['id']}...", flush=True)
            s.send(message.encode())
            s.settimeout(ACK_TIMEOUT)
            ack = s.recv(1024)
            s.close()
            received_ack = ack.decode()
            if received_ack == "":
                raise Exception("No ACK received")
            print(f"Received ACK: {received_ack}", flush=True)
            return received_ack
        except socket.timeout:
            print(f"ACK not received from receiver {receiver['id']}. Retrying...", flush=True)
        except ConnectionRefusedError:
            print(f"Connection refused by receiver {receiver['id']}. Giving Up...", flush=True)
            return None
        except ConnectionResetError:
            print(f"Connection reset by receiver {receiver['id']}. Retrying...", flush=True)
        except KeyboardInterrupt:
            print("Exiting...", flush=True)
            exit(0)
        except Exception as e:
            print(f"Error: {e}", flush=True)
            print(f"Error sending message to receiver {receiver['id']}. Retrying...", flush=True)


def show_receivers(receivers):
    list_receivers = []
    for receiver in receivers:
        list_receivers.append(receiver['id'])
    print("Available receivers:", flush=True)
    for i, receiver in enumerate(list_receivers):
        print(f"{i}: {receiver}", flush=True)

if __name__ == "__main__":
    while True:
        
        print("Discovering receivers...", flush=True)
        receivers = discover_receivers()
        if(len(receivers) == 0):
            # clear screen
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        show_receivers(receivers)
        chosen = input("Choose a receiver to send a message to: ")
        if(int(chosen) >= len(receivers)):
            print("Invalid receiver chosen")
            continue
        receiver_selected = receivers[int(chosen)]

        ack = send_message(receiver_selected, "Hello Receiver!")
        if ack:
            print(f"Received ACK from receiver {receiver_selected['id']}: {ack}", flush=True)
        
