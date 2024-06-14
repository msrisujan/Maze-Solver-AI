import pygame, argparse, csv, time
import argparse
import numpy as np
from time import sleep
from numpy.random import randint

def is_in_maze(pos, grid_size):
    return pos[0] >= 0 and pos[0] < grid_size[0] and pos[1] >= 0 and pos[1] < grid_size[1]

def get_possible_moves(curr_pos, grid_size):
    possible_moves = []
    actions_1 = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    actions_2 = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    for i in range(len(actions_1)):
        actions_1x, actions_1y = actions_1[i]
        actions_2x, actions_2y = actions_2[i]
        new_pos_1 = (curr_pos[0] + actions_1x, curr_pos[1] + actions_1y)
        new_pos_2 = (curr_pos[0] + actions_2x, curr_pos[1] + actions_2y)
        if is_in_maze(new_pos_1, grid_size) and is_in_maze(new_pos_2, grid_size):
            possible_moves.append([new_pos_1, new_pos_2])

    return possible_moves

def generate_move(grid, curr_pos, pos_visited, back_track):
    (x, y) = curr_pos
    grid[x][y] = 1
    
    grid_size = (len(grid), len(grid[0]))
    possible_moves = get_possible_moves(curr_pos, grid_size)

    valid_moves = []
    for move in possible_moves:
        (x1, y1) = move[0]
        (x2, y2) = move[1]

        if (grid[x1, y1] != 1) & (grid[x2, y2] != 1) & (grid[x1, y1] != 2) & (grid[x2, y2] != 2):
            valid_moves.append(move)

    
    if (len(valid_moves) == 0):
        curr_pos = pos_visited[-2 - back_track]
        if curr_pos == (0, 0):
            done = True
            return grid, curr_pos, pos_visited, back_track, done
        back_track += 1
        done = False
        return grid, curr_pos, pos_visited, back_track, done
    else:
        back_track = 0
        curr_pos = valid_moves[randint(len(valid_moves)) - 1]
        (x1, y1) = curr_pos[0]
        (x2, y2) = curr_pos[1]
        grid[x1][y1] = 1
        grid[x2][y2] = 4
        curr_pos = curr_pos[1]
        done = False
        return grid, curr_pos, pos_visited, back_track, done
    
if __name__ == "__main__":
    start_time = time.time()

    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (50,205,50)
    red = (255,99,71)
    grey = (211,211,211)
    blue = (153,255,255)

    height = 7
    width = height
    margin = 1

    parser = argparse.ArgumentParser()
    parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
    parser.add_argument("--num_mazes", help="Number of mazes to generate.", default=1, type=int)
    args = parser.parse_args()

    for i in range(args.num_mazes):
        start_t = time.time()

        rows = 41
        columns = rows
        grid = np.zeros((rows, columns))

        done = False
            
        curr_pos = (0, 0)
        pos_visited = [curr_pos]
        back_track = 0

        grid[0, 0] = 2
        grid[-1, -1] = 3

        if args.display == 1:
            pygame.init()
            window_size = [330, 330]
            screen = pygame.display.set_mode(window_size)
            pygame.display.set_caption(f"Creating Maze {i+1}/{args.num_mazes}...")

            run = False

            clock = pygame.time.Clock()

            colors = [black, white, green, red, blue]

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            run =  True

                screen.fill(grey)

                for row in range(rows):
                    for column in range(columns):
                        color = colors[int(grid[row][column])]
                        pygame.draw.rect(screen, color, 
                                         [(margin + width) * column + margin, 
                                          (margin + height) * row + margin, 
                                          width, height])
                        
                clock.tick(60)
                pygame.display.flip()

                if run:
                    grid, curr_pos, pos_visited, back_track, done = generate_move(grid, curr_pos, pos_visited, back_track)
                    if curr_pos not in pos_visited:
                        pos_visited.append(curr_pos)
                    sleep(0.01)

            close = False
            while not close:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close = True
                        pygame.quit()

                if event.type == pygame.KEYDOWN:
                    close = True
                    pygame.quit()

        else:

            print(f"Creating Maze {i+1}/{args.num_mazes}...")

            while not done:
                grid, curr_pos, pos_visited, back_track, done = generate_move(grid, curr_pos, pos_visited, back_track)
                if curr_pos not in pos_visited:
                    pos_visited.append(curr_pos)
                    
        
        zero_indices = np.argwhere(grid == 0)
    

        indices_to_change = np.random.choice(len(zero_indices), 50, replace=False)
    
        for index in indices_to_change:
            k, l = zero_indices[index]
            grid[k, l] = 1

        with open(f"mazes/maze_{i}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(grid)
        print(f"{time.time() - start_t:.2f} seconds to create maze {i+1}/{args.num_mazes}.")

    print(f"Total time: {time.time() - start_time:.2f} seconds.")
    print("Maze creation complete.")
    exit(0)