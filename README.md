# ECE558_Project
1. Server(IP ,Port known, first to run the program, accept the incoming tcp connections,have /home/share for file syncronization), server store client ip/port , 
2. Other Node(VM), Before Join, Send Connect Request to Server, /home/share, may store all neighbor info
3. New Node, Before Join, send connect request to server, server store the client info(IP/port),may store all neighbor info
4. How to monitor file: MD5(if file is modified, md5 change, if change, notify all the neighbor)
5. f=open(), if open in binary, file to binary send to neighbor, decode from binary, add together.
More:
1. Server can have an thread reponsible for notify nodes, to send all nodes with topology information(IP,in dictionary?)
2. Other part of server can serve as a normal node for syncronizing file /home/share 
3. Client can have a thread for receiving and communicating topology information
Drawback:May take a lot of time and increase complexity
#ECE558 Project Solution 2:
server need send topology information to all client.
New Change: When a node has file change, notify server first,server then send the information(maybe IP,filename, new file content) to all other clients,server can have file changed.
Drawback:When server shut down, the system can't work
Maybe have a server election,consensus,maybe can have new connect.
   Common:
   1. File mpnitor By MD5,return filename, readfile,f=open("file","rb")
   2. 

Before 11.20 have file monito logic
Before 11.27 have Overall implemented project prototype
11.27-final Presentation, Testing, Add Extra functions,Demo,Report
We finalized with solution 1.
   
   
