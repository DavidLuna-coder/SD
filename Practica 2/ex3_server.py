import argparse
import socket
import numpy as np
def main(host, port):
    # ...
    s_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s_server.bind((host,port))
    #* Nombre J1
    nombreJ1,addr_j1 = s_server.recvfrom(16)
    nombreJ1 = nombreJ1.decode("utf-8")
    #* Tablero J1
    tableroJ1 = s_server.recvfrom(1024)[0]
    tableroJ1 = tableroJ1.decode("utf-8")
    tableroJ1 = np.array(np.mat(tableroJ1),dtype=int)

    #* Nombre J2
    nombreJ2,addr_j2 = s_server.recvfrom(16)
    nombreJ2 = nombreJ2.decode("utf-8")
    #* Tablero J2
    tableroJ2 = s_server.recvfrom(1024)[0]
    tableroJ2 = tableroJ2.decode("utf-8")
    tableroJ2 = np.array(np.mat(tableroJ2),dtype=int)

    id = 1
    acabar = False
    next = True
    addr = addr_j1
    while acabar == False:
        
        s_server.sendto(("Turn " + str(id)).encode("utf-8"),addr)
        
        #* Guardar coordenadas y el jugador atacante
        
        coords,atacante_addr = s_server.recvfrom(1024)
        coords = coords.decode("utf-8")
        i = int(coords[1]) - 1
        j = ord(coords[0]) - 65
        

        #* Guardar jugador defensor y tablero
        if atacante_addr == addr_j1:
            tablero = tableroJ2
            defensor_addr = addr_j2
        else:
            tablero = tableroJ1
            defensor_addr = addr_j1
        
        #* Disparo fallado
        if tablero[i][j] == 0:
            id = id + 1
            addr = defensor_addr
            s_server.sendto("Fail".encode("utf-8"),atacante_addr)
        
        #* Disparo acertado
        elif tablero[i][j] == 1:
            id = id + 1
            addr = atacante_addr
            tablero[i][j] = 0
            #* Tablero no Vacio
            if not np.all(tablero == np.zeros((10,10),dtype=int)):
                s_server.sendto("Hit".encode("utf-8"),atacante_addr)
            #* Tablero Vacio
            else:  
                s_server.sendto("You win".encode("utf-8"),atacante_addr)
                s_server.sendto("You lost".encode("utf-8"),defensor_addr)
                acabar = True
        
    s_server.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
