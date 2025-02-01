import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with Reinforcement Learning")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Q-Learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1

# Actions: UP, DOWN, LEFT, RIGHT
ACTIONS = [UP, DOWN, LEFT, RIGHT]

# Initialize Q-table
Q_TABLE = np.zeros((ROWS, COLS, len(ACTIONS)))

# Reward values
FOOD_REWARD = 10
GHOST_PENALTY = -50
MOVE_PENALTY = -1

# Pac-Man class
class PacMan:
    def __init__(self):
        self.position = [1, 1]  # Start position
        self.score = 0

    def move(self, direction):
        new_pos = [self.position[0] + direction[0], self.position[1] + direction[1]]
        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS:
            self.position = new_pos

    def draw(self):
        x, y = self.position[1] * CELL_SIZE, self.position[0] * CELL_SIZE
        pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)

# Ghost class
class Ghost:
    def __init__(self):
        self.position = [ROWS - 2, COLS - 2]  # Start position

    def choose_action(self, state):
        if random.uniform(0, 1) < EPSILON:
            return random.choice(ACTIONS)  # Explore
        else:
            q_values = Q_TABLE[state[0], state[1]]
            action_idx = np.argmax(q_values)
            return ACTIONS[action_idx]  # Exploit

    def move(self, action):
        new_pos = [self.position[0] + action[0], self.position[1] + action[1]]
        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS:
            self.position = new_pos

    def draw(self):
        x, y = self.position[1] * CELL_SIZE, self.position[0] * CELL_SIZE
        pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]

    def respawn(self):
        self.position = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]

    def draw(self):
        x, y = self.position[1] * CELL_SIZE, self.position[0] * CELL_SIZE
        pygame.draw.circle(screen, BLUE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)

# Check collision
def check_collision(pos1, pos2):
    return pos1 == pos2

# Main game loop
def main():
    pacman = PacMan()
    ghost = Ghost()
    food = Food()

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get user input for Pac-Man
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move(UP)
        elif keys[pygame.K_DOWN]:
            pacman.move(DOWN)
        elif keys[pygame.K_LEFT]:
            pacman.move(LEFT)
        elif keys[pygame.K_RIGHT]:
            pacman.move(RIGHT)

        # Ghost AI
        ghost_state = tuple(ghost.position)
        ghost_action = ghost.choose_action(ghost_state)
        ghost.move(ghost_action)

        # Update Q-table
        reward = MOVE_PENALTY
        if check_collision(pacman.position, food.position):
            pacman.score += FOOD_REWARD
            food.respawn()
            reward += FOOD_REWARD
        if check_collision(pacman.position, ghost.position):
            reward += GHOST_PENALTY
            print("Game Over! Score:", pacman.score)
            running = False

        # Update Q-value for the ghost
        max_future_q = np.max(Q_TABLE[ghost.position[0], ghost.position[1]])
        current_q = Q_TABLE[ghost_state[0], ghost_state[1], ACTIONS.index(ghost_action)]
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_future_q)
        Q_TABLE[ghost_state[0], ghost_state[1], ACTIONS.index(ghost_action)] = new_q

        # Draw everything
        pacman.draw()
        ghost.draw()
        food.draw()

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()