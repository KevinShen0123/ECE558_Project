import socket
import pickle
import threading
from config import server_ip, server_port
from client_change_receiver import handle_receive_add, handle_receive_update, handle_receive_delete

# one thread for each pair to pair connection
lock = threading.Lock()
# store info about established pair connection
pair_connections = []
server_socket = None

def getConnection():
    if server_socket:
        return server_socket
    else:
        print("Lost connection with the server")

# Method to handle received message from the server
def handle_received_message(message):
    message_type = message['type']
    data = message['data']

    if message_type == 'connection':
        other_clients = data
        for client_info in other_clients:
            if client_info in pair_connections:
                continue
            else:
                ip, port = client_info.split(':')
                threading.Thread(target=handle_client_connection, args=(ip,int(port))).start()
    elif message_type == 'add':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_add(file_path,file_data)
    elif message_type == 'small_update':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_update(file_path,file_data)
    elif message_type == 'large_update':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_update(file_path,file_data)     
    elif message_type == 'delete':
        file_path = data['file_path']
        handle_receive_delete(file_path)
    elif message_type == 'confirmation':
        result = message['data']['result']
        if result == "SUCCESS":
            print("File {} transferred successfully.".format(file_path))
            return
        if result == "FAIL":
            file_path = message['data']['file_path']
            # The only possibility for a failed change is that the file has been deleted
            handle_receive_delete(file_path)
    else:
        print("Unknown message type received")

# Method to create a new thread for each p2p connection
def handle_client_connection(ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip,port))
        with lock:
            pair_connections.append(client_socket)

        # TODO: Add logic for election
        while True:
            message = client_socket.recv(4096)
        
    except Exception as e:
        print("Could not connect to {}:{} - {}".format(ip,port,e))

    finally:
        client_socket.close()
        with lock:
            pair_connections.remove(client_socket)

# A wrapper to send message to server
# Two types of message: update_notifications, delete_notifications
def send_to_server(server_socket, message_type, data):
    message = {
        'type': message_type,
        'data': data
    }
    serialized_message = pickle.dumps(message)
    # ensure the safety of shared resources
    with lock:
        server_socket.sendall(serialized_message)

def main():
    # load the config info
    server_ip = server_ip
    server_port = server_port

    # connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip,server_port))

    # receive data from the server
    while True:
        message = pre_process_message(server_socket)

        handle_received_message(message)

# to avoid timeout
# refactor 
# almost the same as the function in server connection
def pre_process_message(server_socket):
    TIMEOUT_DURATION = 10
 
    server_socket.settimeout(TIMEOUT_DURATION)
    serialized_message = server_socket.recv(4096)
    message = pickle.loads(serialized_message)

    message_type = message['type']
    if message_type in ['small_update', 'large_update']:
        file_data = b''
        file_data += message['type']['file_data']
        while True:
            try:
                serialized_message_sub = server_socket.recv(4096)
                message_sub = pickle.loads(serialized_message_sub)
                if message_sub['data'] == b'END':
                    break
                else:
                    file_data += message_sub['data']['file_data']
            except socket.timeout:
                print("Timeout occurred while receiving file data.")
                # Handle Timeout
                break
            finally:
                server_socket.settimeout(None)  

        file_path = message['data']['file_path']
        message['data'] = {
            "file_path": file_path,
            "file_data": file_data,
        }

    return message
        
if __name__ == "__main__":
    main()

