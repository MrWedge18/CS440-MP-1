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
    def __init__(self, y, x, parent, food, visited):
        self.y = y
        self.x = x
        self.coord = (y, x)
        self.parent = parent
        if parent is None:
            self.cost = 0
        else:
            self.cost = parent.cost + 1
        self.food = list(food)
        self.visited = visited
        
    def up(self):
        new_visited = list(self.visited)
        new_visited.append(self.coord)
        return Position(self.y-1, self.x, self, self.food, new_visited)
        
    def down(self):
        new_visited = list(self.visited)
        new_visited.append(self.coord)
        return Position(self.y+1, self.x, self, self.food, new_visited)
        
    def left(self):
        new_visited = list(self.visited)
        new_visited.append(self.coord)
        return Position(self.y, self.x-1, self, self.food, new_visited)
        
    def right(self):
        new_visited = list(self.visited)
        new_visited.append(self.coord)
        return Position(self.y, self.x+1, self, self.food, new_visited)
        
    def equals(self, pos):
        if self.x == pos.x and self.y == pos.y:
            return True
        else:
            return False
            
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
    
def tiny_search():
    file = open("tinySearch.txt")
    maze = np.empty([9, 10], dtype=str)
    for i in range(9):
        for j in range(10):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze
    
#Checks if pos is at a food space
def check(pos):
    for i in range(len(pos.food)):
        if pos.coord == pos.food[i]:
            pos.food.pop(i)
            pos.visited = []
            return True
            
    return False

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
    if not maze[pos.y][pos.x] == '%' and not maze[pos.y][pos.x] == "'" and pos.coord not in pos.visited:
        return True
    return False
            
# Breadth First search
# Start is a 2-tuple
# Food is a list of 2-tuples
# Visited is a boolean. bfs will track visited spaces if True
def bfs(maze, start, food, visited):
    bounds = maze.shape

    frontier = deque()
    
    pos = Position(start[0], start[1], None, food, [])
    frontier.append(pos)
    
    count = 0
    
    while(len(pos.food) > 0):
        #pdb.set_trace()
        print('step ' + str(count))
        print(len(pos.food))
        count += 1
        if count == 1000000:
            #print_to_txt(maze)
            pdb.set_trace()
            #break
        pos = frontier.popleft()
        if check(pos):
            #pdb.set_trace()
            maze = tiny_search()
            if len(pos.food) == 0:
                return pos
        
        if pos.y >= bounds[0] or pos.x >= bounds[1]:
            continue
        
        if is_valid(maze, pos):
            #if visited:
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
              
    path(maze, pos, 0)
    return pos

# recursively goes through the path backwards and places '.' on the path
def path (maze, pos, cost):
    if pos.parent is None:
        print_to_txt(maze)
        print(cost)
        return
    
    maze[pos.y][pos.x] = '.'
    path(maze, pos.parent, cost + 1)
    
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
    
def show_visited(maze, pos):
    bounds = maze.shape
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            if (i, j) in pos.visited:
                maze[i][j] = '.'
                
    print_to_txt(maze)