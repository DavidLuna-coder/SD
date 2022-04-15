import json
from requests import post
with open('CommunicationJSON.json') as f:
    database = json.load(f)

class Room:
    def __init__(self,id,capacity,resources):
        self.roomId = id
        self.capacity = capacity
        self.resources = resources

data = {"roomId": 5,"capacity":229,"resources":["cable","monitor"]}
roomId = data["roomId"]
capacity = data["capacity"]
resources = data["resources"]
for id in database['rooms']:
    if id["roomId"] == roomId:
        raise ValueError
room = Room(roomId,capacity,resources)
dict_to_parse = {"roomId": roomId,"capacity": capacity,"resources":resources}
database["rooms"].append(dict_to_parse)
    
with open ('CommunicationJSONTEST.json','w') as f:
    json.dump(database,f,indent=2)

    