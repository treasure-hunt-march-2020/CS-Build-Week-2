from actions import *
from util import *
from mine import *
import re
import requests
import hashlib
import random
from collections import deque
import json
# other imports?


class Game:

    def init(self):
        self.key = ''
        self.header = {"Authorization": f"Token {self.key}"}
        self.cooldown = 0
        self.world = {}
        self.current_room = None
        self.encumbrance = 0
        self.encumbered = False
        self.gold = 0
        # self.bodywear = None
        # self.footwear = None
        self.name_changed = False
        # self.items = deque()

    def load_world(self):
        with open('world.json', 'r') as f:
            self.world = json.load(f)

    def create_player(self):
        new_room = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
                    header=self.header)
        self.current_room = new_room['room_id']
        return

    def play(self):
        while True:
            if self.gold >= 1000:
                if self.named_changed is False:
                    # I think this is the room to change your name?
                    self.move(room['pirate_ry']['room_id'])
                    self.change_name()

            if self.gold < 1000:
                if self.encumbered:
                    self.move(room['shop']['room_id'])
                    self.treasure_sell()
                if not self.encumbered:
                    self.move(random.choice(room.get_exits()))
                    if self.treasure is True:
                        self.treasure_pick()

            if self.name_changed is True:
                # go to wishing well to see where coins are
                self.move(room['wishing_well']['room_id'])
                clue = examine_object()
                room_to_mine = # something from clue?
                room['mine']['room_id'] = room_to_mine
                self.move(room['mine']['room_id'])
                mine(room['mine']['room_id'])

    def autoplay(self):
        self.load_world()
        self.create_player()
        self.play()