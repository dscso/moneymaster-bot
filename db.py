import time
from collections import defaultdict
import json, os

class Ticket():
    def __init__(self, amount:float=0, description:str="not specified"):
        self.amount = amount
        self.description = description
        self.timestamp = time.time()
    def getAmount(self):
        return self.amount
    def getDescription(self):
        return self.description
    def getTime(self):
        return self.timestamp
    def fromJson(self, json):
        self.amount = json['amount']
        self.description = json['description']
        self.timestamp = json['timestamp']
        return self

class Group():
    def __init__(self, id:int):
        self.chat_id:int = id
        self.tickets:Dict[int, List[Ticket]] = defaultdict(dict)
        self.currency:str = "RUB"
        self.users:Dict[int, str] = defaultdict(dict)
    def getID(self):
        return self.chat_id
    def setName(self, data):
        self.setNameFast(data.id, "{} {}".format(isinstance(data.first_name, str) and data.first_name or "NoName", isinstance(data.last_name, str) and data.last_name or ""))
    def setNameFast(self, uid:int, name:str):
        self.users[uid] = name
    def getName(self, uid):
        return self.users.get(uid, "Unknown User")
    def getAllNames(self):
        return self.users
    def addGroupMember(self, user:int):
        if not isinstance(self.tickets[user], list):
            self.tickets[user] = []
    def addTicket(self, user:int, ticket:Ticket):
        self.addGroupMember(user)
        self.tickets[user].append(ticket)
    def getTickets(self):
        return self.tickets
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            indent=4, sort_keys=True)
    def save(self):
        with open('db/'+str(self.chat_id)+'.json','w') as out:
            out.write(self.toJSON())


class DB():
    def __init__(self):
        self.groups: Dict([int, Group]) = {}
    def getGroup(self, groupID:int):
        if not groupID in self.groups:
            self.groups[groupID] = Group(groupID)
        return self.groups[groupID]
    def removeGroup(self, gid:int):
        self.groups.pop(gid)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def saveDB(self):
        for groupid, group in self.groups.items():
            group.save()

    def loadDB(self):
        for filename in os.listdir('db'):
            with open('db/'+filename) as json_file:
                data = json.load(json_file)
                group = self.getGroup(data['chat_id'])
                for user, name in data['users'].items():
                    group.setNameFast(int(user), name)
                for owner, tickets in data['tickets'].items():
                    for ticket in tickets:
                        group.addTicket(int(owner), Ticket().fromJson(ticket))
        