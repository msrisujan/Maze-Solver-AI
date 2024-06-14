import pygame, argparse, csv, time
import numpy as np
from time import sleep
from itertools import count
from queue import PriorityQueue

class Node:
    def __init__(self,parent,g,cost,position):
        self.parent = parent
        self.g = g
        self.position = position
        self.f = cost
    
def is_in_maze(pos,grid_size):
    return pos[0] >= 0 and pos[0] <= grid_size[0] and pos[1] >= 0 and pos[1] <= grid_size[1]

class Astar:
    def __init__(self,grid,start,end,grid_dim):
        self.grid=grid
        self.start = start
        self.end = end
        self.grid_dim=grid_dim
        self.pqueue = PriorityQueue()
        self.visited = []
        self.path = []
        
    def heuristic1(self,position):
        return np.sqrt((position[0]-self.end[0])**2 + (position[1]-self.end[1])**2)
    
    def heuristic2(self,position):
        return abs(position[0]-self.end[0]) + abs(position[1]-self.end[1])
    
    def compute_children(self,node,heuristic):
        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        children = []
        x,y = node.position
        for move in moves:
            new_pos = (x+move[0],y+move[1])
            if is_in_maze(new_pos,self.grid_dim) and self.grid[new_pos[0]][new_pos[1]]!=0 and new_pos not in self.visited:
                if heuristic == 1:
                    h=self.heuristic1(new_pos)
                else:
                    h=self.heuristic2(new_pos)
                
                g=node.g+1
                f=g+h
                new_node=Node(node,g,f,new_pos)
                children.append(new_node)
        return children
    
    def solution1(self):
        unique=count()
        h=self.heuristic1(self.start)
        g=0
        f=g+h
        start_node=Node(None,g,f,self.start)
        self.pqueue.put((f,next(unique),start_node))
        while True:
            current=self.pqueue.get()[2]
            if current.position == self.end:
                self.path.append(current.position)
                while current.parent:
                    current=current.parent
                    self.path.append(current.position)
                return self.path[::-1],True
            for child in self.compute_children(current,1):
                self.pqueue.put((child.f,next(unique),child))
            self.visited.append(current.position)
            
        return self.path,False
    
    def solution2(self):
        unique=count()
        h=self.heuristic2(self.start)
        g=0
        f=g+h
        start_node=Node(None,g,f,self.start)
        self.pqueue.put((f,next(unique),start_node))
        while True:
            current=self.pqueue.get()[2]
            if current.position == self.end:
                self.path.append(current.position)
                while current.parent:
                    current=current.parent
                    self.path.append(current.position)
                return self.path[::-1],True
            for child in self.compute_children(current,2):
                self.pqueue.put((child.f,next(unique),child))
            self.visited.append(current.position)
            
        return self.path,False
    
if __name__=="__main__":
    start_time = time.time()
    black = (0, 0, 0) 
    white = (255, 255, 255) 
    green = (0,255,128) 
    red = (255,51,51) 
    grey = (192,192,192) 
    blue = (153,200,255) 
    path = (255,255,0)
    height = 12
    width = height 
    margin = 1


    parser = argparse.ArgumentParser()
    parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
    parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_0.csv", type=str)
    args = parser.parse_args()

    address = "mazes/" + args.maze_file
    grid = np.genfromtxt(address, delimiter=',', dtype=int)
    num_rows = len(grid)
    num_columns = len(grid[0])

    start = (0,0)
    goal = (num_rows-1, num_columns-1)
    grid_dim = (num_rows-1, num_columns-1)

    if args.display == 1:
    
        pygame.init()
        WINDOW_SIZE = [535, 535]
        screen = pygame.display.set_mode(WINDOW_SIZE)
      
        pygame.display.set_caption(f"Solving using Astar: {address}")

        done = False 
        run = False 
        close = False

        clock = pygame.time.Clock() 

        idx_to_color = [black, white, green, red, blue, path]

        astar = Astar(grid, start, goal, grid_dim)

       
        grid[0, 0] = 2
        grid[-1, -1] = 3
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True       
                elif event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        run = True
            
            screen.fill(grey) 
                
            #
            for row in range(num_rows):
                for column in range(num_columns):
                    color = idx_to_color[int(grid[row, column])]
                    pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin,width, height])

           
            clock.tick(60)
            pygame.display.flip()

            if run == True:
                sleep(0.01)
                solution,done = astar.solution2()
            
                explored = [node for node in astar.visited]

                for pos in explored:
                    grid[pos[0], pos[1]] = 4

            if done == True:
                for pos in solution:
                    grid[pos[0], pos[1]] = 5

                grid[0, 0] = 2
                grid[-1, -1] = 3

                screen.fill(grey) 
            
                for row in range(num_rows):
                    for column in range(num_columns):
                        color = idx_to_color[grid[row, column]]
                        pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin,width, height])

                clock.tick(60)
                pygame.display.flip() 

        
        print("Solved! Click exit.")
        while not close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                elif event.type == pygame.KEYDOWN:
                    close = True
        pygame.quit()

    else:
        print(f"Solving using Astar: {address}")
        astar = Astar(grid, start, goal, grid_dim)

        solution,done = astar.solution1()

        explored = [node for node in astar.visited]

        for pos in explored:
            grid[pos[0], pos[1]] = 4

        for pos in solution:
            grid[pos[0], pos[1]] = 5

        grid[0, 0] = 2
        grid[-1, -1] = 3

    with open(f"mazes_solutions/astar/astar_{args.maze_file}", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

    print(f"--- finished {time.time()-start_time:.3f} s---")
    exit(0)
    
        
        
        
        
        
                    
                
        
        
        
    