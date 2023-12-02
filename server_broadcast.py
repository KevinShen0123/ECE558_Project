import socket
import threading
import os

from server_connection import client_socket_dic, send_to_client, lock

def update_broadcast_message(file_path):
    file_size = os.path.getsize(file_path)
    max_size = 1024 * 1024 * 5

    if file_size > max_size:
        with lock:
            for conn in client_socket_dic.keys():
                try:
                    send_chunked_data_over_existing_connection(conn, file_path)
                except Exception as e:
                    print("Error sending message to client: {}".format(e))
        
    else:
        with lock:
            for conn in client_socket_dic.keys():
                try:
                    send_data_over_existing_connection(conn, file_path)
                except Exception as e:
                    print("Error sending message to client: {}".format(e))

def delete_broadcast_message(file_path):
    with lock:
            for conn in client_socket_dic.keys():
                try:
                    send_delete_file_request(conn, file_path)
                except Exception as e:
                    print("Error sending message to client: {}".format(e))


def send_data_over_existing_connection(conn, file_path):  
    with open(file_path,'rb') as file:
        while True:
            data = file.read()
            if not data:
                break
            # get server socket
            send_data = {
                "file_path":file_path,
                "file_data": data,
            }
            send_to_client(conn, "small_update", send_data)
    send_to_client(conn, "small_update", b'END')

# Chunk the data and then send data over existing connection
def send_chunked_data_over_existing_connection(conn, file_path, chunk_size=1024*1024*5):
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size // chunk_size) + (1 if file_size % chunk_size > 0 else 0)

    with open(file_path,'rb') as file:
        for chunk_num in range(total_chunks):
            data = file.read(chunk_size)
            header = f"{len(data):010d}:{chunk_num:010d}".encode()
            send_data = {
                "file_path":file_path,
                "file_data": data,
            }
            send_to_client(conn, "large_update",header+send_data)
    
    # send end of file signal to server
    send_to_client(conn, "large_update", b'END')

# send delte request
def send_delete_file_request(conn,file_path):
    send_data = {
                "file_path":file_path,
                "file_data": None,
            }
    send_to_client(conn, "delete", send_data)
        

    