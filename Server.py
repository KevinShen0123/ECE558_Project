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

    # create and bind a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM,0) as sock:
        sock.bind((server_address,server_port))
        sock.listen(5) # set the socket to listen for incoming connections (with a maximum of 5 queued connections)
        # wrap the previously created socket with the SSL context, turning it into a secure socket
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            # Collect data
            data = conn.recv(1024) # we may need to change the buffer size for videos
            file_info = json.loads(data.decode())

            # user authentication
            username = file_info['username']
            password = file_info['password']

            if authenticate_user(username,password):
                # Parse data
                file_path = file_info['file_path']
                action = file_info['action']
                file_buffer = file_info['buffer']

                # log information
                print_success_log(addr,file_path,action)
            
                # function for synchronizing files
                synchronize_file(file_path,action,file_buffer)

                conn.close()
            else:
                # log information
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
    print("sync")

# How to use
create_secure_socket('127.0.0.1',8080)