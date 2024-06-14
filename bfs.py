import pygame, argparse, csv, time
import numpy as np
from time import sleep
from numpy.random import randint
def is_in_maze(pos, grid_size):
    return pos[0] >= 0 and pos[0] <= grid_size[0] and pos[1] >= 0 and pos[1] <= grid_size[1]



class Node:
    def __init__(self, pos, parent):
        self.x = pos[0]
        self.y=pos[1]
        self.parent = parent

class BFS:
    def __init__(self,start,end,grid_size):
        self.start = start
        self.goal = end
        self.dim = grid_size
        self.queue = [Node(start,None)]
        self.visited=[]
    
    def get_path(self,node):
        path = []
        while node.parent!=None:
            path.append((node.x,node.y))
            node=node.parent
        return path
    
    def compute_child(self,grid):
        current_node = self.queue.pop(0)
        x,y=current_node.x,current_node.y
        neighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for neighbour in neighbours:
            if is_in_maze(neighbour,self.dim) and (grid[neighbour[0]][neighbour[1]] in [1,3]):
                next_node = Node(neighbour,current_node)
                self.queue.append(next_node)
                if(neighbour==self.goal):
                    self.visited.append(next_node)
                    return self.get_path(next_node),True
        
        self.visited.append(current_node)
        return [],False
    

if __name__=="__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--display",help="Display generating process 0:False 1:True",default=1,type=int)
    parser.add_argument("--maze_file",help="filename (Csv) of the maze to load.",default="maze_0.csv",type=str)
    args=parser.parse_args()
    
    address="mazes/"+args.maze_file
    grid=np.genfromtxt(address,delimiter=",",dtype=int)
    num_rows=grid.shape[0]
    num_columns=grid.shape[1]
    
    start_pos=(0,0)
    end_pos=(num_rows-1,num_columns-1)
    grid[0,0]=2
    grid[-1,-1]=3
    
    grid_size=(num_rows-1,num_columns-1)


    if args.display:
        black=(0,0,0)
        white=(255,255,255)
        green=(50,205,50)
        red=(255,99,71)
        grey=(211,211,211)
        blue=(153,255,255)
        magenta=(255,0,255)
        
        idx_to_color=[black,white,green,red,blue,magenta]
        height=12
        width=height
        margin=1
        
        pygame.init()
        WINDOW_SIZE = [535, 535]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        pygame.display.set_caption(f"BFS Pathfinder. Solving: {address}")

    
        done = False
        run = False
        close = False

        clock = pygame.time.Clock()
        bfs = BFS(start_pos,end_pos,grid_size)

    
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
               
                elif event.type == pygame.KEYDOWN:
                    run = True
        
            screen.fill(grey) 
        
            for row in range(num_rows):
                for column in range(num_columns):
                    color = idx_to_color[grid[row, column]]
                    pygame.draw.rect(screen, color, 
                                  [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width, height])
        
        
            clock.tick(60) 
            pygame.display.flip() 
        
            if run == True:
                sleep(0.01)
                solution, done = bfs.compute_child(grid=grid)
                explored = [(node.x,node.y) for node in bfs.visited]

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
                        pygame.draw.rect(screen, color, 
                                      [(margin + width) * column + margin, 
                                      (margin + height) * row + margin,
                                      width, height])
        
        
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
        print(f"Pathfinder BFS. solving: {address}")

        done = False
        bfs = BFS(start_pos, end_pos, grid_size)

        while not done:
            solution, done = bfs.compute_child(grid=grid)

            explored = [(node.x,node.y) for node in bfs.visited]

            for pos in explored:
                grid[pos[0], pos[1]] = 4

    
        for pos in solution:
            grid[pos[0], pos[1]] = 5

    grid[0, 0] = 2
    grid[-1, -1] = 3


 
    with open(f"mazes_solutions/bfs/bfs_{args.maze_file}", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

    print(f"--- finished {time.time()-start_time:.3f} s---")
    exit(0)
        
    