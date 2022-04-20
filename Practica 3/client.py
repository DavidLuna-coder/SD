import json
import requests

def menu():
    print("1. Añadir sala\n2. Mostrar información de sala\n3. Añadir reserva\n4. Listar reservas\n5. Eliminar reserva\n6. Exit".format("utf-8"))
    
def anadir_sala():
    print("Introduce el ID de la sala: ")
    roomId = int(input())
    print("Introduce la capacidad de la sala: ")
    capacity = int(input())
    print("Introduce los recursos de la sala separado por un espacio")
    resources = str(input()).split(" ")
    response = requests.post("http://localhost:8080/addRoom",json = {"roomId":roomId,"capacity":capacity, "resources":resources})

def mostrar_info_sala():
    print("Info mostrada")
    
def anadir_reserva():
    print("Reserva anadida")
    
def listar_reserva():
    print("Lista de reservas")

def eliminar_reserva():
    print("reserva Eliminada")

if __name__ == '__main__':
    menu()
    opcion = input()
    anadir_sala()