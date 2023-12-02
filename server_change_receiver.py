import time
import os
import socket
from server_connection import send_to_client,lock
from server_broadcast import update_broadcast_message, delete_broadcast_message

file_status_dict = {}

def update_file_status(file_path):
    current_time = time.time()
    with lock:
        file_status_dict[file_path] = current_time

def remove_file_status(file_path):
    with lock:
        del file_status_dict[file_path]

def handle_receive_update(save_path, file_data, client_socket):
    result, timestamp = check_file_status(save_path)
    
    if result:
        with open(save_path, 'wb') as file:
            with lock:
                file.write(file_data)
        print("File received completely.")
        # update the file status
        file_path = save_path
        if file_path in file_status_dict:
            update_file_status(file_path)
        else:
            update_file_status(file_path)
        message_type = "confirmation"
        send_data = {
            "result": "SUCCESS",
            "file_path": file_path
        }
        send_to_client(client_socket,message_type,send_data)
        update_broadcast_message(file_path)
    else:
        # The only possibility for a failed change is that the file has been deleted
        message_type = "confirmation"
        send_data = {
            "result": "FAIL",
            "file_path": file_path
        }
        send_to_client(client_socket,message_type,send_data)

def handle_receive_add(save_path, file_data):
    handle_receive_update(save_path, file_data)

def handle_receive_delete(delete_path):
    result, timestamp = check_file_status(delete_path)

    if result:
        if os.path.exists(delete_path):
            with lock:
                os.remove(delete_path)
            remove_file_status(delete_path)
            delete_broadcast_message(delete_path)


def check_file_status(file_path):
    if file_path in file_status_dict:
        operation_type, timestamp = file_status_dict[file_path]
        return True, operation_type, timestamp
    return False, None, None