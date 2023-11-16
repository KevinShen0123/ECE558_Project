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
    

# def login_info_wrapper(username,password,file_info):
#     file_info.username = username