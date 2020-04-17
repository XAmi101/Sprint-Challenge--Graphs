from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


traversal_path = []



# traversal_stack = []
# visited = []

# directions = ['n', 's', 'e', 'w']

# current_room = world.rooms[0]

reverse_dir = {'n': 's', 's': 'n','w': 'e','e': 'w'}


def get_possible_traversed_path(starting_room, visited=set()):
    
    path = []

    # get all possible exits in current_room
    for direction in player.current_room.get_exits():
        # player travel to room in direction of exit
        player.travel(direction)

        # check if new room has been visited, if not
        if player.current_room.id not in visited:
            # mark room id as visited
            visited.add(player.current_room.id)
            # add new direction to path
            path.append(direction)
            recurse = get_possible_traversed_path(player.current_room.id, visited)
            # recurse with new current_room and add to path
            path = path + recurse 
            # backtrack and go to different room
            player.travel(reverse_dir[direction])
            # add backtrack to path to keep track of steps 
            path.append(reverse_dir[direction])

        else:
            # Room already visited so backtrack and go to different room
            player.travel(reverse_dir[direction])

    return path

traversal_path = get_possible_traversed_path(player.current_room.id)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")




