import numpy as np
import pdb
from collections import deque
import math
import heapq

# Position object
# y - y coordinate in the maze
# x - x coordinate in the maze
# (0,0) is the top left and y increases as you go down
# parent is the parent node. None if this node is the root
#
# Position object will also internally store the path cost. get_cost() will return the cost.
class Position:
    def __init__(self, y, x, parent):
        self.y = y
        self.x = x
        self.coord = (y, x)
        self.parent = parent
        if parent is None:
            self.cost = 0
        else:
            self.cost = parent.cost + 1
        
    def up(self):
        return Position(self.y-1, self.x, self)
        
    def down(self):
        return Position(self.y+1, self.x, self)
        
    def left(self):
        return Position(self.y, self.x-1, self)
        
    def right(self):
        return Position(self.y, self.x+1, self)
        
    def equals(self, pos):
        if self.x == pos.x and self.y == pos.y:
            return true
        else:
            return false
            
    def up_coord(self):
        return (self.y-1, self.x)
        
    def down_coord(self):
        return (self.y, self.x)
        
    def left_coord(self):
        return (self.y, self.x-1)
        
    def right_coord(self):
        return (self.y, self.x+1)
    
    def get_cost(self):
        return self.cost

# Reads the medium maze and returns it as a numpy array
def medium_maze():
    file = open("mediumMaze.txt")
    maze = np.empty([23,61], dtype=str)
    for i in range(23):
        for j in range(61):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze

# Reads the big maze and returns it as a numpy array    
def big_maze():
    file = open("bigMaze.txt")
    maze = np.empty([31, 81], dtype=str)
    for i in range(31):
        for j in range(81):
            maze[i][j] = file.read(1)
        file.read(2)
    file.close()
    return maze

# Reads the open maze and returns it as a numpy array
def open_maze():
    file = open("openMaze.txt")
    maze = np.empty([20, 37], dtype=str)
    for i in range(20):
        for j in range(37):
            maze[i][j] = file.read(1)
        file.read(2)
    file.close()
    return maze
    
#Checks if pos is at a food space
def check(pos, food):
    for i in range(len(food)):
        if pos.coord == food[i]:
            food.pop(i)
            return

#prints the maze numpy array to a text file.
def print_to_txt(maze):
    bounds = maze.shape
    file = open("debug.txt", "w")
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            file.write(maze[i][j])
        file.write("\r\n")  #\r\n for windows notepad

#Checks if the position is a valid position (i.e. not a wall or visited position)
def is_valid(maze, pos):
    if not maze[pos.y][pos.x] == '%' and not maze[pos.y][pos.x] == "'":
        return True
        
    return False
            
# Breadth First search
# Start is a 2-tuple
# Food is a list of 2-tuples
# Visited is a boolean. bfs will track visited spaces if True
def bfs(maze, start, food, visited):
    bounds = maze.shape

    frontier = deque()
    
    pos = Position(start[0], start[1], None)
    frontier.append(pos)
    
    count = 0
    
    while(len(food) > 0):
        #pdb.set_trace()
        print('step ' + str(count))
        count += 1
        if count == 10000:
            print_to_txt(maze)
            pdb.set_trace()
            break
        pos = frontier.popleft()
        check(pos, food)
        
        if pos.y >= bounds[0] or pos.x >= bounds[1]:
            continue
        
        if is_valid(maze, pos):
            if visited:
                maze[pos.y][pos.x] = "'"
            up = pos.up()
            down = pos.down()
            left = pos.left()
            right = pos.right()
            if is_valid(maze, up):
                frontier.append(up)
            if is_valid(maze, down):
                frontier.append(down)
            if is_valid(maze, left):
                frontier.append(left)
            if is_valid(maze, right):
                frontier.append(right)
              
    print_to_txt(maze)
    return pos

# recursively goes through the path backwards and places '.' on the path
def path (maze, pos, cost):
    if pos.parent is None:
        print_to_txt(maze)
        print(cost)
        return
    
    maze[pos.y][pos.x] = '.'
    path(maze, pos.parent, cost + 1)

