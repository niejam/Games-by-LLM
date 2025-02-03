import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions and tile size
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Learning Game")
clock = pygame.time.Clock()
FPS = 10

# Game level layout (1 = wall, 0 = path, 2 = exit tile)
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

def get_valid_positions():
    """Pre-compute and return all valid positions where Pac-Man can move."""
    valid_positions = []
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 0:  # `0` indicates a valid tile (walkable)
                valid_positions.append((x, y))
    return valid_positions
# Get all valid positions for placing answers
valid_positions = get_valid_positions()

# Load game assets
PACMAN_FRAMES = [
    pygame.image.load("assets/man1.png"),
    pygame.image.load("assets/man2.png"),
]
GHOST_SPRITES = {
    "red": pygame.image.load("assets/police1.png"),
    "blue": pygame.image.load("assets/police3.png"),
}
WALL_TILE = pygame.image.load("assets/fence.png")
BACKGROUND_IMAGE = pygame.image.load("assets/background.png")

# UI font
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 48)


def draw_answers(answers):
    """Draw the answer circles with numbers inside."""
    for answer, ax, ay in answers:
        # Draw a green circle for the answer
        pygame.draw.circle(
            screen, GREEN, (ax * TILE_SIZE + TILE_SIZE // 2, ay * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2
        )
        # Draw the associated number on the circle
        answer_text = FONT.render(str(answer), True, BLACK)  # Number text in black
        screen.blit(
            answer_text,
            (
                ax * TILE_SIZE + TILE_SIZE // 2 - answer_text.get_width() // 2,
                ay * TILE_SIZE + TILE_SIZE // 2 - answer_text.get_height() // 2,
            ),
        )


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
            self.path = self.bfs((self.x, self.y), target)
        if self.path:
            next_step = self.path.pop(0)
            self.x, self.y = next_step

    def bfs(self, start, target):
        """Breadth-First Search to find shortest path."""
        queue = deque([start])
        came_from = {start: None}
        while queue:
            current = queue.popleft()
            if current == target:
                break
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] in (0, 2):
                neighbors.append((nx, ny))
        return neighbors

    def draw(self):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))


def draw_background():
    """Draw the background image."""
    screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT)), (0, 0))


def draw_grid():
    """Render the level layout with wall and exit tiles."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                screen.blit(pygame.transform.scale(WALL_TILE, (TILE_SIZE, TILE_SIZE)), (x * TILE_SIZE, y * TILE_SIZE))


def draw_math_question(question):
    """Display the current math question on the screen."""
    text = BIG_FONT.render(question, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

def draw_scorelives(score, lives):
    """Render UI showing score and lives."""
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))
    for i in range(lives):
        screen.blit(pygame.transform.scale(PACMAN_FRAMES[0], (TILE_SIZE, TILE_SIZE)),
                    (WIDTH - (i + 1) * TILE_SIZE - 10, HEIGHT - 40))
        
def main():
    pacman = PacMan(1, 1)
    ghosts = [
        Ghost(10, 10, "red"),
        Ghost(15, 15, "blue"),
    ]

    math_questions = [("3 + 5", 8), ("7 - 3", 4), ("6 * 2", 12), ("10 / 2", 5)]
    current_question, correct_answer = random.choice(math_questions)
    print(current_question, correct_answer)

    #answers = [(random.randint(1, 20), x, y) for x, y in [(5, 5), (7, 8), (12, 12)]]
    # Place answers randomly within valid positions
    answers = []
    for _ in range(3):  # Generate 3 random wrong answers
        wrong_answer = random.randint(1, 20)
        while wrong_answer == correct_answer:  # Ensure wrong answers are not duplicates of the correct answer
            wrong_answer = random.randint(1, 20)
        x, y = random.choice(valid_positions)
        valid_positions.remove((x, y))  # Remove this position to avoid overlapping
        answers.append((wrong_answer, x, y))

    # Add the correct answer at a valid position
    x, y = random.choice(valid_positions)
    answers.append((correct_answer, x, y))
    valid_positions.remove((x, y))

    #answers.append((correct_answer, random.randint(1, COLS - 2), random.randint(1, ROWS - 2)))
    #print(answers)

    score = 0
    lives = 1
    running = True

    while running:
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

        pacman.move()

        # Update ghosts
        for ghost in ghosts:
            ghost.move((pacman.x, pacman.y))
            if (ghost.x, ghost.y) == (pacman.x, pacman.y):  # Collision
                lives -= 1
                print("Pac-Man got caught!")
                if lives <= 0:
                    print("Game Over!")
                    running = False

        # Check if Pac-Man collects any answer
        for answer, ax, ay in answers[:]:
            if (pacman.x, pacman.y) == (ax, ay):
                answers.remove((answer, ax, ay))
                if answer == correct_answer:
                    score += 1
                    print("Correct!")
                else:
                    lives -= 1
                    print("Incorrect!")
                running = False

        # if lives <= 0:
        #     print("Game Over!")
        #     running = False
        # elif not answers:  # All answers collected
        #     print("You Win!")
        #     running = False

        draw_background()
        draw_grid()
        pacman.draw()
        for ghost in ghosts:
            ghost.move((pacman.x, pacman.y))
            ghost.draw()
        draw_math_question(f"{current_question} = ?")
        #for answer, ax, ay in answers:
        #    pygame.draw.circle(screen, GREEN, (ax * TILE_SIZE + TILE_SIZE // 2, ay * TILE_SIZE + TILE_SIZE // 2), 15)
        draw_answers(answers)

        draw_scorelives(score, lives)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()