import numpy as np
import Queue

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
    
def bfs(maze, start, food):
    