import socket

# HOST = 'localhost'
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 1025
REMOTE_ADDR = (REMOTE_HOST, REMOTE_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(REMOTE_ADDR)

print("Sending a message...")
buffer = "A message.".encode("utf-8")
s.send(buffer)

s.close()