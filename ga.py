import pygame, argparse, csv, time
import numpy as np
from time import sleep
from numpy.random import randint
import random

population_size = 10000
mutation_rate = 0.1
num_generations = 1000

population = []
for i in range(population_size):
    solution = []
    for j in range(1681):
        solution.append(random.choice(['up', 'down', 'left', 'right']))
    population.append(solution)

def fitness(solution, grid):
    # print("hi")
    start = (0, 0)
    end = (41, 41)
    time = 0
    for move in solution:
        if move == 'up':
            start = (start[0], start[1] - 1)
        elif move == 'down':
            start = (start[0], start[1] + 1)
        elif move == 'left':
            start = (start[0] - 1, start[1])
        elif move == 'right':
            start = (start[0] + 1, start[1])
        x, y = start
        # print(x)
        # print(y)
        # print(type(x))
        # print(type(y))
        # print(type(grid))
        grid_val = grid[x, y]
        if start[0] < 0 or start[0] >= 41 or start[1] < 0 or start[1] >= 41:
            # population.remove(solution)
            return 0
        if grid_val == 0:
            # population.remove(solution)
            return 0
        
        time += 1
        if start == end:
            return 1.0 / time
    return 0



def selection(population,f1):
    total_fitness = sum(f1)
    if total_fitness == 0:
        return -1
    probabilities = [f1[i]/total_fitness for i in range(len(f1))]
    selected = []
    for i in range(population_size):
        selected.append(population[np.random.choice(range(population_size), p=probabilities)[0]])
    return selected

def crossover(parent1, parent2):
    crossover_point = randint(0,len(parent1)-1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(solution):
    mutated_solution = solution.copy()
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            mutated_solution[i] = random.choice(['up', 'down', 'left', 'right'])
    return mutated_solution


if __name__ == "__main__":

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


    for generation in range(num_generations):
        print("1")
        # Evaluate fitness of each solution
        fitness_scores = [fitness(solution, grid) for solution in population]
        
        # Select parents for reproduction
        parents = selection(population,fitness_scores)
        if parents == -1:
            continue
        
        # Create offspring through crossover
        offspring = []
        for i in range(population_size//2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)
        
        # Introduce mutation
        offspring = [mutation(solution) for solution in offspring]
        
        # Replace the old population with the new generation
        population = offspring
        # Check if a solution is found
        # best_solution = max(population, key=fitness)
        best_solution = max(population, key=lambda solution: fitness(solution, grid))
        if fitness(best_solution, grid) == 1.0:
            print("Solution found in generation", generation+1)
            print("Action sequence:", best_solution)

    if args.display:
        black=(0,0,0)
        white=(255,255,255)
        green=(50,205,50)
        red=(255,99,71)
        grey=(211,211,211)
        blue=(153,255,255)
        magenta=(255,0,255)
        
        idx_to_color=[black,white,green,red,blue,magenta]
        height=7
        width=height
        margin=1
        
        pygame.init()
        WINDOW_SIZE = [330, 330]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        pygame.display.set_caption(f"BFS Pathfinder. Solving: {address}")

        # current best solution
        best_solution = max(population, key=lambda solution: fitness(solution, grid))

        print("Action sequence:", best_solution)
        # change the grid to show the path
        start = (0, 0)
        end = (41, 41)
        for move in best_solution:
            if move == 'up':
                start = (start[0], start[1] - 1)
            elif move == 'down':
                start = (start[0], start[1] + 1)
            elif move == 'left':
                start = (start[0] - 1, start[1])
            elif move == 'right':
                start = (start[0] + 1, start[1])
            grid[start[0]][start[1]] = 5
            if start == end:
                break

        grid[0, 0] = 2
        grid[-1, -1] = 3
        
        print(grid)

        for row in range(num_rows):
            for column in range(num_columns):
                color = idx_to_color[grid[row, column]]
                pygame.draw.rect(screen, color, 
                                [(margin + width) * column + margin, 
                                (margin + height) * row + margin,
                                width, height])
                
        close = False
        while not close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                    pygame.quit()

            if event.type == pygame.KEYDOWN:
                close = True
                pygame.quit()


    print("Time taken:", time.time()-start_time)