# This module is responsible for keep the log information

def print_success_log(addr,file_path,action):
    print("Connection from {}, file path is {}, action is{}".format(addr,file_path,action))

def print_error_login_log(addr):
    print("Connection from {} is rejected due to wrong username and/or password".format(addr))

def print_success_send_log():
    print("Hello")