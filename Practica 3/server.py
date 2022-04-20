import json
from bottle import run, request, response, get, post, put

#* Cargamos el json en memoria
with open('CommunicationJSON.json') as f:
    database = json.load(f)

class Room:
    def __init__(self,id,capacity,resources):
        self.roomId = id
        self.capacity = capacity
        self.resources = resources

class User:
    def __init__(self,dni,username,password):
        self.DNI = dni
        self.userName = username
        self.password = password

class Booking:
    def __init__(self,id,dni,date,startTime,endtime):
        self.bookingId = id
        self.DNI = dni
        self.date = date
        self.startTime = startTime
        self.endTime = endtime

rooms = [] #Lista de habitaciones
users = []  #Lista de Usuarios
bookinglist = [] #Lista de Reservas

#*Cargamos los datos en memoria
def carga():
    for index in database["rooms"]:
        rooms.append(Room(index["roomId"],index["capacity"],index["resources"]))

    for index in database["users"]:
        users.append(User(index["DNI"],index["userName"],["password"])) 
    
    for index in database["booking"]:
        bookinglist.append(Booking(index["bookingId"],index["DNI"],index["date"],index["startTime"],index["endTime"]))

#* Añadir Habitacion
@post('/addRoom')
def add_Room():
    data = request.json
    roomId = data["roomId"]
    capacity = data["capacity"]
    resources = data["resources"]
    for id in rooms:
        if data["roomId"] == id.roomId:
            raise ValueError
    rooms.append(Room(roomId,capacity,resources))
    dict_to_parse = {"roomId": roomId,"capacity": capacity,"resources":resources}
    database["rooms"].append(dict_to_parse)
    
    with open ('CommunicationJSON.json','w') as f:
        json.dump(database,f,indent=2)
        
@get('/showInformationRoom/<id:int>')
def show_Information_Room(id):
    for index in rooms:
        if index.roomId == id:
            break
    return json.dumps(index,indent = 2)

@post ('/addBooking')
def add_Booking():
    data = request.json
    lista = []
    id_exist = False
    for i in bookinglist:
        if i.bookingId == data['bookingId']:
            id_exist = True
            if i.DNI != None:
                error_Message = {'errorMessage':"La sala que desea reservar esta ocupada"}
                for j in bookinglist:
                    if j.startTime == data['startTime'] and j.endTime == data["endTime"] and j.DNI == None:
                        list.append(j)
                error_Message["booking"] = list
                return json.dumps(error_Message,indent = 2)
        break
                
    if id_exist == False:
        return json.dumps(database["errorMessage"])
    else:
        index = bookinglist[bookinglist.index(i)]
        i.DNI = data["DNI"]
        i.startTime = data["startTime"]
        i.endTime = data["endTime"]
        bookinglist[index] = i
        
        database["booking"][index]["DNI"] = i.DNI
        database["booking"][index]["startTime"] = i.startTime
        database["booking"][index]["endTime"] = i.endTime
        
        with open ('CommunicationJSON.json','w') as f:
            json.dump(database,f,indent=2)

@get('/showBookings/<userDni>')
def show_Bookings(userDni):
    list = []
    for i in bookinglist:
        if i.DNI == userDni:
            list.append(i)
    
    dict = {"bookings":list}
    return json.dumps(dict,indent = 2)

@post('deleteBooking/<bookingId>')
def delete_Booking(bookingId):
    exist = False
    for i in bookinglist:
        if i.bookingId == bookingId:
            exist = True
            bookinglist.remove(i)
            database['booking'].remove(i)
            break
    if exist == False:
        error_Message = {"errorMessage":"No existe identificador de la reserva"}
        return json.dumps(error_Message)
    with open ('CommunicationJSON.json','w') as f:
            json.dump(database,f,indent=2)
    return {"Message":"Reserva eliminada"}
    
            
if __name__ == '__main__':
    carga()
    run(host = 'localhost',port = 8080,debug=True)