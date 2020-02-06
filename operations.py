import requests
from time import sleep
import json
import hashlib
import random


api_key = "Token 26b3338051c40210c961c3080dfd3e7f292a58e0"

class Operations:
    def __init__(self):
        self.current_room = {}

    def init_player(self):
        res = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", headers={"Authorization": api_key}).json()
        self.wait = float(res.get('cooldown'))
        self.current_room = res
        sleep(res["cooldown"])
        return self.current_room

    def room_id(self):
        return self.current_room['room_id']

    def move(self, direction):
        if direction not in self.current_room['exits']:
            print("You can't go that way")
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move", json={"direction": direction}, headers={'Authorization': api_key}).json()
            self.current_room = res 
            sleep(res["cooldown"])
            return self.current_room

    def take(self):
        if len(self.current_room['items']) == 0:
            print("Nothing here to take")
            return None
        else:
            item = self.current_room["items"]
            print(f"Taking {item}")
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take", json={"name": item[0]}, headers={"Authorization": api_key}).json()
            sleep(res["cooldown"])

    def status_check(self):
        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status", headers={'Authorization': api_key}).json()
        print(res)
        sleep(res["cooldown"])

    def sell(self, item="tiny treasure"):
        if self.current_room['title'] != 'Shop':
            print("You should go to the shop to sell")
        else:
            res1 = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell", json={"name": item}, headers={"Authorization": api_key}).json()
            print(res1)
            sleep(res1["cooldown"])
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell", json={"name": item, "confirm": "yes"}, headers={"Authorization": api_key}).json()
            print(res)
            sleep(res['cooldown'])

    def change_name(self, name):
        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name", json={"name": [name], "confirm": "aye"}, headers={'Authorization': api_key}).json()
        print("You shall be known as", str(name))
        print(res)
        return res

    def lambda_coin_wallet(self):
        res = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance", headers={"Authorization": api_key}).json()
        print(res)
        sleep(res["cooldown"])

    def wise_explore(self, direction, next_id):
        if direction not in self.current_room['exits']:
            print("Not a valid move")
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move", json={"direction": direction, "next_room_id": next_id}, headers={"Authorization": api_key}).json()
            sleep(res["cooldown"])

    def pray(self):
        if self.current_room["tiite"] != "Shrine":
            print("Nothing here to pray to")
            return
        else:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/pray", headers={"Authorization": api_key}).json()
            print("praying")
            print(res)
            sleep(res["cooldown"])

    def get_last_proof():
        res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof', headers={'Authorization': api_key}).json()
        print("Last Proof", res)
        sleep(res["cooldown"])
        return res

    def proof_of_work(last_proof):
        last = last_proof['proof']
        difficulty = last_proof['difficulty']
        print("Searching for next proof")
        proof = random.randint(-9876543211, 9876543211)
        last_hash = json.dumps(last)
        while valid_proof(last_hash, proof, difficulty) is False:
            proof += 1

        print("Proof found: ", proof)
        new_proof = {"proof": int(proof)}
        res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine', headers={"Authorization": api_key}, json=new_proof).json()
        print("Coin mined?", res)
        print(res)
        sleep(res['cooldown'])
        return res

    def valid_proof(last_hash, proof):
        guess = f'{last_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess[:difficulty] == "0" * difficulty



