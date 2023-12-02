import socket
import os
from client_p2p_connection import getConnection, send_to_server

# Send data over existing connection
def send_data_over_existing_connection(file_path):  
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
            conn = getConnection()
            send_to_server(conn, "small_update", send_data)
    send_to_server(conn, "small_update", b'END')
    
    # wait for the server to respond
    # response = conn.recv(1024).decode()
    # if response == 'SUCCESS':
    #     print("File {} transferred successfully.".format(file_path))
    #     return
    # if response == 'RESEND':
    #     send_data_over_existing_connection(file_path, count=count+1)

# Chunk the data and then send data over existing connection
def send_chunked_data_over_existing_connection(file_path, chunk_size=1024*1024*5):
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size // chunk_size) + (1 if file_size % chunk_size > 0 else 0)
    conn = getConnection()

    with open(file_path,'rb') as file:
        for chunk_num in range(total_chunks):
            data = file.read(chunk_size)
            header = f"{len(data):010d}:{chunk_num:010d}".encode()
            send_data = {
                "file_path":file_path,
                "file_data": data,
            }
            send_to_server(conn, "large_update",header+send_data)
    
    # send end of file signal to server
    send_to_server(conn, "large_update", b'END')

# send delte request
def send_delete_file_request(file_path):
    conn = getConnection()
    send_data = {
                "file_path":file_path,
                "file_data": None,
            }
    send_to_server(conn, "delete", send_data)