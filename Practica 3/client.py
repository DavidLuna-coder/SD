import json
import datetime
import requests

def menu():
    print("1. Añadir sala\n2. Mostrar información de sala\n3. Añadir reserva\n4. Listar reservas\n5. Eliminar reserva\n6. Exit".format("utf-8"))
    
def anadir_sala():
    usuario = iniciar_sesion()
    roomId = int(input("Introduce el ID de la sala: "))
    capacity = int(input("Introduce la capacidad de la sala: "))
    resources = str(input("Introduce los recursos de la sala separado por un espacio: ")).split(" ")
    response = requests.post("http://localhost:8080/addRoom",json = {"roomId":roomId,"capacity":capacity, "resources":resources, "userName":usuario[0], "password":usuario[1]})
    print (response.text)

def mostrar_info_sala():
    usuario = iniciar_sesion()
    idSala = int(input("Introduce el id de la sala: "))
    response = requests.get("http://localhost:8080/showInformationRoom/{id}".format(id = idSala),json= {"userName": usuario[0],"password":usuario[1]})
    print(response.text)
    
def anadir_reserva():
    usuario = iniciar_sesion()
    idSala = input("Introduce el id de la sala que quiere reservar: ")
    Fecha = input("Introduce la fecha de la reserva formato DD/MM/AAAA: ")
    try:
        datetime.datetime.strptime(Fecha,"%d/%m/%Y")
    except:
        print("---- ERROR: FECHA EN FORMATO INCORRECTO ----\n")
    startTime = input("Introduce la hora de inicio de la reserva, formato HORAS:MINUTOS : ")
    try:
        ts = datetime.datetime.strptime(startTime,"%H:%M")
    except:
        print("---- ERROR: HORA EN FORMATO INCORRECTO ----\n")
        return
    endTime = input("Introduce la hora del fin de la reserva, formato HORA:MINUTOS : ")
    try:
        te = datetime.datetime.strptime(endTime,"%H:%M")
    except:
        print("---- ERROR: HORA EN FORMATO INCORRECTO ----\n")
        return
    try:   
        if (te <= ts):
            raise 
    except:
        print("---- ERROR: Hora de finalización < Hora de entrada ----\n")
        return
    
    send = {"userName":usuario[0],"password":usuario[1],"roomId":idSala,"date":Fecha,"startTime":startTime,"endTime":endTime}
    response = requests.post("http://localhost:8080/addBooking",json=send)
    print (response.text)
    
def listar_reservas():
    usuario = iniciar_sesion()
    userDNI = input("Introduce el DNI del usuario a consultar: ")
    response = requests.get("http://localhost:8080/showBookings/{dni}".format(dni=userDNI),json={"userName": usuario[0],"password":usuario[1]})
    print(response.text)

def eliminar_reserva():
    usuario = iniciar_sesion()
    bookingId = input("Introduce la id de la reserva a eliminar: ")
    response = requests.delete("http://localhost:8080/deleteBooking/{id}".format(id = bookingId),json={"userName": usuario[0],"password":usuario[1]})
    print(response.text)

    
def iniciar_sesion():
    usr_name = input("Introduce tu nombre de usuario: ")
    password = input("Introduce tu contraseña: ")
    return usr_name,password
    

def opcion_elegida(opcion):
    if opcion == 1:
        anadir_sala()
    elif opcion == 2:
        mostrar_info_sala()
    elif opcion == 3:
        anadir_reserva()
    elif opcion == 4:
        listar_reservas()
    elif opcion == 5:
        eliminar_reserva()
    elif opcion == 6:
        return 0
    
            
                
if __name__ == '__main__':
    while True:
        menu()
        opcion = int(input())
        opcion_elegida(opcion)
        if opcion == 6:
            break
    