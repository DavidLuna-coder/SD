import socket

# HOST = 'localhost'
HOST = '127.0.0.1'
PORT = 1025

s_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_listener.bind((HOST, PORT))

print("Waiting for client connections...")
s_listener.listen()
s_for_client, addr_c = s_listener.accept()

print("A new client in the address: " + str(addr_c))
print("Waiting for client messages...")
buffer = s_for_client.recv(512)
print("Received message: '" + buffer.decode("utf-8") + "'")

s_for_client.close()
s_listener.close()
