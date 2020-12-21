import pygame
import math
from queue import PriorityQueue # Used for the 'open' spots queue

WIDTH = 800 # Dimensions of the pygame window
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # Because these are squares, we have same dimension
pygame.display.set_caption("Python A* Path Finding Algorithm Visualization")

# Colors for the visualization in Pygame

RED = (255, 0, 0) # Closed
GREEN = (0, 255, 0) # Open
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) # Default
BLACK = (0, 0, 0) # Barrier
PURPLE = (128, 0, 128) # Path, end of path
ORANGE = (255, 165 ,0) # Start 
GREY = (128, 128, 128) # Line color
TURQUOISE = (64, 224, 208)

# A class for nodes in which the grid is made up of
# 1. this class is designed to keep track of where the node is in the graph
# 2. the width of itself for pygame
# 3. keep track of neighbors
# 4. color of itself 

class Node:
    def __init__(self, row, col, width, num_rows):
        self.row = row
        self.col = col
        self.x = row * width # Need to keep track of coordinate position for pygame
        self.y = col * width # Need to keep track of coordinate position for pygame
        self.color = WHITE # To start, we want white nodes for open
        self.neighbors = []
        self.width = width
        self.num_rows = num_rows

    def get_position(self):
        return self.row, self.col # Indexing using (row, col) not (col, row), personal preference


    # DETERMINERS FOR NODE STATUS
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset_node(self):
        self.color = WHITE

    # SETTERS FOR NODE STATUS
    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_wall(self):
        self.color = BLACK

    def set_start(self):
        self.color = ORANGE

    def set_end(self):
        self.color = PURPLE

    def set_path(self):
        self.color = TURQUOISE

    def draw_node_to_screen(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbor_nodes(self, grid):
        self.neighbors = []
        # Checking if row we are at is less than total rows - 1
        if self.row < self.num_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # Go down a row
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # Go up a row
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.num_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # Go right a row
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # Go left a row
            self.neighbors.append(grid[self.row][self.col - 1])
        

    # This function stands for less than, this is what happens when we compare 2 nodes
    def __lt__(self, other):
        return False


def manhattan_distance(node1, node2):
    # This is just the 'L' distance between 2 nodes, not very efficient, there are better ways to do this
    x1, y1 = node1 # decomposition
    x2, y2 = node2
    return abs(x2 - x1) + abs(y2 - y1)

def draw_path(prev_node, current_node, draw):
    while current_node in prev_node:
        current_node = prev_node[current_node]
        current_node.set_path()
        draw()

# The actual A* path finding algorithm
def a_star(draw, grid, start, end):
    # draw argument is a function passed in by the lambda function
    counter = 0
    open_nodes = PriorityQueue() # Imported library
    open_nodes.put((0, counter, start)) # put() is add to priority queue, we are adding start node with F score of 0 into queue
    prev_node = {}
    g_score = {node: float("inf") for row in grid for node in row} # start all g-scores at infinity
    g_score[start] = 0 # g-score of start node is 0
    f_score = {node: float("inf") for row in grid for node in row} # start all g-scores at infinity
    f_score[start] = manhattan_distance(start.get_position(), end.get_position()) # start the f-score of our start node at the heuristic from the start to end estimate

    nodes_in_queue = {start}

    while not open_nodes.empty():
        for event in pygame.event.get():
            # base case of quitting game for this own while loop although we have in main function
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current_node_being_analyzed = open_nodes.get()[2] # Our open nodes scores f-score, count, and node, and we just want the node
        nodes_in_queue.remove(current_node_being_analyzed)

        if current_node_being_analyzed == end:
            # we found the shortest path, so we need to reconstruct and draw the path 
            draw_path(prev_node, end, draw)
            start.set_start()
            end.set_end()
            return True
        
        for neighbor in current_node_being_analyzed.neighbors:
            temporary_g_score = g_score[current_node_being_analyzed] + 1 # we can assume all the edges are 1

            if temporary_g_score < g_score[neighbor]:
                # if we found better way to reach the neighbor, we need to update and keep track of that to construct path
                prev_node[neighbor] = current_node_being_analyzed
                g_score[neighbor] = temporary_g_score
                f_score[neighbor] = temporary_g_score + manhattan_distance(neighbor.get_position(), end.get_position()) 
                if neighbor not in nodes_in_queue:
                    counter += 1
                    open_nodes.put((f_score[neighbor], counter, neighbor))
                    nodes_in_queue.add(neighbor)
                    neighbor.set_open()
                
        draw()

        if current_node_being_analyzed != start:
            current_node_being_analyzed.set_closed()
        
    return False

def construct_grid(rows, width):
    grid = []
    gap = width // rows # Integer division by rows, this will give us what the width of each of the nodes should be
    for row in range(rows):
        grid.append([]) # Creating 2d list
        for col in range(rows):
            node = Node(row, col, gap, rows)
            grid[row].append(node)

    return grid # Return the grid that was constructed, made up of nodes

def render_grid_lines(win, rows, width):
    gap = width // rows
    for row in range(rows):
        pygame.draw.line(win, GREY, (0, row * gap), (width, row * gap))
        for col in range(rows):
            pygame.draw.line(win, GREY, (col * gap, 0), (col * gap, width))

def render_board(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw_node_to_screen(win)

    render_grid_lines(win, rows, width)
    pygame.display.update()

def get_node_clicked_on(pos, rows, width):
    # taking the position of x and y and dividing by the width of each of the nodes, this will give us the node we are clicking on
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50 # Easily changable
    grid = construct_grid(ROWS, width) # Gives us 2D list of nodes
    
    start = None
    end = None

    run = True
    started = False # Started algo or not

    while run:
        render_board(win, grid, ROWS, width)
        for event in pygame.event.get():
            # Check each event on the pygame canvas, this is how we know what user is doing
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # if left click
                position = pygame.mouse.get_pos()
                row, col = get_node_clicked_on(position, ROWS, width) # Get row and col we clicked on in the 2D list
                node = grid[row][col] # we can now index the row,col in the grid
                
                if not start and node != end: # so we cannot put start and end in same place
                    start = node
                    start.set_start()

                elif not end and node != start: # so we cannot put start and end in the same place
                    end = node
                    end.set_end()

                elif node != start and node != end:
                    node.set_wall()

            elif pygame.mouse.get_pressed()[2]:
                # if right click
                position = pygame.mouse.get_pos()
                row, col = get_node_clicked_on(position, ROWS, width) # Get row and col we clicked on in the 2D list
                node = grid[row][col] # we can now index the row,col in the grid
                node.reset_node() # makes it back to white (empty node)
                # Reset start and end if we make those reset
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Run the algorithm if the user presses space
                    for row in grid:
                        for node in row:
                            node.update_neighbor_nodes(grid)

                    # call anonymous function for A* algorithm, we do this to pass render_board function to another function
                    a_star(lambda: render_board(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = construct_grid(ROWS, width)


    pygame.quit()

main(WIN, WIDTH)

