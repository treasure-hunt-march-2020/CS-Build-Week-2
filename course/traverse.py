from util import Stack, Queue
from graph import Graph
import requests 
import json

def traverse(self):
    stack = Stack()
    option = Stack()
    visited = set()
    path = []
    stack.push(0)


def init(self):
    headers = {
        'Authorization': 'Token 0578cda4d3cc0b65ac21d7e03dd509bbafd50e39',
        'Content-Type': 'application/json',
    }

    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
    print(res.json()) 

def move(direction):
    headers = {
        'Authorization': 'Token 0578cda4d3cc0b65ac21d7e03dd509bbafd50e39',
        'Content-Type': 'application/json',
    }

    data = '{"direction":"s"}'

    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    print(res.json()) 

# print(move("ololo"))