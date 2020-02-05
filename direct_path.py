import json
import requests
from decouple import config
from utils import Queue
from time import sleep
from player import Player
from operations import Operations

player = Player()
ops = Operations()
api_key = config("DAKOTA_KEY")

with open("room_conns.txt", "r") as conns:
    room_conn = json.loads(conns.read())

# {
#     "room_id": 148,
#     "title": "A misty room",
#     "description": "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.",
#     "coordinates": "(56,57)",
#     "elevation": 0,
#     "terrain": "NORMAL",
#     "players": [],
#     "items": [],
#     "exits": [
#         "e",
#         "w"
#     ],
#     "cooldown": 1.0,
#     "errors": [],
#     "messages": []
# }
current_room = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers={'Authorization': api_key}).json()


def bfs(current_room, end_room):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    q = Queue()
    q.enqueue([current_room])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if v == end_room:
                return path
            visited.add(v)
            for key, value in room_conn[str(v)].items():
                new_path = list(path)
                new_path.append(value)
                q.enqueue(new_path)
    return None


def go_to_room(current_room, end_room):
    fast_paths = bfs(current_room["room_id"], end_room=end_room)
    print(fast_paths)
    routes = []
    for ind in range(len(fast_paths)):
        for direc in ["n", "e", "w", "s"]:
            try:
                if room_conn[str(fast_paths[ind])][direc] == fast_paths[ind + 1]:
                    routes.append(direc)
            except KeyError:
                None
            except IndexError:
                None
    counter = 0
    while current_room['room_id'] != end_room:
        for dirs in routes:
            if counter < len(fast_paths):
                sleep(current_room['cooldown'])
                next_room = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={"direction": str(dirs)}, headers={'Authorization': api_key}).json()
                current_room = next_room
                print(current_room)
                counter += 1
            else:
                break


def sell(item="tiny treasure"):
    if current_room['title'] != 'Shop':
        print("You should go to the shop to sell")
    else:
        sleep(current_room["cooldown"])
        # res1 = requests.post(" https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={"name": item}, headers={'Authorization': api_key}).json()
        # print(res1)
        # sleep(res1["cooldown"])
        res = requests.post(" https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={"name": item, "confirm": "yes"}, headers={'Authorization': api_key}).json()
        print(res)
        sleep(res["cooldown"])

def examine(item='Well'):
    sleep(current_room["cooldown"])
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/", json={"name": item}, headers={'Authorization': api_key}).json()
    with open("well_code.txt","w") as wc:
        wc.write(res['description'])
    sleep(res["cooldown"])


# sell()
# ops.status_check()
# ops.change_name("D Wandering Beard")
# examine('Well')
# List of important room numbers

shop = '1'
namer = '467'
speed_shrine = '461'
warp_shrine = '374'
gold_shrine = '499'
sandovsky_statue = '492'
aarons_athenaeum = '486'
well = '55'
mine = '255'

go_to_room(current_room, mine)
