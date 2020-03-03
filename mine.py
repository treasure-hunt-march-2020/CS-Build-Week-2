import hashlib
import requests
import sys
import random

def new_proof(last_proof, difficulty):
    proof = 0
    tries = 0
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += random.randint(1, 17)
        tries += 1
    print(f'Proof found after {tries} attempts')
    return proof


def valid_proof(last_proof, proof, difficulty):
    # hash(last_proof, proof) must contain N leading zeroes,
    # where N is the current difficulty level

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    if guess_hash[:difficulty] == '0' * difficulty:
        print(f'Valid solution: {guess_hash} from proof {proof}')

    return guess_hash[:difficulty] == '0' * difficulty

# def mine(new_proof):
#     data = '{"proof": f"{new_proof}"'
#     res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=data)
#     return res.json