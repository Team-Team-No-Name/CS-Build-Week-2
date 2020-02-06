import hashlib
import requests
from decouple import config
import json
from uuid import uuid4
from time import sleep
import sys

from uuid import uuid4

from timeit import default_timer as timer

from random import randint

api_key = config('STAN_KEY')

headers = {
    'Authorization: api_key'
}


def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    last_hash = json.dumps(last_proof, sort_keys=True)
    proof = last_proof*randint(0, 100)
    while valid_proof(last_hash, proof, difficulty) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
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
