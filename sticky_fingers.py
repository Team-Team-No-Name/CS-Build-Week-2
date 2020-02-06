from operations import Operations
from player import Player
from time import sleep

op = Operations()
player = Player()

broke = True

while broke:
    current_room = op.init_player()
    sleep(current_room["cooldown"])
    while not player.sticky_fingers(current_room['room_id'], 'tiny treasure'):
        current_room = op.init_player()
    player.go(current_room['room_id'], 'Shop')

    res = op.sell('tiny treasure')
    if res is None:
        continue
    sleep(res['cooldown'])
    gold = res['gold']
    print(f"You have {gold} Gold!")
    if int(gold) > 1000:
        broke = False