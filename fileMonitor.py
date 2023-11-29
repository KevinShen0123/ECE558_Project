# File change detection
import hashlib
import os
import time
import json
import Client
import File

# Calculate the MD5 checksum of the file at the given path
def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)
    return hasher.hexdigest()

# Use recurssion to get all file pathes
def get_all_paths(directory_path,all_file_paths=None):
    if all_file_paths == None:
        all_file_paths = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path,filename)
        if os.path.isfile(file_path):
            all_file_paths.append(file_path)
        if os.path.isdir(file_path):
            get_all_paths(file_path,all_file_paths)
    return all_file_paths

# This function returns a dictionary representing the current state of the directory
# This dictionary maps file names to their MD5 checksums
def get_directory_state(directory_path):
    directory_state = {}
    all_files = get_all_paths(directory_path)

    for file_path in all_files:
        directory_state[file_path] = calculate_md5(file_path)
    return directory_state

# This function aims at continuously monitoring the given directory
# change the interval value to reset how often a directory is checked (in seconds)
# if a change is detected, the new file will be sent in the binary form along with its corresponding path(in JSON format)
# handle change is a call back function
def monitor_directory(directory_path, interval=10, handle_change=None):
    last_state = None
    while True:
        current_state = get_directory_state(directory_path)
        changes = []

        if last_state is not None:
            added = current_state.keys() - last_state.keys()
            removed = last_state.keys() - current_state.keys()
            modified = {file_path for file_path in current_state.keys() & last_state.keys()
                        if current_state[file_path] != last_state[file_path]}
            
            for file_path in added:
                changes.append({"action":"added", "file_path":file_path})
            for file_path in removed:
                changes.append({"action":"removed","file_path":file_path})
            for file_path in modified:
                with open(file_path,'rb') as f:
                    buffer = f.read()
                    changes.append({"action":"modified","file_path":file_path,"buffer":buffer})
            
            if changes:
                response = json.dumps(changes)
                handle_change(response)
        
        last_state = current_state
        time.sleep(interval)

# callback function that responsible to send the response to all nodes within the network (a dummy function now)
def handle_change(res):
    # load string
    changes = json.loads(res)

    for change in changes:
        file_path = change['file_path']
        action = change['action']

        # encoding the file buffer for 'added' or 'modified' files
        file_buffer = change.get('buffer', None)
        if file_buffer is not None:
            file_buffer = file_buffer.decode('latin-1')  # convert to a string for JSON compatibility

        # Creating a FileObject
        file_obj = File.FileObject(file_path, action, file_buffer)
        
        # need to set login credentials
        # file_obj.set_login_info(username, password)  

        # Convert to JSON and broadcast to all nodes
        file_info_json = file_obj.to_json()
        Client.broadcast_file_info_to_nodes(file_info_json)  # Broadcast to all nodes

# How to use this monitor
directory_to_monitor = "" # change the directory here
monitor_directory(directory_to_monitor)