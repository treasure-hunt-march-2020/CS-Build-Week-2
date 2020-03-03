from util import Stack, Queue
from graph import Graph
from actions import *
import requests 
import json
import time


def init():
    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
    print(res.json()) 

def move(direction):
    data = '{"direction":"'+str(direction)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    print(res.json())
    time.sleep(res.json()["cooldown"])
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
    graph.add_vertex(start_room["room_id"], start_room["title"], start_room["description"], start_room["coordinates"], start_room["players"], start_room["items"], start_room["exits"], start_room["cooldown"], start_room["errors"], start_room["messages"])

    while stack.size() > 0:
        room_id = stack.pop()
        print("room_id: ", room_id)

        if room_id not in visited:
            visited.add(room_id)
            path.append(room_id)
        if len(visited) == 500:
            print("==========That's it==========")
            return path
        exits = graph.directions[room_id]
        print("exits: ", exits)

        directions = 0
        moved = False
        for way in exits:
            print("Way in exits: ", way, exits[way])
            if exits[way] == "?":
                directions +=1
                if moved == False:
                    next_room = move(way)
                    print("next_room: ", next_room)
                    graph.add_vertex(next_room["room_id"], next_room["title"], next_room["description"], next_room["coordinates"], next_room["players"], next_room["items"], next_room["exits"], next_room["cooldown"], next_room["errors"], next_room["messages"])
                    # print("graph.directions", graph.directions)
                    graph.add_edge(room_id, way, next_room["room_id"])
                    print("graph.directions", graph.directions)
                    print("\n===graph.directions len===", len(graph.directions))
                    stack.push(next_room["room_id"])
                    moved = True
        
        if directions > 1:
            options.push(room_id)

        if directions == 0:
            return_room = options.pop()
            print("==========BFS==========")
            room_path = graph.bfs(room_id, return_room)

            i = 0
            next_room_to = 0
            while i < len(room_path)-1:
                current_room = room_path[i]
                next_room_to = room_path[i+1]
                direction = graph.directions[current_room]

                for way in direction:
                    if direction[way] == next_room_to:
                        next_room = move(way)
                if current_room not in visited:
                    visited.add(current_room)
                i+=1
            stack.push(next_room_to)
    return None

startt = {'room_id': 63, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['User 20726', 'User 20649'], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 1.0, 'errors': [], 'messages': []}
# init()
traverse(startt)