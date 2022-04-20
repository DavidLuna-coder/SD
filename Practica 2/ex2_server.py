import argparse
import socket
import re
def main(host, port):
    port = int(port)
    s_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_listener.bind((host,port))
    s_listener.listen()
    s_for_client,addr = s_listener.accept()
    tam_buffer = int(s_for_client.recv(8).decode("utf-8"))
    s_for_client.send("Check".encode("utf-8"))
    
    file = s_for_client.recv(tam_buffer).decode("utf-8")
    pattern = "[a-zA-Z]*[aA]+[a-zA-Z]*"
    words = re.findall(pattern,file)
    s_for_client.send(str(len(words)).encode("utf-8"))
    s_for_client.send(str(words).encode("utf-8"))
    s_for_client.close()
    s_listener.close()
    # ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
