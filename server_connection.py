import socket
import threading
import pickle
import sys
from server_change_receiver import handle_receive_add, handle_receive_update, handle_receive_delete

# server socket is a global variable
# Wrapper method to send data to client
def send_to_client(server_socket, message_type, data):
    message = {
        'type': message_type,
        'data': data
    }
    serialized_message = pickle.dumps(message)
    server_socket.sendall(serialized_message)

def handle_client_message(message, client_socket):
    message_type = message['type']
    data = message['data']
    if message_type == 'add':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_add(file_path,file_data)
    if message_type == 'small_update':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_update(file_path,file_data)
    if message_type == 'large_update':
        file_path = data['file_path']
        file_data = data['file_data']
        handle_receive_update(file_path,file_data) 
    if message_type == 'delete':
        file_path = data['file_path']
        handle_receive_delete(file_path)
    else:
        print("Unknown message type received")

# to avoid timeout
def pre_process_message(client_socket):
    TIMEOUT_DURATION = 10
 
    client_socket.settimeout(TIMEOUT_DURATION)
    serialized_message = client_socket.recv(4096)
    message = pickle.loads(serialized_message)

    message_type = message['type']
    if message_type in ['small_update', 'large_update']:
        file_data = b''
        file_data += message['type']['file_data']
        while True:
            try:
                serialized_message_sub = client_socket.recv(4096)
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
                server_socket.settimeout(None)  # 将超时设置回无限制

        file_path = message['data']['file_path']
        message['data'] = {
            "file_path": file_path,
            "file_data": file_data,
        }

    return message

def handle_client(client_socket):
    try:
        # send the other client nodes' info to the client node requesting connection
        other_clients = [client_socket_dic[client] for client in client_socket_dic.keys() if client != client_socket]
        send_to_client(server_socket, "connection", other_clients)
        
        while True:
            message = pre_process_message(client_socket)
            handle_client_message(message)

    except Exception as e:
        print("Error with client {}:{}".format(client_socket,e))
    finally:
        with lock:
            del client_socket_dic[client_socket]
        client_socket.close()
        print("Connection with {} closed.".format(client_socket))

if len(sys.argv) == 1:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(500)
    client_socket_dic= {} # Use dictionary to record all client nodes' info
    lock = threading.Lock

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        client_info = f"{client_address[0]}:{client_address[1]}"
        with lock:
            client_socket_dic[client_socket] = client_info
        print("Accepted connection from {}".format(client_address))
        threading.Thread(target=handle_client, args=(client_socket)).start()

