import hashlib
import requests

import sys
import json
import time
from actions import headers


def proof_of_work(last_proof, difficulty):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """

    print("Searching proof...")
    block_string = json.dumps(last_proof, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof, difficulty) is False:
        proof += 1
    print("-+==[Proof found: " + str(proof), " ]==+-")
    
    return proof


def valid_proof(last_hash, proof, difficulty):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    
    guess = f"{last_hash}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:difficulty] == "0" * difficulty

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = 'https://lambda-treasure-hunt.herokuapp.com/api/bc'

    lambdacoin = 0

    # Run forever until interrupted
    while True:
        print(f"===getting last block from the server===")
        r = requests.get(url=node + "/last_proof", headers=headers)
        data = r.json()
        time.sleep(data['cooldown'])

        get_proof = proof_of_work(data.get('proof'), data.get('difficulty'))
        proof_value = {"proof": get_proof}

        # ====================

        r = requests.post(url=node + "/mine", json=proof_value, headers=headers)
        data = r.json()
        time.sleep(data['cooldown'])
        print('Server said: ', data)
        if data.get('message') is not None:
            lambdacoin += 1
            print("------=========== successfully [mined] coin============---------")
            print("Coins mined per session: " + str(lambdacoin))
        else:
            print('failed, try again')