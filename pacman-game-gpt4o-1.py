import pygame
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Exit door color

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with AI Ghosts and Exit")

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 10

# Map layout (1 = wall, 0 = path, 2 = exit)
LEVEL = [
    "11111111111111111111",
    "10000000001100000001",
    "10111101101101111101",
    "10111101100001111101",
    "10000000001100000001",
    "10110111111111101101",
    "10010100000000010101",
    "11110101101111010111",
    "11110101101111010111",
    "10000000000000000001",
    "10111111111111111101",
    "10000000001100000001",
    "10111101101101111101",
    "10111101101101111101",
    "10000001100001100001",
    "11110111111111101111",
    "11110000000000002111",  # Exit is at the bottom-right corner
    "11111111111111111111"
]
ROWS, COLS = len(LEVEL), len(LEVEL[0])

# Load game map as a grid
grid = [[int(cell) for cell in row] for row in LEVEL]

# Define helper functions for drawing
def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 2:  # Draw the exit door
                pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] in (0, 2):  # Allow paths and exit
            neighbors.append((nx, ny))
    return neighbors

def bfs(start, target):
    """A simple Breadth-First Search to find the shortest path."""
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()

        if current == target:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]  # Return reversed path

# Define Pac-Man class
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)

    def move(self):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

# Define Ghost class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.path = []
        self.counter = 0  # Delay mechanism for ghost movement

    def move(self, target):
        # Only move every 3 frames (adjust delay here)
        if self.counter < 3:
            self.counter += 1
            return
        self.counter = 0
        if not self.path or (self.x, self.y) == self.path[0]:
            self.path = bfs((self.x, self.y), target)
        if self.path:
            next_step = self.path.pop(0)
            self.x, self.y = next_step

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

# Create game objects
pacman = PacMan(1, 1)
ghosts = [
    Ghost(10, 10, RED),
    Ghost(15, 15, BLUE)
]

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                pacman.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.direction = (1, 0)

    # Move Pac-Man
    pacman.move()

    # Check for exit condition
    if grid[pacman.y][pacman.x] == 2:  # Pac-Man reaches the exit
        print("You Win!")
        running = False

    # Move ghosts with AI (slowed down)
    for ghost in ghosts:
        ghost.move((pacman.x, pacman.y))

    # Check collision with ghosts
    for ghost in ghosts:
        if (ghost.x, ghost.y) == (pacman.x, pacman.y):
            print("Pac-Man got caught!")
            running = False

    # Draw everything
    draw_grid()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()