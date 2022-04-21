import json
import datetime
from bottle import run, request, response, get, post, delete

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
    def __init__(self,roomId,id,dni,date,startTime,endtime):
        self.roomId = roomId
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
        users.append(User(index["DNI"],index["userName"],index["password"])) 
    
    for index in database["booking"]:
        bookinglist.append(Booking(index["roomId"],index["bookingId"],index["DNI"],index["date"],index["startTime"],index["endTime"]))


def login_status(userName,password):
    success = False
    for index in users:
        #print(str(index.userName) + " " + str(index.password))
        if index.userName == userName and index.password == password:
            success = True
            break
    return success

#* Añadir Habitacion
@post('/addRoom')
def add_Room():
    data = request.json
    if login_status(data["userName"],data["password"]):
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
        return "Sala añadida correctamente"
    else:
        return "Credenciales no Validas"
        
#Mostrar Informacion
@get('/showInformationRoom/<id:int>')
def show_Information_Room(id):
    data = request.json
    valido = False
    if login_status(data["userName"],data["password"]):
        for index in rooms:
            if index.roomId == id:
                formatData = {"roomId":index.roomId,"capacity":index.capacity,"resources":index.resources}
                valido = True
                break
        if valido == True:
            return json.dumps(formatData,indent = 2)
        else:
            return "ID de sala no valido"
    else:
        return "Credenciales no Validas"

@post ('/addBooking')
def add_Booking():
    data = request.json
    if login_status(data["userName"],data["password"]):
        for user in users:
            if user.userName == data["userName"]:
                DNI = user.DNI
        free_room = True
        room_exist = False
        print (data["date"] +" " + data["startTime"])
        startTime = datetime.datetime.strptime(data["date"] +" " + data["startTime"],"%d/%m/%Y %H:%M") 
        endTime = datetime.datetime.strptime(data["date"] +" " + data["endTime"],"%d/%m/%Y %H:%M")
        
        for i in rooms:
            if i.roomId == data["roomId"]:
                room_exist = True
                break
        for i in bookinglist:
            ts = datetime.datetime.strptime(i.date + " " + i.startTime,"%d/%m/%Y %H:%M")
            te = datetime.datetime.strptime(i.date + " " + i.endTime,"%d/%m/%Y %H:%M")
            checkTime = (startTime < ts and endTime < ts) or (startTime > te and endTime > te)
            if i.roomId == data["roomId"]:
                if not checkTime:
                    free_room = False
                else:
                    room_exist = True
                    break
                    
        
                    
        if free_room == False:
            errorMsg = "La sala que desea reservar esta ocupada"
            roomsinfo = []
            for i in rooms:
                has_booking = False
                for j in bookinglist:
                    if i.roomId == j.roomId:
                        has_booking = True
                        if j.date == data["date"]:
                            ts = datetime.datetime.strptime(j.date + " " + j.startTime,"%d/%m/%Y %H:%M")
                            te = datetime.datetime.strptime(j.date + " " + j.endTime,"%d/%m/%Y %H:%M")
                            checkTime = (startTime < ts and endTime < ts) or (startTime > te and endTime > te)
                            if checkTime:
                                roomsinfo.append({"roomId":i.roomId,"capacity":i.capacity,"resources":i.resources})
                
                if not has_booking:
                    roomsinfo.append({"roomId":i.roomId,"capacity":i.capacity,"resources":i.resources})
                    
                    
                        
            return json.dumps({"errorMessage":errorMsg,"rooms":roomsinfo})
        elif free_room:
            bookingId = bookinglist[len(bookinglist) - 1].bookingId + 1
            roomId = data["roomId"]
            date = data["date"]
            start_Time = data["startTime"]
            end_Time = data["endTime"]
            
            bookinglist.append(Booking(roomId,bookingId,DNI,date,start_Time,end_Time))
            dict = {"bookingId":bookingId,"roomId":roomId,"DNI":DNI,"date":date,"startTime":start_Time,"endTime":end_Time}
            database["booking"].append(dict)
            
            with open ('CommunicationJSON.json','w') as f:
                json.dump(database,f,indent=2)
            return json.dumps({"message": "Reserva anadida :-)"})
        elif not room_exist:
            return json.dumps({"errorMessage":"La sala no existe"})
    else:
        return json.dumps({"errorMessage": "Credenciales no Validas"})

@get('/showBookings/<userDni>')
def show_Bookings(userDni):
    data = request.json
    if login_status(data["userName"],data["password"]):
        list = []
        for i in bookinglist:
            if i.DNI == userDni:
                dict = {"bookingId":i.bookingId,"roomId":i.roomId,"DNI": i.DNI,"startTime":i.startTime,"endTime": i.endTime}
                list.append(dict)
        
        dict = {"bookings":list}
        
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(dict,indent = 2)
    else:
        return json.dumps({"errorMessage":"Credenciales no Validas"})

@delete('/deleteBooking/<bookingId:int>')
def delete_Booking(bookingId):
    data = request.json
    if login_status(data["userName"],data["password"]):
        exist = False
        for user in users:
            if user.userName == data["userName"]:
                DNI = user.DNI
                break
        for i in bookinglist:
            if i.bookingId == bookingId:
                if i.DNI != DNI:
                    return json.dumps({"errorMessage": "No puedes eliminar una reserva que no te pertenece"})
                else:
                    exist = True
                    index = bookinglist.index(i)
                    bookinglist.remove(i)
                    data_to_remove = {"booking"}
                    del database['booking'][index]
                    break
        if exist == False:
            error_Message = {"errorMessage":"No existe identificador de la reserva"}
            return json.dumps(error_Message)
        else:
            with open ('CommunicationJSON.json','w') as f:
                    json.dump(database,f,indent=2)
        return {"Message":"Reserva eliminada"}
    else:
        return "Credenciales no Validas"
    
            
if __name__ == '__main__':
    carga()
    run(host = 'localhost',port = 8080,debug=True)