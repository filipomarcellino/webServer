import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
     
server.listen()
print("[STARTING] server is starting...")
print(f"[LISTENING] Server is listening on {SERVER}")
previous = ""
while True:
    conn, addr = server.accept()
    req = conn.recv(1024).decode()
    filename =  req.split()[1] #/test.html
    if  req.split()[0] != 'GET' or   req.split()[2] != 'HTTP/1.1':
        res = 'HTTP/1.1 400 BAD REQUEST\r\n\r\n'
    elif filename != '/test.html':
        res = 'HTTP/1.1 404 NOT FOUND\r\n\r\n%s Not Found' % filename
    elif filename == '/test.html':
        file = open(filename[1:])
        output = file.read()
        #if the contect is not identical to the previous content
        if output != previous:
            previous = output
            res = 'HTTP/1.1 200 OK\n\n' + output 
        else:
            res = 'HTTP/1.1 304 NOT MODIFIED\n\nNot Modified'
        file.close()
    conn.send(res.encode())
    conn.close()
