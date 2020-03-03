from random import choice
# from urls import post, get, end
import json

# Note: This Queue class is sub-optimal. Why?
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

reverse_dirs = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

class Graph:

    """Represent the world as a dictionary of rooms mapping (room, dir) as edge."""

    def __init__(self):
        self.rooms = {}
        self.grid = {}

    def add_vertex(self, room):
        """
        Add a vertex to the graph.
        """
        if room['room_id'] not in self.rooms:
            self.rooms[room['room_id']] = room
            # self.rooms[room['room_id']]['exits'] = {
            #     d: '?' for d in room['exits']}

    def dfs(self, room, path=None):
        if not path:
            path = []
        next_dirs = self.get_unexplored_dir(room)
        path.append(room['room_id'])
        print('dfs path ---->', path)
        if len(next_dirs):
            direction = choice(next_dirs)
            explored = self.explore(direction, room)
            return self.dfs(explored, path)
        else:
            return path

    def get_unexplored_dir(self, room):
        return [direction for direction, value in self.rooms[room['room_id']]['exits'].items() if value == '?']

    def get_all_directions(self, room):
        return [d for d in self.rooms[room['room_id']]['exits']]

    def get_room_in_dir(self, room, direction):
        '''
        { <= self.rooms
            "0": { <= room_id
                "exits": { <= exits
       direction => "n": 1,
                    "s": 5,
                    "e": 8
                }
            }
        }
        '''
        return self.rooms[room['room_id']]['exits'][direction]

    def explore(self, direction, room, next_room=None):
        prev_room = room['room_id']
        if next_room:
            res = post(end['move'], {
                       'direction': direction, 'next_room_id': str(next_room)})
        else:
            res = post(end['move'], {'direction': direction})
            self.rooms[prev_room]['exits'][direction] = res['room_id']
            self.add_vertex(res)
            self.rooms[res['room_id']
                       ]['exits'][reverse_dirs[direction]] = prev_room
        return res

    def explore_path(self, room, path):
        '''
        Accepts a path that has a direction and the room id
        for the next room in that direction and returns an 
        object of the room at the end of the path
        path = [
            {
                d: "n",
                next_room: 5
            }
        ]
        '''
        path_length = len(path)
        curr_room = room
        for obj in path:
            print('number of rooms left to explore ---->', path_length)
            explored = self.explore(obj['d'], room, obj['next_room'])
            curr_room = explored
            path_length -= 1
        return curr_room

    def backtrack_to_unex(self, room):
        '''
        Accepts a full room object and finds a path to a 
        room with an unexplored direction and returns the 
        object of the room with an unexplored direction
        '''
        q = Queue()
        all_dirs = self.get_all_directions(room)
        visited = set()
        for d in all_dirs:
            next_room = self.get_room_in_dir(room, d)
            q.enqueue([{'d': d, 'next_room': next_room}])
        current_room = room
        while q.size:
            back_path = q.dequeue()
            room_in_dir = back_path[-1]['next_room']
            visited.add(room_in_dir)
            current_room = self.rooms[room_in_dir]
            unex = self.get_unexplored_dir(self.rooms[room_in_dir])
            if len(unex):
                return self.explore_path(room, back_path)
            else:
                next_dirs = self.get_all_directions(self.rooms[room_in_dir])
                for d in next_dirs:
                    room_in_next_dir = self.get_room_in_dir(current_room, d)
                    if room_in_next_dir not in visited:
                        q.enqueue(list(back_path) +
                                  [{'d': d, 'next_room': room_in_next_dir}])

    def get_path_to_room(self, curr, room_id):
        '''
        Accepts (current room, target room id)
        returns shortest path to target room from current room
        '''
        if curr['room_id'] == room_id:
            return curr
        curr_room = curr
        q = Queue()
        all_dirs = self.get_all_directions(curr)
        visited = set()
        for d in all_dirs:
            next_room = self.get_room_in_dir(curr, d)
            q.enqueue([{'d': d, 'next_room': next_room}])
        while q.size:
            path_to_room = q.dequeue()
            room_in_dir = path_to_room[-1]['next_room']
            d_in_dir = path_to_room[-1]['d']
            curr_room = self.rooms[room_in_dir]
            visited.add(f'{room_in_dir}{d_in_dir}')
            if room_in_dir == room_id:
                return self.explore_path(curr, path_to_room)
            else:
                next_dirs = self.get_all_directions(self.rooms[room_in_dir])
                for d in next_dirs:
                    room_in_next_dir = self.get_room_in_dir(curr_room, d)
                    if f'{room_in_next_dir}{d}' not in visited:
                        q.enqueue(list(path_to_room) +
                                  [{'d': d, 'next_room': room_in_next_dir}])