from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

map_file = "room_data2.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())

room_graph2 = {}
for key in room_graph.keys():
    room_graph2[int(key)] = room_graph[key]
world.load_graph(room_graph2)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)




#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
