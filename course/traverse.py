from util import Stack, Queue
from graph import Graph
from actions import *
import requests 
import json


def init():
    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
    print(res.json()) 

def move(direction):
    data = '{"direction":f{direction}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    print(res.json())
    return res.json()

def traverse(start_room):
    graph = Graph()
    # Place for path
    stack = Stack()
    path = []
    # Place for room_id with non-visited directions
    options = Stack()
    # Place for visited rooms
    visited = set()
    # Pushing first room in stack
    stack.push(start_room["room_id"])
    graph.add_vertex(start_room["room_id"], start_room["title"], start_room["description"], start_room["coordinates"], start_room["exits"], start_room["cooldown"], start_room["errors"], start_room["messages"])

    while stack.size() > 0:
        room_id = stack.pop()
        print("room_id: ", room_id)

        if room_id not in visited:
            visited.add(room_id)
            path.append(room_id)
        if len(visited) == 500:
            return path
        exits = graph.directions[room_id]
        print("exits: ", exits)

        directions = 0
        for way in exits:
            print("Way in exits: ", way, exits[way])
            if exits[way] == "?":
                directions +=1
                print("way: ", way)
                next_room = move(way)
                print("next_room: ", next_room)
                graph.add_vertex(next_room["room_id"], next_room["title"], next_room["description"], next_room["coordinates"], next_room["exits"], next_room["cooldown"], next_room["errors"], next_room["messages"])

print(init())