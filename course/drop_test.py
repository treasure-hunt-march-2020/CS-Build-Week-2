import requests 

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

def inventory_limit(inventory = None):
    inventory = inventory_status()
    if inventory["strength"] >= inventory["encumbrance"]:
        return True
    else:
        return False


# print(treasure_drop('shiny treasure'))
print(inventory_limit())