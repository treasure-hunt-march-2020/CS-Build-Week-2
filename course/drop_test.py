import requests 
import time 
import json 

headers = {
        'Authorization': 'Token 0578cda4d3cc0b65ac21d7e03dd509bbafd50e39',
        'Content-Type': 'application/json',
    }

def treasure_drop(treasure):
    
    data = '{"name":"'+str(treasure)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=data)
    return res.json()

def inventory_status():

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers)
    return res.json()

def recall():

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/recall/', headers=headers)
    return res.json()

def inventory_limit(inventory = None):
    inventory = inventory_status()
    if inventory["strength"] >= inventory["encumbrance"]:
        return True
    else:
        return False

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

def treasure_sell(treasure):

    data = '{"name":"'+str(treasure)+'", "confirm":"yes"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print("Treasure sold", res.json())
    time.sleep(res.json()["cooldown"])

def change_name():

    data = '{"name":"[Heorhii Siburov]", "confirm":"aye"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers, data=data)
    print("Change name", res.json()) 
    time.sleep(res.json()["cooldown"])

def examine():

    data = '{"name":"well"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=headers, data=data)
    print("Change name", res.json()) 
    time.sleep(res.json()["cooldown"])

def balance():

    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/', headers=headers)
    time.sleep(res.json()["cooldown"])
    return res.json()

def proof():

    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers=headers)
    time.sleep(res.json()["cooldown"])
    return res.json()

def mine(proof):

    data = json.dumps({'proof':proof })
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=data)
    print("MINE AWAY", res.json())
    return res.json()



# print(treasure_drop('shiny treasure'))
# print(inventory_status())
print(balance())
# print(init())
# change_name()
# examine()