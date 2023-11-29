# This module is responsible for establishing secure TCP connection via SSL at Server Side
# For simplicity, we use self-signed certificates to demonstrate

# All the comments are only for learning purpose, delete before final submission!
# Add more error handling code

import socket
import ssl
import json
from log import print_success_log,print_error_login_log

path_to_cert = "path/to/cert.pem" # dummy path
path_to_key = "path/to/key.pem" # dummy path

# For server side
def create_secure_socket(server_address, server_port):
    # create a new SSL context with default settings for the purpose of client authentication
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # load the certificate and private key into the context
    context.load_cert_chain(certfile=path_to_cert,keyfile=path_to_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((server_address, server_port))
        sock.listen(5)  # Listen for incoming connections

        while True:  # Continuous listening
            with context.wrap_socket(sock, server_side=True) as ssock:
                conn, addr = ssock.accept()

                # Receive and process data
                data = conn.recv(1024)  # Adjust buffer size as needed
                file_info = json.loads(data.decode())

                # User authentication
                username = file_info['username']
                password = file_info['password']

                if authenticate_user(username, password):
                    process_received_data(file_info, addr)
                else:
                    print_error_login_log(addr)
                    conn.close()

# Authentication at server side
# We may need a database to store username and password, here I just use the simplest way to do it
# We may need to use token for security concern
def authenticate_user(username,password):
    if username == "username" and password == "password":
        return True
    else:
        return False

# A dummy function now
def synchronize_file(file_path,action,file_buffer):
    if action == 'added' or action == 'modified':
        with open(file_path, 'wb') as file:
            file.write(file_buffer)

    elif action == 'removed':
        # os.remove(file_path)
        print('handle remove')

# This function will process the received data and updates local files accordingly.
def process_received_data(file_info):
    file_path = file_info['file_path']
    action = file_info['action']
    file_buffer = file_info.get('buffer', None)

    if file_buffer:
        file_buffer = file_buffer.encode('latin-1')  # Convert back to binary

    synchronize_file(file_path, action, file_buffer)

# How to use
create_secure_socket('127.0.0.1',8080)