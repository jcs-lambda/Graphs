from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from queue import SimpleQueue, LifoQueue


def full_path(relative_path: str) -> str:
    from os.path import dirname, join, realpath
    return join(dirname(realpath(__file__)), relative_path)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/main_maze.txt"
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(full_path(map_file), "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

################################################################################
graph = {}
dead_ends = []
paths = {}

# DFT to build entire graph
stack = LifoQueue()
stack.put(player.current_room)
while not stack.empty():
    room:Room = stack.get()
    if room.id not in graph:
        graph[room.id] = {exit:'?' for exit in room.get_exits()}
    for direction, destination in graph[room.id].items():
        if destination == '?':
            next_room:Room = room.get_room_in_direction(direction)
            graph[room.id][direction] = next_room.id
            stack.put(next_room)
    if len(graph[room.id]) == 1:
        dead_ends.append(room.id)

# BFS to find shortest path to each room
for destination in graph:
    visited = set()
    queue = SimpleQueue()
    queue.put([player.current_room.id])
    while not queue.empty():
        path = queue.get()
        room:Room = path[-1]
        visited.add(room)
        if room == destination:
            paths[destination] = path
            break
        for next_room in graph[room].values():
            if next_room not in visited:
                queue.put(path + [next_room])

# for exits in graph.values():
#     exits.update({v:k for k,v in exits.items()})

print(len(graph), len(paths))
for i in range(10):
    print(i, graph[i], paths[i])

################################################################################
"""
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
"""