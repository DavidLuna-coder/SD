import argparse
import socket
import random

def main(host, port, n):
    s_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    below_counter = 0
    
    for i in range (0,int(n)):
        x = random.uniform(0,1)
        y = random.uniform(0,1)

        s_client.sendto("({},{})".format(x,y).encode("utf-8"),(host,int(port)))
        response,addr = s_client.recvfrom(1024)
        response = response.decode("utf-8")
        if response == "below":
            below_counter = below_counter + 1
    pi = 4.0 * float(below_counter) / float(n)
    print("El valor aproximado de pi con {} puntos aleatorios es {}".format(n,pi))
    s_client.sendto("exit".encode("utf-8"),(host,port))
    s_client.close()
    return 0
    
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()

    main(args.host, args.port, args.number)
