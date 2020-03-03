import requests
import time
import sys
import json

url = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": "Token 6f3b08d7fd9a56e4f252f8e8ca9d3397fa308836"}

def move(direction, room_id=None):
    if room_id is None:
        data = {"direction": direction}
        r = requests.post(url=url + "/adv/move",
                            json=data, headers=headers)
        result = r.json()
        time.sleep(r.json()["cooldown"])
        return result

    else:
        data = {"direction": direction, "next_room_id": str(room_id)}
        r = requests.post(url=url + "/adv/move",
                            json=data, headers=headers)
        result = r.json()
        time.sleep(r.json()["cooldown"])
        return result

r = requests.get(url=url + "/adv/init", headers=headers)
starting_room = r.json()
cooldown = starting_room["cooldown"]
time.sleep(cooldown)

stack = []
stack.append(starting_room)
visited = dict()

# while len(visited) < 500:
#     while len(stack) > 0:
#         print(f'Rooms visited: {len(visited)}')
#         room = stack.pop()
#         if room["room_id"] not in visited:
#             visited[room["room_id"]] = dict()

#             for d in room["exits"]:
#                 visited[room["room_id"]][d] = "?"

#         if "w" in visited[room["room_id"]] and visited[room["room_id"]]["w"] == "?":
#             room_w_to = move("w")

#             stack.append(room_w_to)
#             visited[room["room_id"]]["w"] = room_w_to["room_id"]
#             if room_w_to["room_id"] not in visited:

#                 visited[room_w_to["room_id"]] = dict()
#                 for d in room_w_to["exits"]:
#                     visited[room_w_to["room_id"]][d] = "?"
#                 visited[room_w_to["room_id"]]["e"] = room["room_id"]
#             else:
#                 visited[room_w_to["room_id"]]["e"] = room["room_id"]

#         elif "e" in visited[room["room_id"]] and visited[room["room_id"]]["e"] == "?":
#             room_e_to = move("e")

#             stack.append(room_e_to)
#             visited[room["room_id"]]["e"] = room_e_to["room_id"]
#             if room_e_to["room_id"] not in visited:
#                 visited[room_e_to["room_id"]] = dict()
#                 for d in room_e_to["exits"]:
#                     visited[room_e_to["room_id"]][d] = "?"
#                 visited[room_e_to["room_id"]]["w"] = room["room_id"]
#             else:
#                 visited[room_e_to["room_id"]]["w"] = room["room_id"]

#         elif "n" in visited[room["room_id"]] and visited[room["room_id"]]["n"] == "?":
#             room_n_to = move("n")

#             stack.append(room_n_to)
#             visited[room["room_id"]]["n"] = room_n_to["room_id"]
#             if room_n_to["room_id"] not in visited:
#                 visited[room_n_to["room_id"]] = dict()
#                 for d in room_n_to["exits"]:
#                     visited[room_n_to["room_id"]][d] = "?"
#                 visited[room_n_to["room_id"]]["s"] = room["room_id"]
#             else:
#                 visited[room_n_to["room_id"]]["s"] = room["room_id"]

#         elif "s" in visited[room["room_id"]] and visited[room["room_id"]]["s"] == "?":
#             room_s_to = move("s")

#             stack.append(room_s_to)
#             visited[room["room_id"]]["s"] = room_s_to["room_id"]
#             if room_s_to["room_id"] not in visited:
#                 visited[room_s_to["room_id"]] = dict()
#                 for d in room_s_to["exits"]:
#                     visited[room_s_to["room_id"]][d] = "?"
#                 visited[room_s_to["room_id"]]["n"] = room["room_id"]
#             else:
#                 visited[room_s_to["room_id"]]["n"] = room["room_id"]

#         else:
#             queue = []
#             paths = []
#             for d in room["exits"]:
#                     paths.append([d])
#                     queue.append(visited[room["room_id"]][d])
#             while len(queue) > 0:
#                 room_id = queue.pop(0)
#                 path = paths.pop(0)

#                 if ("s" in visited[room_id] and visited[room_id]["s"] == "?") or \
#                 ("n" in visited[room_id] and visited[room_id]["n"] == "?") or \
#                 ("w" in visited[room_id] and visited[room_id]["w"] == "?") or \
#                 ("e" in visited[room_id] and visited[room_id]["e"] == "?"):
#                     queue.clear()
#                     current_room = room
#                     for p in path:
#                         new_room = move(p, visited[current_room["room_id"]][p])
#                         current_room = new_room

#                     stack.append(current_room)
#                 else:
#                     if "s" in visited[room_id]:
#                         new_path = path.copy()
#                         new_path.append("s")
#                         paths.append(new_path)
#                         queue.append(visited[room_id]["s"])
#                     if "n" in visited[room_id]:
#                         new_path = path.copy()
#                         new_path.append("n")
#                         paths.append(new_path)
#                         queue.append(visited[room_id]["n"])
#                     if "w" in visited[room_id]:
#                         new_path = path.copy()
#                         new_path.append("w")
#                         paths.append(new_path)
#                         queue.append(visited[room_id]["w"])
#                     if "e" in visited[room_id]:
#                         new_path = path.copy()
#                         new_path.append("e")
#                         paths.append(new_path)
#                         queue.append(visited[room_id]["e"])

with open('world.json', 'w', encoding='utf-8') as f:
    json.dump(visited, f, ensure_ascii=False, indent=4)