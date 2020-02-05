import json
import requests
from operations import Operations
from utils import Queue
from time import sleep
from decouple import config

api_key = config("DAKOTA_KEY")


class Player:
    def __init__(self):
        self.op = Operations()
        self.op.init_player()

    def sticky_fingers(self, current_room, item):
        room_data = []
        with open("room_data.txt", "r") as dat:
            room_data = json.loads(dat.read())

        self.go(current_room, item)
        data = self.op.take()
        for room in room_data:
            if room['room_id'] == current_room:
                if len(room['items']) > 0:
                    room['items'] = []
        with open("room_data.txt", "w") as da:
            da.write(json.dumps(room_data))
        if data:
            return True
        return False

    def go(self, current_room, end_room):
        room_data = []
        room_conns = {}
        with open("room_data.txt", "r") as rdat:
            room_data = json.loads(rdat.read())
        with open("room_conns.txt", "r") as rcon:
            room_conns = json.loads(rcon.read())
        print('Going to ', str(end_room))
        traversing = self.traverse(room_conns, room_data, current_room, end_room)
        if not traversing:
            print("Cant get there")
            return
        for step in range(len(traversing)):
            data = {}
            print('Walking')
            next_room = room_conns[str(current_room)][traversing[step]]
            data = self.op.move(traversing[step])
            # if "cooldown" in data:
            #     sleep(data["cooldown"])
            #     break

            current_room = str(data['room_id'])
            sleep(data["cooldown"])
            print(data)

    def traverse(self, room_conns, room_data, room_id, end_room):
        cue = Queue()
        checked = set()
        paths = {}
        cue.enqueue(room_id)
        paths[room_id] = [room_id]

        while cue.size() > 0:
            current = cue.dequeue()
            checked.add(current)
            for possibles in room_conns[str(current)].values():
                if possibles in checked or possibles == "?":
                    continue
                new = paths[current][:]
                new.append(possibles)
                paths[possibles] = new
                found = False
                for data in room_data:
                    if possibles == str(data['room_id']):
                        if data['title'].lower() == end_room.lower():
                            found = True
                            break
                        if 'items' in data and 'small treasure' in data['items']:
                            found = True
                            break
                        elif 'items' in data and 'tiny treasure' in data['items']:
                            found = True
                            break
                if possibles == end_room:
                    found = True
                if found:
                    the_path = paths[possibles]
                    exits = []
                    for step in range(len(the_path) - 1):
                        exits.append(self.compass(room_conns, str(the_path[step]), the_path[step + 1]))
                        return exits
                cue.enqueue(possibles)
        return None

    def compass(self, room_conns, room_id, next):
        for connection, room in room_conns[room_id].items():
            if room == next:
                return connection
        return None
