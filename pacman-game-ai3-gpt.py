import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
CELL_SIZE = 20
PACMAN_SPEED = 5
GHOST_SPEED = 0.000000001  # Reduced speed further for slowest movement
score = 0

# Load fonts
font = pygame.font.SysFont("Arial", 24)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = PACMAN_SPEED
        self.direction = "right"
        self.radius = CELL_SIZE // 2

    def move(self):
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Keep Pac-Man within screen bounds
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

# Ghost class with A* pathfinding
class Ghost:
    def __init__(self, color):
        self.x = random.randint(0, WIDTH // CELL_SIZE) * CELL_SIZE
        self.y = random.randint(0, HEIGHT // CELL_SIZE) * CELL_SIZE
        self.speed = GHOST_SPEED
        self.color = color
        self.radius = CELL_SIZE // 2
        self.path = []

    def astar_pathfinding(self, target_x, target_y):
        start = (self.x // CELL_SIZE, self.y // CELL_SIZE)
        goal = (target_x // CELL_SIZE, target_y // CELL_SIZE)
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if 0 <= next_pos[0] < WIDTH // CELL_SIZE and 0 <= next_pos[1] < HEIGHT // CELL_SIZE:
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + heuristic(goal, next_pos)
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current
        
        path = []
        current = goal
        while current != start:
            if current in came_from:
                path.append(current)
                current = came_from[current]
            else:
                break
        
        path.reverse()
        return path

    def move_towards(self, target_x, target_y):
        if not self.path or (self.x // CELL_SIZE, self.y // CELL_SIZE) == self.path[0]:
            self.path = self.astar_pathfinding(target_x, target_y)
        
        if self.path:
            next_pos = self.path.pop(0)
            self.x = next_pos[0] * CELL_SIZE
            self.y = next_pos[1] * CELL_SIZE

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Pellet class
class Pellet:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 5

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

# Create game objects
pacman = PacMan()
ghosts = [Ghost(RED), Ghost(BLUE)]  # Two AI ghosts
pellets = [Pellet() for _ in range(20)]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = "left"
            elif event.key == pygame.K_RIGHT:
                pacman.direction = "right"
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"

    # Move Pac-Man
    pacman.move()

    # Move ghosts using A*
    for ghost in ghosts:
        ghost.move_towards(pacman.x, pacman.y)

    # Check for collisions with pellets
    for pellet in pellets[:]:
        if pygame.math.Vector2(pacman.x - pellet.x, pacman.y - pellet.y).length() < pacman.radius + pellet.radius:
            pellets.remove(pellet)
            score += 10

    # Check for collisions with ghosts
    for ghost in ghosts:
        if pygame.math.Vector2(pacman.x - ghost.x, pacman.y - ghost.y).length() < pacman.radius + ghost.radius:
            running = False

    # Draw game objects
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    for pellet in pellets:
        pellet.draw()

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Game over
pygame.quit()
print(f"Game Over! Your score: {score}")
