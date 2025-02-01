import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = 3

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bird_images = [
    pygame.transform.scale(pygame.image.load("assets/bird1.png"), (30, 30)),  # Flap up image
    pygame.transform.scale(pygame.image.load("assets/bird2.png"), (30, 30))   # Flap down image
]
block_image = pygame.image.load("assets/block.png")  # Load block image for pipes
block_image = pygame.transform.scale(block_image, (PIPE_WIDTH, 400))  # Resize image for pipes
bird = pygame.Rect(BIRD_X, BIRD_Y, 30, 30)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
    
    def move(self):
        self.x -= PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self):
        screen.blit(block_image, (self.x, 0), (0, 400 - self.height, PIPE_WIDTH, self.height))  # Draw top pipe
        screen.blit(block_image, (self.x, self.height + PIPE_GAP), (0, 0, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))  # Draw bottom pipe

# Game variables
def game_loop():
    velocity = 0
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    clock = pygame.time.Clock()
    bird_frame = 0  # To alternate bird flapping frames

    def jump():
        nonlocal velocity, bird_frame
        velocity = FLAP_STRENGTH
        bird_frame = 1  # Change to flapping image
    
    while running:
        screen.fill(BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump()
        
        # Bird mechanics
        velocity += GRAVITY
        bird.y += velocity
        bird_frame = 0 if velocity > 0 else 1  # Switch bird image depending on motion
        
        if bird.y >= HEIGHT or bird.y <= 0:
            running = False  # Game over if bird goes off-screen
        
        screen.blit(bird_images[bird_frame], (bird.x, bird.y))  # Draw bird image with animation
        
        # Pipe mechanics
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH))
                score += 1  # Increase score when a pipe is passed
            
            # Collision detection
            if bird.colliderect(pipe.top_rect) or bird.colliderect(pipe.bottom_rect):
                running = False  # Game over
        
        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
        
        pygame.display.update()
        clock.tick(30)
    
    end_game(score)

def end_game(score):
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 50)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    
    font = pygame.font.Font(None, 36)
    retry_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

game_loop()
