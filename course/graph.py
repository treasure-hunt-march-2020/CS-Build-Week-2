from util import Stack, Queue
import copy

class Graph:

    def __init__(self):
        self.vertices = {}
        self.room_data = {}


    def add_vertex(self, room_id, title, description, coordinates, players, items, exits, cooldown, errors, messages):
        edges = {}
        for way in exits:
            edges[way] = "?"
        self.vertices[room_id] = edges
        self.room_data[room_id] = {"title": title, "description": description, "coordinates": coordinates, "players": players, "items": items, "exits": exits, "cooldown": cooldown, "errors": errors, "messages": messages}


    def add_edge(self, room1, direction, room2):
        global_directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
        if room1 in self.vertices and room2 in self.vertices:
            self.vertices[room1][direction] = room2
            reverse_direction = global_directions[direction]
            self.vertices[room2][reverse_direction] = room1
        else:
            raise IndexError("That vertex does not exist!")

    def get_neighbors(self, room_id):
        return self.vertices[room_id]

    def bft(self, starting_vertex):
        q = Queue()
        q.enqueue(starting_vertex)
        visited = set()
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                print(v)
                visited.add(v)
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def bfs(self, starting_vertex, destination_vertex):
        q = Queue()
        q.enqueue([starting_vertex])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            print(path)
            last_vertex = path[-1]
            if last_vertex == destination_vertex:
                return path
            if path[-1] not in visited:
                visited.add(path[-1])
                # print(visited)
                for neighbor in self.get_neighbors(path[-1]):
                     path_copy = copy.copy(path)
                     path_copy.append(neighbor)
                     q.enqueue(path_copy)