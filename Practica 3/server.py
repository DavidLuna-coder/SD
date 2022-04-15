import json
from bottle import run, request, response, get, post, put

with open('CommunicationJSON.json') as f:
    database = json.load(f)

class Room:
    def __init__(self,id,capacity,resources):
        self.roomId = id
        self.capacity = capacity
        self.resources = resources
    
@post('/addRoom')
def add_Room():
    data = request.json
    roomId = data["roomId"]
    capacity = data["capacity"]
    resources = data["resources"]
    for id in database['rooms']:
        if id["roomId"] == roomId:
            raise ValueError
    room = Room(roomId,capacity,resources)
    dict_to_parse = {"roomId": roomId,"capacity": capacity,"resources":resources}
    database["rooms"].append(dict_to_parse)
    
    with open ('CommunicationJSON.json','w') as f:
        json.dump(database,f,indent=2)
        
@get('/showInformationRoom/<id:int>')
def show_Information_Room(id):
    for index in database['rooms']:
        if index['roomId'] == id:
            break
    return json.dumps(index,indent = 2)

@post ('/addBooking')
def add_Booking():
    data = request.json
    lista = []
    id_exist = False
    for i in data['booking']:
        if i['bookingId'] == database['bookingId']:
            id_exist = True
            if i['DNI'] != "":
                error_Message = {'errorMessage':"La sala que desea reservar esta ocupada"}
                for j in database['booking']:
                    if j['startTime'] == data['startTime'] and j["endTime"] == data["endTime"] and j['DNI'] == "":
                        list.append(j)
                error_Message["booking"] = list
                return json.dumps(error_Message,indent = 2)
        break
                
    if id_exist == False:
        return json.dumps(database["errorMessage"])
    else:
        database["booking"].append(data)
        with open ('CommunicationJSON.json','w') as f:
            json.dump(database,f,indent=2)

@get('/showBookings/<userDni>')
def show_Bookings(userDni):
    list = []
    for i in database["bookings"]:
        if i["DNI"] == userDni:
            list.append(i)
    
    dict = {"bookings":list}
    return json.dumps(dict,indent = 2)

@post('deleteBooking/<bookingId>')
def delete_Booking(bookingId):
    exist = False
    for i in database['booking']:
        if i['bookingId'] == bookingId:
            exist = True
            database['booking'].remove(i)
            break
    if exist == False:
        error_Message = {"errorMessage":"No existe identificador de la reserva"}
        return json.dumps(error_Message)
    with open ('CommunicationJSON.json','w') as f:
            json.dump(database,f,indent=2)
    return {"Message":"Reserva eliminada"}
    
            
                