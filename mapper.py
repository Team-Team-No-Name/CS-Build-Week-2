import requests
from time import sleep
import json
from utils import Queue
from decouple import config

api_key = config('ADAM_KEY')


def initialize_room():
    room_data = []
    start_room = {
        "room_id": 0,
        "title": "A brightly lit room",
        "description": "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.",
        "coordinates": "(60,60)",
        "players": [],
        "elevation": 0,
        "terrain": "NORMAL",
        "items": [],
        "exits": ["n", "s", "e", "w"],
        "cooldown": 1.0,
        "errors": [],
        "messages": []
        }

    room_data.append(start_room)
    with open('room_data.txt', 'w') as rd:
        rd.write(json.dumps(room_data))

    # start with all unknowns
    room_conns = {}
    start_conns = {"0": {"n": "?", "s": "?", "e": "?", "w": "?"}}
    room_conns.update(start_conns)
    # parse to conn file
    with open("room_conns.txt", "w") as conns:
        conns.write(json.dumps(room_conns))


def explore(queue):
    room_id = str(room_data[-1]["room_id"])
    current_conns = room_conns[room_id]
    unchecked_conns = []
    for direction in current_conns:
        if current_conns[direction] == "?":
            unchecked_conns.append(direction)

    if unchecked_conns:
        queue.enqueue(unchecked_conns[0])
    else:
        unchecked_paths = bft(room_data, room_conns)
        if unchecked_paths is not None:
            for path in unchecked_paths:
                for direction in current_conns:
                    if current_conns[direction] == path:
                        queue.enqueue(direction)



def bft(room_data, room_conns):
    cue = Queue()
    cue.enqueue([str(room_data[-1]["room_id"])])
    visited = set()

    while cue.size() > 0:
        room_list = cue.dequeue()
        room = room_list[-1]
        if room not in visited:
            visited.add(room)
            for direction in room_conns[room]:
                if room_conns[room][direction] == "?":
                    return room_list
                else:
                    path = list(room_list)
                    path.append(room_conns[room][direction])
                    cue.enqueue(path)
    return None


initialize_room()

with open("room_data.txt", "r") as rdat:
    room_data = json.loads(rdat.read())

with open("room_conns.txt", "r") as rconn:
    room_conns = json.loads(rconn.read())

q2 = Queue()

explore(q2)

while q2.size() > 0:
    # Room information
    with open("room_data.txt", "r") as rdat:
        room_data = json.loads(rdat.read())
    # Room connections
    with open("room_conns.txt", "r") as rconn:
        room_conns = json.loads(rconn.read())

    player_room = str(room_data[-1]["room_id"])
    direction = q2.dequeue()
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={"direction": direction}, headers={'Authorization': api_key})
    data = res.json()
    room_data.append(data)

    new_room = str(room_data[-1]["room_id"])
    print("Now in Room:" + str(new_room))
    room_conns[player_room][direction] = new_room
    if new_room not in room_conns:
        exits = data["exits"]
        directions = {}
        for xit in exits:
            directions[xit] = "?"
        room_conns[new_room] = directions

    puddit_in_reverse_terry = {"n": "s", "s": "n", "e": "w", "w": "e"}
    reverse = puddit_in_reverse_terry[direction]
    room_conns[new_room][reverse] = player_room

    # Push it.. push it to the text files
    with open("room_data.txt", "w") as rdat:
        rdat.write(json.dumps(room_data))
    with open("room_conns.txt", "w") as rcon:
        rcon.write(json.dumps(room_conns))
    # rest my child
    sleep(data["cooldown"])
    explore(q2)
