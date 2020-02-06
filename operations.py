import requests
from time import sleep
import json
import hashlib
import random
from decouple import config

api_key = config('STAN_KEY')
url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"


class Operations:
    def __init__(self):
        self.current_room = {}
        self.wait = None

    def init_player(self):
        res = requests.get(url, headers={'Authorization': api_key}).json()
        self.wait = float(res.get('cooldown'))
        self.current_room = res
        sleep(res["cooldown"])
        return self.current_room

    def room_id(self):
        return self.current_room['room_id']

    def move(self,direction):
        if direction not in self.current_room['exits']:
            print("You can't go that way")
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
                                json={"direction": direction}, headers={'Authorization': api_key}).json()
            self.current_room = res
            sleep(res["cooldown"])
            return self.current_room

    def take(self):
        if len(self.current_room['items']) == 0:
            print('Nothing here to take')
            return None
        else:
            item = self.current_room['items']
            print(f'Taking {item}')
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/",
                                json={"name": item[0]}, headers={'Authorization': api_key}).json()
            sleep(res["cooldown"])

    def status_check(self):
        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/",
                            headers={'Authorization': api_key}).json()
        print(res)
        sleep(res["cooldown"])

    def sell(self, item="tiny treasure"):
        if self.current_room['title'] != 'Shop':
            print("You should go to the shop to sell")
        else:
            res1 = requests.post(" https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/",
                                 json={"name": item}, headers={'Authorization': api_key}).json()
            print(res1)
            sleep(res1["cooldown"])
            res = requests.post(" https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/",
                                json={"name": item, "confirm": "yes"}, headers={'Authorization': api_key}).json()
            print(res)
            sleep(res["cooldown"])

    def change_name(self, name):

        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/",
                            json={"name": [name], "confirm": "aye"}, headers={'Authorization': api_key}).json()
        print("You shall be known as", str(name))
        print(res)
        return res

    def lambda_coin_wallet(self):
        res = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/",
                           headers={'Authorization': api_key}).json()
        print(res)
        sleep(res["cooldown"])

    def wise_explore(self, direction, next_id):
        if direction not in self.current_room['exits']:
            print('Not a valid move')
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
                                json={"direction": direction, "next_room_id": next_id}).json()
            sleep(res["cooldown"])

    def pray(self):
        if self.current_room["title"] != 'Shrine':
            print("Nothing here to pray to")
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/",
                                headers={'Authorization': api_key}).json()
            print("praying")
            print(res)
            sleep(res["cooldown"])

ops = Operations()

ops.lambda_coin_wallet()
