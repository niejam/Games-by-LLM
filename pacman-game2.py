import pygame
import random

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
GHOST_SPEED = 3
score = 0

# Load fonts
font = pygame.font.SysFont("Arial", 24)

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
        # Draw Pac-Man as a circle with a mouth
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
        # Draw the mouth based on direction
        if self.direction == "right":
            start_angle = 0.78  # 45 degrees
            end_angle = 5.49    # 315 degrees
        elif self.direction == "left":
            start_angle = 3.92  # 225 degrees
            end_angle = 2.35    # 135 degrees
        elif self.direction == "up":
            start_angle = 5.49  # 315 degrees
            end_angle = 3.92    # 225 degrees
        elif self.direction == "down":
            start_angle = 2.35  # 135 degrees
            end_angle = 0.78    # 45 degrees
        pygame.draw.polygon(screen, BLACK, [
            (self.x, self.y),
            (self.x + self.radius * pygame.math.Vector2(1, 0).rotate(start_angle * 57.3).x,
             self.y + self.radius * pygame.math.Vector2(1, 0).rotate(start_angle * 57.3).y),
            (self.x + self.radius * pygame.math.Vector2(1, 0).rotate(end_angle * 57.3).x,
             self.y + self.radius * pygame.math.Vector2(1, 0).rotate(end_angle * 57.3).y)
        ])

# Ghost class
class Ghost:
    def __init__(self, color):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = GHOST_SPEED
        self.color = color
        self.radius = CELL_SIZE // 2
        self.direction = random.choice(["left", "right", "up", "down"])

    def move(self):
        # Move the ghost in its current direction
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Keep ghost within screen bounds
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

        # Randomly change direction
        if random.randint(0, 100) < 5:  # 5% chance to change direction
            self.direction = random.choice(["left", "right", "up", "down"])

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
ghosts = [Ghost(RED), Ghost(BLUE)]  # Add two ghosts
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

    # Move ghosts
    for ghost in ghosts:
        ghost.move()

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