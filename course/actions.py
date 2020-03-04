import requests 
import json
import time

headers = {
        'Authorization': 'Token 0578cda4d3cc0b65ac21d7e03dd509bbafd50e39',
        'Content-Type': 'application/json',
    }

# =================== Treasure ===================
def treasure_pick(treasure):

    data = '{"name":"'+str(treasure)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=data)
    time.sleep(res.json()["cooldown"])
    return res.json()

def treasure_drop(treasure):

    data = '{"name":"'+str(treasure)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=data)
    return res.json()

# ================ Treasure sell ==================
def treasure_sell(treasure):

    data = '{"name":"'+str(treasure)+'", "confirm":"yes"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print("Treasure sold", res.json())
    time.sleep(res.json()["cooldown"])

# =============== Status/inventory ================
def inventory_status():

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers)
    return res.json()

# =================== Examine =====================
def examine_object(name):

    data = '{"name":"'+str(name)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=headers, data=data)
    print("Examine", res.json())

# =================== Equipment =====================
def wear_equipment(equipment):

    data = '{"name":"'+str(equipment)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/', headers=headers, data=data)
    print("Wear equipment",  res.json())

def drop_equipment(equipment):

    data = '{"name":"'+str(equipment)+'"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/', headers=headers, data=data)
    print("Drop equipment", res.json()) 

# =================Local functions==================
def show_inventory(inventory = None):
    if inventory == None:
        inventory = inventory_status()
    return inventory["inventory"]

def inventory_limit(inventory = None):
    inventory = inventory_status()
    if len(inventory["inventory"]) == ["strength"]:
        return True
    else:
        return False

def inventory_list(inventory = None):
    if inventory == None:
        inventory = inventory_status()
    return inventory["inventory"]

def gold_need(inventory = None):
    inventory=inventory_status()
    if inventory["gold"] >=1000:
        return True
    else:
        return False

# ============= Name change =======================
def change_name():

    data = '{"name":"[Heorhii Siburov]"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers, data=data)
    print("Change name", res.json()) 

def shrine_use():

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers)
    print("-==Shrine use==-", res.json()) 