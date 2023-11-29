# This module is responsible for sending the packet from the client side
import socket
import ssl
import json

username = "username" # set new username later
password = "password" # set new username later

# call this function within the callback function in server side
def send_file_info(server_address, server_port, file_info):
    context = ssl.create_default_context()
    
    with socket.create_connection((server_address, server_port)) as sock:
        with context.wrap_socket(sock,server_hostname=server_address) as ssock:
            # wrap the original file info
            print("TBC")

# this function is used to send updates to all other nodes
# node addresses are ip of other nodes
def broadcast_file_info_to_nodes(file_info_json, node_addresses, server_port):
    # Assuming a list of all node addresses is maintained
    for node_address in node_addresses:
        send_file_info(node_address, server_port, file_info_json)

    
# def login_info_wrapper(username,password,file_info):
#     file_info.username = username