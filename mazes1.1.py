import numpy as np
import pdb
from collections import deque

class Position:
    def __init__(self, y, x, parent):
        self.y = y
        self.x = x
        self.coord = (y, x)
        self.parent = parent
        
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

def medium_maze():
    file = open("mediumMaze.txt")
    maze = np.empty([23,61], dtype=str)
    for i in range(23):
        for j in range(61):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze
    
def big_maze():
    file = open("bigMaze.txt")
    maze = np.empty([31, 81], dtype=str)
    for i in range(31):
        for j in range(81):
            maze[i][j] = file.read(1)
        file.read(2)
    file.close()
    return maze
    
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
    
def small_search():
    file = open("smallSearch.txt")
    maze = np.empty([13, 30], dtype=str)
    for i in range(13):
        for j in range(30):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze
    
def medium_search():
    file = open("mediumSearch.txt")
    maze = np.empty([13, 49], dtype=str)
    for i in range(13):
        for j in range(49):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze
    
def check(pos, food):
    for i in range(len(food)):
        if pos.coord == food[i]:
            food.pop(i)
            return

def print_to_txt(maze):
    bounds = maze.shape
    file = open("debug.txt", "w")
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            file.write(maze[i][j])
        file.write("\r\n")
        
def is_valid(maze, pos):
    if not maze[pos.y][pos.x] == '%' and not maze[pos.y][pos.x] == "'":
        return True
        
    return False
            
# Maze is a 2D numpy array
# Start is a 2-tuple
# Food is a list of 2-tuple
def bfs(maze, start, food):
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
    
maze = medium_maze()
path = bfs(maze, (1,1), [(20,59)])

