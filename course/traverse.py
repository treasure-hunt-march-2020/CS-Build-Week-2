from util import Stack, Queue
from graph import Graph
from actions import *
import requests 
import json


def init():
    res = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
    print(res.json()) 

def move(direction):
    data = '{"direction":"s"}'
    res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    print(res.json()) 

def traverse(self):
    graph = Graph()
    stack = Stack()
    option = Stack()
    visited = set()
    path = []


print(init())