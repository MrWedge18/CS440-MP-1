from collections import deque
import numpy as np
import pdb
import math
import heapq

class Node:
    def __init__(self, y, x, parent):
        self.y = y
        self.x = x
        self.parent = parent
        if parent is None:
            self.cost = 0
        else:
            self.cost = parent.cost + 1
    def coord(self):
        return(self.y, self.x)

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
    
# Reads small search and returns it as a numpy array    
def small_search():
    file = open("smallSearch.txt")
    maze = np.empty([13, 30], dtype=str)
    for i in range(13):
        for j in range(30):
            maze[i][j] = file.read(1)
        file.read(1)
    file.close()
    return maze
    
# Reads medium search and returns it as a numpy array
def medium_search():
    file = open("mediumSearch.txt")
    maze = np.empty([13, 49], dtype=str)
    for i in range(13):
        for j in range(49):
            maze[i][j] = file.read(1)
        file.read(1)
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

# returns list of food
def foods (maze):
    food = []
    dim = maze.shape
    for i in range(dim[0]):
        for j in range(dim[1]):
            if maze[i][j] == '.':
                coord = (i, j)
                food.append(coord)
    return food
 
# Searches maze for 'P'. Returns a tuple of its position 
def starts (maze):
    start = ()
    dim = maze.shape
    for i in range(dim[0]):
        for j in range(dim[1]):
            if maze[i][j] == 'P':
                start = (i, j)
                break
    return start

# returns list of up, down, left, and right neighbors    
def get_children(node):
    up = Node(node.y - 1, node.x, node)
    down = Node(node.y + 1, node.x, node)
    left = Node(node.y, node.x - 1, node)
    right = Node(node.y, node.x + 1, node)
    return [up, down, left, right]
    
def is_valid(maze, node):
    if not maze[node.y][node.x] == '%':
        return true
    
def bfs(maze):
    start = starts(maze)
    food_list = foods(maze)
    
    frontier = deque()
    visited = set([])
    test = set([])
    
    n = Node(start[0], start[1], None)
    
    frontier.append(n)
    test.add(n.coord())
    
    step = 0
    
    #pdb.set_trace()
    while len(frontier) > 0:
        #pdb.set_trace()
        
        print(step)
        step += 1
        
        #if step % 1000 == 0:
        #    pdb.set_trace()
        
        parent = frontier.popleft()
        test.discard(parent.coord())
        
        if parent.coord() in food_list:
            #pdb.set_trace()
            food_list.remove(parent.coord())
            if len(food_list) == 0:
                path(maze, parent, 0)
                print(parent.cost)
                return
            else:
                frontier.clear()
                test.clear()
                visited.clear()
                
                frontier.append(parent)
                test.add(parent.coord)
        
        for child in get_children(parent):
            if not maze[child.y][child.x] == '%' and child.coord() not in visited and child.coord() not in test:
                frontier.append(child)
                test.add(child.coord())
                
        visited.add(parent.coord())
        
def dfs(maze):
    start = starts(maze)
    food_list = foods(maze)
    
    frontier = deque()
    visited = set([])
    test = set([])
    
    n = Node(start[0], start[1], None)
    
    frontier.append(n)
    test.add(n.coord())
    
    step = 0
    
    #pdb.set_trace()
    while len(frontier) > 0:
        #pdb.set_trace()
        
        print(step)
        step += 1
        
        #if step % 1000 == 0:
        #    pdb.set_trace()
        
        parent = frontier.pop()
        test.discard(parent.coord())
        
        if parent.coord() in food_list:
            #pdb.set_trace()
            food_list.remove(parent.coord())
            if len(food_list) == 0:
                path(maze, parent, 0)
                print(parent.cost)
                return
            else:
                frontier.clear()
                test.clear()
                visited.clear()
                
                frontier.append(parent)
                test.add(parent.coord)
        
        for child in get_children(parent):
            if not maze[child.y][child.x] == '%' and child.coord() not in visited and child.coord() not in test:
                frontier.append(child)
                test.add(child.coord())
                
        visited.add(parent.coord())
        
def greedy(maze):
    start = starts(maze)
    food_list = foods(maze)
    
    frontier = []
    visited = set([])
    test = set([])
    
    n = Node(start[0], start[1], None)
    
    heapq.heappush(frontier, (md(n, food_list), n))
    test.add(n.coord())
    
    step = 0
    
    #pdb.set_trace()
    while len(frontier) > 0:
        #pdb.set_trace()
        
        print(step)
        step += 1
        
        #if step % 1000 == 0:
        #    pdb.set_trace()
        
        tup = heapq.heappop(frontier)
        parent = tup[1]
        test.discard(parent.coord())
        
        if parent.coord() in food_list:
            #pdb.set_trace()
            food_list.remove(parent.coord())
            if len(food_list) == 0:
                path(maze, parent, 0)
                print(parent.cost)
                return
            else:
                frontier = []
                test.clear()
                visited.clear()
                
                heapq.heappush(frontier, (md(parent, food_list), parent))
                test.add(parent.coord)
        
        for child in get_children(parent):
            if not maze[child.y][child.x] == '%' and child.coord() not in visited and child.coord() not in test:
                heapq.heappush(frontier, (md(child, food_list), child))
                test.add(child.coord())
                
        visited.add(parent.coord())
    
def ayyy(maze):
    start = starts(maze)
    food_list = foods(maze)
    
    frontier = []
    visited = set([])
    test = set([])
    
    n = Node(start[0], start[1], None)
    
    heapq.heappush(frontier, (eval(n, food_list), n))
    test.add(n.coord())
    
    step = 0
    
    #pdb.set_trace()
    while len(frontier) > 0:
        #pdb.set_trace()
        
        print(step)
        step += 1
        
        #if step % 1000 == 0:
        #    pdb.set_trace()
        
        tup = heapq.heappop(frontier)
        parent = tup[1]
        test.discard(parent.coord())
        
        if parent.coord() in food_list:
            #pdb.set_trace()
            food_list.remove(parent.coord())
            if len(food_list) == 0:
                path(maze, parent, 0)
                print(parent.cost)
                return
            else:
                frontier = []
                test.clear()
                visited.clear()
                
                heapq.heappush(frontier, (eval(parent, food_list), parent))
                test.add(parent.coord)
        
        for child in get_children(parent):
            if not maze[child.y][child.x] == '%' and child.coord() not in visited and child.coord() not in test:
                heapq.heappush(frontier, (eval(child, food_list), child))
                test.add(child.coord())
                
        visited.add(parent.coord())
        
def path (maze, node, cost):
    if node.parent is None:
        print_to_txt(maze)
        print(cost)
        return
    
    maze[node.y][node.x] = '.'
    path(maze, node.parent, cost + 1)
    
#prints the maze numpy array to a text file.
def print_to_txt(maze):
    bounds = maze.shape
    file = open("debug.txt", "w")
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            file.write(maze[i][j])
        file.write("\r\n")  #\r\n for windows notepad
        
def md (node, food):
    if(len(food) <= 0):
        return float("inf")
    return math.fabs(food[0][0] - node.y) + math.fabs(food[0][1] - node.x)
    
# For A*. Calculates path cost + Manhattan distance
def eval(node, food):
    return node.cost + md(node, food)