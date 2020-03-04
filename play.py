# from actions import *
from util import *
from mine import *
import re
import requests
import hashlib
import random
from collections import deque
import json
import time
from datetime import datetime
# other imports?

URL = 'https://lambda-treasure-hunt.herokuapp.com/'

class Game:

    def __init__(self):
        self.key = '6f3b08d7fd9a56e4f252f8e8ca9d3397fa308836'
        self.header = {"Authorization": f"Token {self.key}",
                        "Content-Type": "application/json"}
        self.cooldown = 0
        self.world = {}
        self.current_room = None
        self.encumbrance = 0
        self.encumbered = False
        self.gold = 0
        self.strength = 0
        self.then = datetime.now()
        self.balance = 0
        self.state = []
        # self.bodywear = None
        # self.footwear = None
        self.name_changed = False
        self.items_ = deque()
        self.places = {'Shop': {'room_id': 1},
                       'Mine': {'room_id': None},
                       "Pirate Ry's": {'room_id': 467},
                       'Wishing Well': {'room_id': 55},
                       'warp': {'room_id': None},
                       'warp_well': {'room_id': 555}}

    def load_world(self):
        with open('world.json', 'r') as f:
            self.world = json.load(f)

    def make_request(self, suffix, data=None, header=None, http=None):
        while (datetime.now() - self.then).seconds < self.cooldown + 0.1:
            pass
        try:
            if http == 'get':
                response = requests.get(URL + suffix, headers=header, data=data)
            elif http == 'post':
                response = requests.post(URL + suffix, headers=header, json=data)
        except response.raise_for_status():
            self.autoplay()
        response = response.json()
        self.handle_response(response)
        self.then = datetime.now()
        return response

    def handle_response(self, response):
        if 'cooldown' in response:
            self.cooldown = float(response['cooldown'])
        if 'errors' in response:
            if response['errors']:
                print(f'Error: {response["errors"]}')
        if 'messages' in response:
            print(f'{"".join(response["messages"])}')

    def create_player(self):
        header = {"Authorization": f"Token {self.key}"}
        new_room = self.make_request(suffix='api/adv/init/', header=header, http='get')
        self.current_room = new_room['room_id']
        self.status()
        # self.balance()
        self.find_items(new_room)
        return

    def play(self):
        while True:
            # if self.gold >= 1000 and self.name_changed is False:
            #     self.name_change()

            # if self.gold < 1000:
            #     if self.encumbered:
            #         # self.move(room['Shop']['room_id'])
            #         self.sell_things()
            #     if not self.encumbered:
            #         self.move(random.choice(self.world['room']['exits']))
            #         if self.treasure is True:
            #             self.take()

            # if self.name_changed is True:
            #     # go to wishing well to see where coins are
            #     self.move(room['Wishing Well']['room_id'])
            #     clue = examine_object()
            #     # room_to_mine = # something from clue?
            #     room['mine']['room_id'] = room_to_mine
            #     self.move(room['mine']['room_id'])
            #     mine(room['mine']['room_id'])
            if self.places["Pirate Ry's"]['room_id'] and not self.name_changed and self.gold >= 1000:
                self.name_change()
            # Sell treasure.
            if self.encumbered and self.places['Shop']['room_id']:
                self.sell_things()
            # Go to random rooms to collect treasure until you can carry no more.
            if not self.encumbered:
                self.treasure_hunt()
            # Go get a golden snitch.
            # Mine lambda a coin.
            if self.encumbered and self.places['Wishing Well']['room_id'] and self.name_changed:
                self.get_coin()

    def find_path(self, target):
        if self.current_room == target:
            return []
        visited = set()
        path = [(self.current_room, '')]
        queue = deque()
        room = path[-1][0]
        if room not in visited:
            visited.add(room)
            exits = self.world['room']['exits']
            for exit in exits:
                new_room = self.world[room][f'to_{exit}']
                new_path = [*path, (new_room, exit)]
                if new_room == target:
                    return new_path[1:]
                queue.append(new_path)

    def take_path(self, path):
        for n_room in path:
            room = n_room[0]
            direction = n_room[1]
            n_room = self.move(direction, room=room)
            self.current_room = int(n_room['room_id'])

    def treasure_hunt(self):
        start, end = 0, 499
        random_room = random.randint(start, end)
        print(f'going to {random_room}')
        path = self.find_path(random_room)
        self.take_path(path)
        print(f'got to {random_room}')

    def examine(self, item):
        suffix = 'api/adv/examine/'
        data = {"name": f'{item}'}
        response = self.make_request(suffix=suffix, data=data, header=self.header, http='post')
        return response

    def take(self, item):
        # come back to this
        item = self.examine(item)
        item_type = item['itemtype']
        item_weight = int(item['weight'])
        if item_type == 'TREASURE' and (self.encumbrance + item_weight < self.strength):
            self.items_.append(item)
            self.encumbrance += item_weight
        return response


    def find_items(self, new_room):
        if new_room['items'] and not self.encumbered:
            for item in new_room['items']:
                self.take(item)

    def move(self, direction, room):
        if room is not None:
            data = {'direction': f'{direction}', 'next_room_id': f'{room}'}
        else:
            data = {'direction': f'{direction}'}
        suffix = 'api/adv/move'
        new_room = self.make_request(suffix=suffix, header = self.header, data=data, http='post')
        self.find_items(new_room)
        return new_room

    def sell_things(self):
        print('going to the store')
        path = self.find_path(int(self.places['Shop']['room_id']))
        self.take_path(path)
        self.sell()
        self.status()

    def sell(self):
        suffix = 'api/adv/sell/'
        while any([item['itemtype'] == 'TREASURE' for item in self.items_]):
            item = self.items_.popleft()
            if item['itemtype'] == 'TREASURE':
                print(f'selling {item["itemname"]}')
                data = {'name': item['name']}
                self.make_request(suffix=suffix, data=data, header=self.header, http='post')
                data = {'name': item['name'], 'confirm': 'yes'}
                self.make_request(suffix=suffix, data=data, header=self.header, http='post')
            else:
                self.items_.append(item)
        self.status()

    def change_name(self):
        suffix = 'api/adv/change_name/'
        data = {'name': 'mastin', 'confirm': 'aye'}
        response = self.make_request(suffix=suffix, data=data, header=self.header, http='post')
        return response

    def name_change(self):
        path = self.find_path(int(self.places["Pirate Ry's"]['room_id']))
        self.take_path(path)
        self.change_name()
        self.name_changed = True
        self.status()

    def status(self):
        suffix = 'api/adv/status/'
        response = self.make_request(suffix=suffix, header=self.header, http='post')
        self.encumbrance = int(response['encumbrance'])
        self.status_ = response['status']
        self.gold = response['gold']
        if self.encumbrance >= self.strength:
            self.encumbered = True
        else:
            self.encumbered = False
        return response

    def proof(self):
        suffix = 'api/bc/last_proof/'
        auth = {'Authorization': f'Token {self.key}'}
        response = self.make_request(suffix=suffix, header=auth, http='get')
        last_proof = response['proof']
        difficulty = response['difficulty']
        self.new_proof(last_proof, difficulty)

    def mine(self, proof):
        suffix = 'api/bc/mine'
        data = {'proof': proof}
        response = self.make_request(suffix=suffix, data=data, header=self.header, http='post')
        return response

    # def balance(self):
    #     suffix = 'api/bc/get_balance'
    #     auth = {'Authorization': f'Token {self.key}'}
    #     response = self.make_request(suffix=suffix, header=auth, http='get')
    #     message = response['messages']
    #     balance = re.search(r'\d+', *message)
    #     self.balance_ = int(balance.group(0))

    def wish(self):
        response = self.examine('WELL')
        code = response['description'].split('\n')
        room = re.search(r'\d+', code)
        next_room = int(room.group(0))
        self.places['Mine']['room_id'] = next_room

    def new_proof(self, last_proof, difficulty):
        proof = 0
        tries = 0
        while valid_proof(last_proof, proof, difficulty) is False:
            proof += random.randint(1, 17)
            tries += 1
        print(f'Proof found after {tries} attempts')
        return proof

    def valid_proof(self, last_proof, proof, difficulty):
        # hash(last_proof, proof) must contain N leading zeroes,
        # where N is the current difficulty level

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        if guess_hash[:difficulty] == '0' * difficulty:
            print(f'Valid solution: {guess_hash} from proof {proof}')

        return guess_hash[:difficulty] == '0' * difficulty

    def get_coin(self):
        path_well = self.find_path(int(self.places['Wishing Well']['room_id']))
        self.take_path(path_well)
        self.wish()
        path_mine = self.find_path(int(self.places['Mine']['room_id']))
        self.take_path(path_mine)
        self.proof()

    def autoplay(self):
        self.load_world()
        self.create_player()
        self.play()