# Depth First search
# Start is a 2-tuple
# Food is a list of 2-tuples
# Visited is a boolean. bfs will track visited spaces if True
def dfs (maze, start, food, visited):
    bounds = maze.shape

    frontier = deque()
    
    pos = Position(start[0], start[1], None)
    frontier.append(pos)
    
    count = 0
    
    while(len(food) > 0):
        #pdb.set_trace()
        print('step ' + str(count))
        count += 1
        if count == 10000:
            print_to_txt(maze)
            pdb.set_trace()
            break
        pos = frontier.pop()
        check(pos, food)
        
        if pos.y >= bounds[0] or pos.x >= bounds[1]:
            continue
        
        if is_valid(maze, pos):
            if visited:
                maze[pos.y][pos.x] = "'"
            up = pos.up()
            down = pos.down()
            left = pos.left()
            right = pos.right()
            if is_valid(maze, up):
                frontier.append(up)
            if is_valid(maze, down):
                frontier.append(down)
            if is_valid(maze, left):
                frontier.append(left)
            if is_valid(maze, right):
                frontier.append(right)
              
    print_to_txt(maze)
    return pos

# Greedy search
# Start is a 2-tuple
# Food is a list of 2-tuples
# Visited is a boolean. bfs will track visited spaces if True
def greedy (maze, start, food, visited):
    bounds = maze.shape

    frontier = []
    
    pos = Position(start[0], start[1], None)
    manhat = md(pos, food)
    heapq.heappush(frontier, (manhat, pos))
    
    count = 0
    
    while(len(food) > 0):
        #pdb.set_trace()
        print('step ' + str(count))
        count += 1
        if count == 1000:
            print_to_txt(maze)
            pdb.set_trace()
            break
        tup = heapq.heappop(frontier)
        pos = tup[1]
        check(pos, food)
        
        if pos.y >= bounds[0] or pos.x >= bounds[1]:
            continue
        
        if is_valid(maze, pos):
            if visited:
                maze[pos.y][pos.x] = "'"
            up = pos.up()
            down = pos.down()
            left = pos.left()
            right = pos.right()
            if is_valid(maze, up):
                heapq.heappush(frontier, (md(up, food), up))
            if is_valid(maze, down):
                heapq.heappush(frontier, (md(down, food), down))
            if is_valid(maze, left):
                heapq.heappush(frontier, (md(left, food), left))
            if is_valid(maze, right):
                heapq.heappush(frontier, (md(right, food), right))
              
    print_to_txt(maze)
    return pos

# A* search
# Start is a 2-tuple
# Food is a list of 2-tuples
# Visited is a boolean. bfs will track visited spaces if True
def ayy(maze, start, food, visited):
    bounds = maze.shape

    frontier = []
    
    pos = Position(start[0], start[1], None)
    heapq.heappush(frontier, (eval(pos, food), pos))
    
    count = 0
    
    while(len(food) > 0):
        #pdb.set_trace()
        print('step ' + str(count))
        count += 1
        if count == 10000:
            print_to_txt(maze)
            pdb.set_trace()
            break
        tup = heapq.heappop(frontier)
        pos = tup[1]
        check(pos, food)
        
        if pos.y >= bounds[0] or pos.x >= bounds[1]:
            continue
        
        if is_valid(maze, pos):
            if visited:
                maze[pos.y][pos.x] = "'"
            up = pos.up()
            down = pos.down()
            left = pos.left()
            right = pos.right()
            if is_valid(maze, up):
                heapq.heappush(frontier, (eval(up, food), up))
            if is_valid(maze, down):
                heapq.heappush(frontier, (eval(down, food), down))
            if is_valid(maze, left):
                heapq.heappush(frontier, (eval(left, food), left))
            if is_valid(maze, right):
                heapq.heappush(frontier, (eval(right, food), right))
              
    print_to_txt(maze)
    return pos
    
# Searches maze for food. Returns a list of tuples of their locations
def foods (maze):
    food = []
    dim = maze.shape
    for i in range(dim[0]):
        for j in range(dim[1]):
            if maze[i][j] == '.':
                coord = (i, j)
                food.append(coord)
    return food
 
# Searches maze fo 'P'. Returns a tuple of its position 
def starts (maze):
    start = ()
    dim = maze.shape
    for i in range(dim[0]):
        for j in range(dim[1]):
            if maze[i][j] == 'P':
                start = (i, j)
                break
    return start

# Calculates Manhattan distance between food and position
def md (pos, food):
    if(len(food) <= 0):
        return float("inf")
    return math.fabs(food[0][0] - pos.y) + math.fabs(food[0][1] - pos.x)
    
# For A*. Calculates path cost + manhattan distance
def eval(pos, food):
    return pos.cost + md(pos, food)