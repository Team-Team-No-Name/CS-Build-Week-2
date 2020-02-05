import json
import requests
from decouple import config
from utils import Queue



api_key = config("DAKOTA_KEY")

with open("room_conns.txt", "r") as conns:
    room_conn = json.loads(conns.read())


current_room = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers={'Authorization': api_key}).json()




def bfs(room_id, current_room_id, end_room):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    q = Queue()
    q.enqueue([current_room_id])
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


def go_to_room(end_room, current_room=current_room):
    fast_paths = bfs([current_room["room_id"]], end_room, room_conn)
    # print(type(current_room['room_id']))
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
                next_room = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={"direction": str(dirs), "next_room_id": str(fast_paths[counter])}, headers={'Authorization': api_key}).json()
                current_room = next_room
                print(current_room)
                counter += 1
            else:
                return

# List of important room numbers
shop = 1
namer = '467'
speed_shrine = '461'
warp_shrine = '374'
gold_shrine = '499'
sandovsky_statue = '492'
aarons_athenaeum = '486'
well = '55'

go_to_room(shop)
