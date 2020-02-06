import json
import requests
from utils import Queue
from player import Player
from operations import Operations
from time import sleep
from decouple import config

api_key = config('ADAM_KEY')


player = Player()
ops = Operations()
# api_key = "Token 26b3338051c40210c961c3080dfd3e7f292a58e0"

with open("room_conns.txt", "r") as conns:
    room_conn = json.loads(conns.read())

current_room = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init', headers={'Authorization': api_key}).json()

def bfs(current_room, end_room):
    cue = Queue()
    cue.enqueue([current_room])
    visited = set()
    while cue.size() > 0:
        path = cue.dequeue()
        v = path[-1]
        if v not in visited:
            if v == end_room:
                return path
            visited.add(v)
            for key, value in room_conn[str(v)].items():
                new_path = list(path)
                new_path.append(value)
                cue.enqueue(new_path)
    return None

def go_to_room(current_room, end_room):
    fast_paths = bfs(current_room["room_id"], end_room=mine)
    print(fast_paths)
    routes = []
    for ind in range(len(fast_paths)):
        for direc in ["n", "s", "e", "w"]:
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
                next_room = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move", json={"direction": str(dirs)}, headers={"Authorization": api_key}).json()
                current_room = next_room
                print(current_room)
                counter += 1
            else:
                break

def sell(item="small treasure"):
    if current_room['title'] != "Shop":
        print('You re not in the shop')
    else: 
        sleep(current_room["cooldown"])
        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell", json={"name": item, "confirm": "yes"}, headers={"Authorization": api_key}).json()
        print(res)
        sleep(res["cooldown"])

def examine(item="Well"):
    sleep(current_room["cooldown"])
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/examine", json={"name": item}, headers={"Authorization": api_key}).json()
    print(res)
    with open("well.txt", "w") as wc:
        wc.write(res['description'])
    sleep(res["cooldown"])


#examine()
#ops.status_check()
#ops.change_name("Ferocious Mouse")

shop = '1'
namer = '467'
speed_shrine = '461'
warp_shrine = '374'
gold_shrine = '499'
sandovsky_statue = '492'
aarons_athenaeum = '486'
well = '55'
mine = "350"


go_to_room(current_room, mine)
