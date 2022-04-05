import argparse
import socket
import math
import re
def f(x):
    return math.sqrt(1-math.pow(x,2))
 
def main(host, port):
    s_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s_server.bind((host,int(port)))
    
    while True:
        msg,addr = s_server.recvfrom(1024)
        data = msg.decode("utf-8")
        if data == "exit":
            break
        pattern = "[0-9].[0-9]+e?[0-9]+"
        numbers = re.findall(pattern,data)
        x,y = numbers
        x = float(x)
        y = float(y)
        
        if  (y < 0.0 or y > 1.0) or x > 1.0 or x < 0.0:
            s_server.sendto("error".encode("utf-8"),addr)
            
        elif y < f(x):
            s_server.sendto("below".encode("utf-8"),addr)
        
        else:
            s_server.sendto("above".encode("utf-8"),addr)
    s_server.close()
# ...

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
