import hashlib
import requests
from decouple import config
import json

from uuid import uuid4

from time import sleep

import random

import sys

api_key = config('ADAM_KEY')

headers = {
    'Authorization': api_key
}


def proof_of_work(last_proof, difficulty):


    print("Searching for next proof")
    block_string = json.dumps(last_proof, sort_keys=True)
    # print(block_string, last_proof, difficulty)
    proof = random.randint(0, 10000000000)
    while valid_proof(block_string, proof, difficulty) is False:
        proof += 1
    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_hash, proof, difficulty):
    difficult = '0' * difficulty
    guess = f"{last_hash}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:difficulty] == difficult
if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/'
    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers={'Authorization': api_key})
        data = r.json()
        # print(data)
        new_proof = proof_of_work(data.get('proof'), data.get('difficulty'))
        post_data = {"proof": new_proof}
        print(post_data)
        r = requests.post(url=node + "/mine", json=post_data, headers={'Authorization': api_key})
        data = r.json()
        sleep(data['cooldown'])
        print('data', data)
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print('Breaking...')
            break