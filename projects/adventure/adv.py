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
done = set()
prev_room:Room = None
direction_travelled:str = None

reverse = {'n':'s','s':'n','w':'e','e':'w'}

def get_color(room:Room) -> str:
    if room.id not in graph:
        return 'white'
    elif '?' in graph[room.id].values():
        return 'grey'
    else:
        done.add(room.id)
        return 'black'

def walk_path(path:[Room]):
    global prev_room, direction_travelled
    assert player.current_room.id == path[0].id, \
        'start of path is not current room'
    for next_room in path[1:]:
        current_room:Room = player.current_room
        for direction in current_room.get_exits():
            if current_room.get_room_in_direction(direction).id == next_room.id:
                prev_room = player.current_room
                direction_travelled = direction
                player.travel(direction)
                traversal_path.append(direction)
                break

while len(done) < len(room_graph):
    room:Room = player.current_room
    if get_color(room) == 'white':
        graph[room.id] = {direction:'?' for direction in room.get_exits()}
    if prev_room is not None:
        graph[room.id][reverse[direction_travelled]] = prev_room.id
        graph[prev_room.id][direction_travelled] = room.id
        get_color(prev_room)
    if get_color(room) == 'grey':
        direction = [
            direction
            for direction, destination in graph[room.id].items()
            if destination == '?'
        ][0]
        walk_path([room, room.get_room_in_direction(direction)])
    if get_color(room) == 'black':
        if len(done) == len(room_graph):
            break
        queue = SimpleQueue()
        queue.put([room])
        visited = set()
        while not queue.empty():
            path = queue.get()
            room = path[-1]
            visited.add(room.id)
            if get_color(room) == 'grey':
                break
            for direction in graph[room.id]:
                next_room:Room = room.get_room_in_direction(direction)
                if next_room.id not in visited:
                    queue.put(path + [next_room])
        
        walk_path(path)

################################################################################

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
