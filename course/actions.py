import requests 
import json

headers = {
        'Authorization': 'Token 0578cda4d3cc0b65ac21d7e03dd509bbafd50e39',
        'Content-Type': 'application/json',
    }

# =================== Treasure ===================
def treasure_pick(treasure):

    data = '{"name":f"{treasure}"'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=data)
    print("Treasure pick up", res.json())

def treasure_drop(treasure):

    data = '{"name":f"{treasure}"'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=data)
    print("Treasure drop", res.json())


# ================ Treasure sell ==================
def treasure_sell(treasure):

    data = '{"name":f"{treasure}"'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print(res.json().messages)

    data = '{"name":f"{treasure}", "confirm":"yes"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print("Treasure sold", res.json())


# =============== Status/inventory ================
def inventory_status():

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers)
    print("Inventory", res.json())

# =================== Examine =====================
def examine_object(name):

    data = '{"name":f"{name}"'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=headers, data=data)
    print("Examine", res.json())

# =================== Equipment =====================
def wear_equipment(equipment):

    data = '{"name":"[f"{equipment}"]"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/', headers=headers, data=data)
    print("Wear equipment",  res.json())

def drop_equipment(equipment):

    data = '{"name":"[f"{equipment}"]"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/', headers=headers, data=data)
    print("Drop equipment", res.json()) 
