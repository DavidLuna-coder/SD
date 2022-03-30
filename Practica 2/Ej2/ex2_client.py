import argparse
import socket
import os
def main(host, port, filein, fileout):
    port = int(port)
    s_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_client.connect((host,port))
    if not os.path.exists(filein):
        raise OSError
    
    f = open(filein,"r")    
    text = f.read()
    f.close()
    
    s_client.send(text.encode("utf-8"))
    length = s_client.recv(1024).decode("utf-8")
    wordlist = s_client.recv(1024).decode("utf-8")
    wordlist = wordlist.replace(",","").replace("[","").replace("]","").replace("'","").split()
    f = open(fileout,"w")
    for i in wordlist:
        f.write(i + "\n")
    f.close()
    s_client.close()
    # ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--filein', default='filein.txt', help="file to be read")
    parser.add_argument('--fileout', default='fileout.txt', help="file to be written")
    args = parser.parse_args()

    main(args.host, args.port, args.filein, args.fileout)
