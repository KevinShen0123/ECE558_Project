import sys
import socket
import pickle
import threading
from server_connection import *
# prepare for final merge
if len(sys.argv) == 1:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1000)
    client_socket_dic= [] # record ip and port only,through recv from client,which is ip port
    lock = threading.Lock

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        client_info_str=client_socket.recv(1024)
        client_info_list=client_info_str.split(" ")
        client_ip=client_info_list[0]
        client_port=int(client_info_list[1])
        with lock:
            client_socket_dic.append([client_ip,client_port])
        threading.Thread(target=handle_client, args=(client_socket)).start()
else:
    pass