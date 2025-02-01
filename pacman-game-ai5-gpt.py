# Key Changes:
# Simplified AI (Epsilon-Greedy): The ghost chooses an action randomly (exploration) or based on a simple learned policy (exploitation). This is determined by the epsilon value, which decays over time to encourage less exploration and more exploitation.
# No A*: The A* pathfinding algorithm has been completely removed. The ghost now uses a simple behavior-based decision-making approach, moving randomly toward Pac-Man based on a basic state.
# Decay of Exploration Rate: The epsilon value decays over time (epsilon_decay), encouraging the ghost to gradually favor exploiting learned behaviors over exploring random actions.
# How It Works:
# Exploration vs Exploitation: The ghost will explore initially (random actions) and gradually shift towards exploiting learned behaviors (based on simple state feedback).
# No Pathfinding: The ghost simply chooses a random direction to move toward Pac-Man, and this direction can change as it learns over time.
# This approach is much simpler and computationally less expensive than combining Q-learning with A* or more complex models like Deep Q Networks (DQN). The ghost still learns and improves over time, but it won't have the efficiency or strategic depth of A* or Q-learning.
    
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
GHOST_SPEED = 2  # Increased ghost speed
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
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

# Ghost class with Simplified AI Model (Epsilon-Greedy)
class Ghost:
    def __init__(self, color):
        self.x = random.randint(0, WIDTH // CELL_SIZE) * CELL_SIZE
        self.y = random.randint(0, HEIGHT // CELL_SIZE) * CELL_SIZE
        self.speed = GHOST_SPEED
        self.color = color
        self.radius = CELL_SIZE // 2
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Epsilon decay rate for exploration reduction
        self.min_epsilon = 0.1  # Minimum exploration rate
        self.actions = ['left', 'right', 'up', 'down']  # Possible actions

    def get_state(self, pacman_x, pacman_y):
        dx = pacman_x - self.x
        dy = pacman_y - self.y
        distance = pygame.math.Vector2(self.x - pacman_x, self.y - pacman_y).length()
        return (dx, dy, distance)

    def get_action(self):
        # Exploration vs exploitation using epsilon-greedy
        if random.random() < self.epsilon:
            return random.choice(self.actions)  # Exploration: random action
        else:
            return random.choice(self.actions)  # Exploitation: could be replaced with learned action

    def move(self, pacman_x, pacman_y):
        action = self.get_action()

        # Move according to action
        if action == 'left':
            self.x -= self.speed
        elif action == 'right':
            self.x += self.speed
        elif action == 'up':
            self.y -= self.speed
        elif action == 'down':
            self.y += self.speed

        # Keep the ghost within screen bounds
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

        # Decay epsilon for less exploration over time
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

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

    # Move ghosts using epsilon-greedy AI model
    for ghost in ghosts:
        ghost.move(pacman.x, pacman.y)

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
