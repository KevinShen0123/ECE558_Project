# ECE558_Project
1. Server(IP ,Port known, first to run the program, accept the incoming tcp connections,have /home/share for file syncronization), server store client ip/port , 
2. Other Node(VM), Before Join, Send Connect Request to Server, /home/share, may store all neighbor info
3. New Node, Before Join, send connect request to server, server store the client info(IP/port),may store all neighbor info
4. How to monitor file: MD5(if file is modified, md5 change, if change, notify all the neighbor,
5. f=open(), if open in binary, file to binary send to neighbor, decode from binary, add together.
6. 
