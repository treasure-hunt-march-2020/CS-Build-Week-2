from util import Stack, Queue
from graph import Graph
from actions import *
import requests 
import json
import time


def init():
    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
    print("=====")
    print("Start room is: ", res.json()["room_id"], res.json()["title"], res.json()["exits"])
    print("=====")
    time.sleep(res.json()["cooldown"])
    return res.json()

def move(direction):
    data = '{"direction":"'+str(direction)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    print(res.json())
    time.sleep(res.json()["cooldown"])
    return res.json()

def move_know(direction, next_room_id):
    data = '{"direction":"'+str(direction)+'", "next_room_id":"'+str(next_room_id)+'"}'
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

    shop = None
    wishing_well = None

    if start_room["title"] == "Shop":
        shop = start_room["room_id"]

    if start_room["title"] == "Wishing Well":
        wishing_well = start_room["room_id"]

    while stack.size() > 0:
        print("\n")
        print("+User status+", inventory_status())
        print("Shop :", shop)
        print("Wishing well :", wishing_well)
        print("\n")

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
                # Possible directions add amount of question mark
                directions +=1
                # Moves to unexplored room and add it to vertices andd edges
                if moved == False:
                    next_room = move(way)
                    print("next_room: ", next_room)
                    graph.add_vertex(next_room["room_id"], next_room["title"], next_room["description"], next_room["coordinates"], next_room["players"], next_room["items"], next_room["exits"], next_room["cooldown"], next_room["errors"], next_room["messages"])
                    # print("graph.directions", graph.directions)
                    graph.add_edge(room_id, way, next_room["room_id"])
                    # print("graph.directions", graph.directions)
                    print("\n===graph.directions len===", len(graph.directions))
                    stack.push(next_room["room_id"])

                    # Checking if there uniq room
                    if next_room["title"] == "Shop":
                        shop = next_room["room_id"]

                    if next_room["title"] == "Wishing Well":
                        wishing_well = next_room["room_id"]

                    if next_room["title"] == "Shrine":
                        shrine_use()

                    moved = True

                    # If room where we just entered has a items
                    if len(next_room["items"]) > 0:
                        # If you have ability to pick that:
                        if inventory_limit() == False:
                            for item in next_room["items"]:
                                print(" ==================")
                                print("++++++ Item ++++++", item)
                                print(" ==================")
                                print("\n")
                                treasure_pick(item)
                        # If you know where is the shop - go there and sell treasures
                        elif shop is not None:
                            shop_road = graph.bfs(next_room["room_id"], shop)
                            reverse = shop_road[::-1]
                            reverse = reverse[1:]
                            full_road = shop_road.extend(reverse)
                            
                            i = 0
                            next_room_to = None
                            while i < len(full_road) - 1:
                                current_room = full_road[i]
                                next_room_to = full_road[i+1]

                                # If you in store - sell each item from inventory
                                if current_room == shop:
                                    inventory_list = inventory_list()
                                    for item in inventory_list:
                                        treasure_sell(item)
                                
                                direction = graph.directions[current_room]
                                for way in direction:
                                    if direction[way] == next_room:
                                        next_room = move_know(way, next_room)
                                
                                if current_room not in visited:
                                    visited.add(current_room)
                                i+=1
                    # if gold_need() == True:
                    #     #TODO traverse to wishing well
                    #     change_name()
                    
                    stack.push(next_room["room_id"])   

        if directions > 1:
            options.push(room_id)

        # If we in dead end - use bfs
        if directions == 0:
            return_room = options.pop()
            print("==========BFS==========")
            room_path = graph.bfs(room_id, return_room)

            i = 0
            next_room_to = None
            while i < len(room_path)-1:
                current_room = room_path[i]
                next_room_to = room_path[i+1]
                direction = graph.directions[current_room]

                for way in direction:
                    if direction[way] == next_room_to:
                        next_room = move_know(way, next_room_to)
                if current_room not in visited:
                    visited.add(current_room)
                i+=1
            stack.push(next_room_to)
    return None

file = open("map.txt","w") 

def start_app():
    start_data = init()
    file.write(str(traverse(start_data)))
    file.close() 
    # traverse(start_data)

start_app()
