import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode()
    client.send(message)
    print(client.recv(2048).decode())

send("GET /test.html HTTP/1.1\r\n")
client.close()