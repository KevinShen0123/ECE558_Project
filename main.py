import sys
import socket
import pickle
import threading
from server_connection import *
from client_p2p_connection import *
# prepare for final merge
global socket_array
if len(sys.argv) == 1:#The code for server side
   def handle_connection(server_socket):
       client_socket_dic = []  # record ip and port only,through recv from client,which is ip port
       lock = threading.Lock
       socket_array = []
       global socket_array
       while True:
           print("Waiting for a connection...")
           client_socket, client_address = server_socket.accept()
           socket_array.append(client_socket)  # remeber all the socket
           client_info_str = client_socket.recv(1024)
           client_info_str=pickle.load(client_info_str)
           client_info_list = client_info_str.split(" ")
           client_ip = client_info_list[0]
           client_port = int(client_info_list[1])
           with lock:
               client_socket_dic.append([client_ip, client_port])
               for socket in socket_array:
                   socket.send(pickle.dumps(client_socket_dic))
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_address = ('localhost', 12345)
   server_socket.bind(server_address)
   server_socket.listen(1000)
   connectionhandler=threading.Thread(target=handle_connection, args=(server_socket))
   connectionhandler.start()
   def client_handler(client_socket):
       try:
          handle_client(client_socket)
       except:
           socket_array.remove(socket_array.index(client_socket))
   for myclient in socket_array:
       clienthandler = threading.Thread(target=clienthandler, args=(server_socket,myclient))
       clienthandler.start()
else:
   if len(sys.argv)<5:
       print("wrong format!")
       exit(0)
   #  client side logic
   server_ip=sys.argv[1]
   server_port=int(sys.argv[2])
   client_entry_thread=threading.Thread(target=client_entry,args=((server_ip,server_port,sys.argv[3],int(sys.argv[4]))))
   client_entry_thread.start()