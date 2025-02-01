# Key Improvements:
# Increased Speed: The ghost's movement speed is increased by setting GHOST_SPEED = 1.5, making the chase faster.
# Learning Rate (alpha): The learning rate is increased to 0.3, allowing faster learning of good actions.
# Epsilon Decay: The decay of epsilon is faster with epsilon_decay = 0.999, encouraging the ghost to transition from exploration to exploitation more quickly.
# Reward System: A stronger negative reward is given if the ghost collides with Pac-Man (penalizing it heavily for failure).

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
GHOST_SPEED = 10  # Increased speed for the ghost
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

# Ghost class with Q-learning AI
class Ghost:
    def __init__(self, color):
        self.x = random.randint(0, WIDTH // CELL_SIZE) * CELL_SIZE
        self.y = random.randint(0, HEIGHT // CELL_SIZE) * CELL_SIZE
        self.speed = GHOST_SPEED
        self.color = color
        self.radius = CELL_SIZE // 2
        self.q_table = {}  # Q-table for storing state-action values
        self.alpha = 0.5  # Increased learning rate for faster learning
        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration rate (epsilon-greedy)
        self.epsilon_decay = 0.999  # Faster decay rate for epsilon
        self.min_epsilon = 0.1  # Minimum exploration rate

    def get_state(self, pacman_x, pacman_y):
        # The state can be represented by the relative position and distance to Pac-Man
        dx = pacman_x - self.x
        dy = pacman_y - self.y
        distance = pygame.math.Vector2(self.x - pacman_x, self.y - pacman_y).length()
        return (dx, dy, distance)

    def get_action(self, state):
        # Explore or exploit based on epsilon-greedy
        if random.random() < self.epsilon:
            # Exploration: choose a random action
            return random.choice(['left', 'right', 'up', 'down'])
        else:
            # Exploitation: choose the best action based on Q-table
            if state not in self.q_table:
                self.q_table[state] = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
            return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, reward, next_state):
        # Initialize state and action if not in Q-table
        if state not in self.q_table:
            self.q_table[state] = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
        if next_state not in self.q_table:
            self.q_table[next_state] = {'left': 0, 'right': 0, 'up': 0, 'down': 0}

        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += self.alpha * (td_target - self.q_table[state][action])

    def move_towards(self, pacman_x, pacman_y):
        state = self.get_state(pacman_x, pacman_y)
        action = self.get_action(state)

        # Perform the action
        if action == 'left':
            self.x -= self.speed
        elif action == 'right':
            self.x += self.speed
        elif action == 'up':
            self.y -= self.speed
        elif action == 'down':
            self.y += self.speed

        # Keep ghost within screen bounds
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

        # Calculate next state after the move
        next_state = self.get_state(pacman_x, pacman_y)

        # Reward system: positive reward for getting closer to Pac-Man, negative reward for getting further or colliding
        distance = pygame.math.Vector2(self.x - pacman_x, self.y - pacman_y).length()
        reward = -distance  # negative reward for being farther away (or less negative for being closer)

        # If the ghost collides with Pac-Man, it gets a big negative reward (game over scenario)
        if distance < self.radius + 10:
            reward = -100  # Game over penalty

        # Update Q-table using the observed reward and new state
        self.update_q_table(state, action, reward, next_state)

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

    # Move ghosts using Q-learning
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
