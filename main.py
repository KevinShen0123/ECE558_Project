import sys
import socket
import pickle
import threading

args = sys.argv
if len(args) == 1:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(500)
    socketarr = []
    #socketarr.append(['localhost', 12345])

    client_socket_arr = []
    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        client_socket_arr.append(client_socket)
        print(f"Accepted connection from {client_address}")


        client_add = client_socket.recv(1024).decode().split(' ')

        if len(client_add[0]) != 0:
            socketarr.append(client_add)
            serilizedarray = pickle.dumps(socketarr)
            for client_socket_item in client_socket_arr:
                client_socket_item.sendall(serilizedarray)


else:
    if len(args) > 1:

        def as_client():
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((args[1], int(args[2])))
            ary = args[3] + ' ' + args[4]

            client_socket.send(ary.encode())
            while True:
                nodes_array = client_socket.recv(4096)
                print(nodes_array)
                de_nodes_array = pickle.loads(nodes_array)
                print(de_nodes_array)
                for node in de_nodes_array:
                    node_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    node_client_socket.connect((node[0], int(node[1])))


        def as_sever():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (args[3], int(args[4]))
            print(server_address)
            server_socket.bind(server_address)
            server_socket.listen(500)
            while True:
                print("Waiting for a connection...")
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")


        thread_server = threading.Thread(target=as_sever)
        thread_clent = threading.Thread(target=as_client)
        thread_server.start()
        print("hello")
        thread_clent.start()
