import pygame
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions and tile size
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Police and Innocent Man")
clock = pygame.time.Clock()
FPS = 10

# Game level (1 = wall, 0 = path, 2 = exit)
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
    "11110000000000002111",
    "11111111111111111111"
]
ROWS, COLS = len(LEVEL), len(LEVEL[0])
grid = [[int(cell) for cell in row] for row in LEVEL]

# Load game assets
PACMAN_FRAMES = [
    pygame.image.load("assets/man1.png"), #pacman2_open.png"),
    pygame.image.load("assets/man2.png"), #pacman2_closed.png")
]
GHOST_SPRITES = {
    "red": pygame.image.load("assets/police1.png"), #ghost_red.png"),
    "blue": pygame.image.load("assets/police3.png")
}
WALL_TILE = pygame.image.load("assets/fence.png")
EXIT_TILE = pygame.image.load("assets/exit_tile.png")
BACKGROUND_IMAGE = pygame.image.load("assets/background.png")

# UI font
FONT = pygame.font.Font(None, 36)

# Helper Functions
def draw_background():
    """Draw the background image."""
    screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))


def draw_grid():
    """Render the level layout with wall and exit tiles."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                screen.blit(pygame.transform.scale(WALL_TILE, (TILE_SIZE, TILE_SIZE)), (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == 2:  # Exit door
                screen.blit(pygame.transform.scale(EXIT_TILE, (TILE_SIZE, TILE_SIZE)), (x * TILE_SIZE, y * TILE_SIZE))


def get_neighbors(pos):
    """Return valid neighboring positions."""
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] in (0, 2):  # Walkable tiles
            neighbors.append((nx, ny))
    return neighbors


def bfs(start, target):
    """Breadth-First Search to find shortest path."""
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
    return path[::-1]  # Reverse path


class PacMan:
    """Pac-Man character."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.frame = 0

    def move(self):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self):
        # Alternate between open and closed mouth every frame
        sprite = PACMAN_FRAMES[self.frame // 10 % len(PACMAN_FRAMES)]
        screen.blit(pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE)), (self.x * TILE_SIZE, self.y * TILE_SIZE))
        self.frame += 1


class Ghost:
    """Ghost character with basic AI."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.sprite = pygame.transform.scale(GHOST_SPRITES[color], (TILE_SIZE, TILE_SIZE))
        self.path = []
        self.counter = 0

    def move(self, target):
        if self.counter < 3:  # Move every 3 frames
            self.counter += 1
            return
        self.counter = 0
        if not self.path or (self.x, self.y) == self.path[0]:
            self.path = bfs((self.x, self.y), target)
        if self.path:
            next_step = self.path.pop(0)
            self.x, self.y = next_step

    def draw(self):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))


def draw_ui(score, lives):
    """Render UI showing score and lives."""
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))
    for i in range(lives):
        screen.blit(pygame.transform.scale(PACMAN_FRAMES[0], (TILE_SIZE, TILE_SIZE)),
                    (WIDTH - (i + 1) * TILE_SIZE - 10, HEIGHT - 40))


# Initialize game objects
pacman = PacMan(1, 1)
ghosts = [
    Ghost(10, 10, "red"),
    Ghost(15, 15, "blue")
]

score = 0
lives = 3
running = True

while running:
    draw_background()  # Draw the background
    draw_grid()        # Draw level layout
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

    # Update Pac-Man
    pacman.move()
    if grid[pacman.y][pacman.x] == 2:  # Reached exit
        print("You Win!")
        running = False

    # Update ghosts
    for ghost in ghosts:
        ghost.move((pacman.x, pacman.y))
        if (ghost.x, ghost.y) == (pacman.x, pacman.y):  # Collision
            lives -= 1
            print("Pac-Man got caught!")
            if lives <= 0:
                print("Game Over!")
                running = False

    # Draw characters and UI
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    draw_ui(score, lives)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()