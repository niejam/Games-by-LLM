import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Bros Clone")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Mario properties
mario_x = 100
mario_y = 400
mario_width = 50
mario_height = 50
mario_velocity_x = 0
mario_velocity_y = 0
gravity = 1
jump_strength = -15

# Platform properties
platforms = [
    pygame.Rect(300, 500, 200, 20),
    pygame.Rect(100, 400, 200, 20),
    pygame.Rect(500, 300, 200, 20)
]

# Function to check for collisions
def check_collision(rect, platforms):
    for platform in platforms:
        if rect.colliderect(platform):
            return True
    return False

# Main game loop
running = True
on_ground = False
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Horizontal movement
    if keys[pygame.K_LEFT]:
        mario_velocity_x = -5
    elif keys[pygame.K_RIGHT]:
        mario_velocity_x = 5
    else:
        mario_velocity_x = 0

    # Jumping
    if keys[pygame.K_SPACE] and on_ground:
        mario_velocity_y = jump_strength

    # Apply gravity
    mario_velocity_y += gravity

    # Update Mario's position
    mario_x += mario_velocity_x
    mario_y += mario_velocity_y

    # Create Mario's rectangle
    mario_rect = pygame.Rect(mario_x, mario_y, mario_width, mario_height)

    # Check for collisions with platforms
    on_ground = False
    for platform in platforms:
        if mario_rect.colliderect(platform) and mario_velocity_y > 0:
            mario_y = platform.top - mario_height
            mario_velocity_y = 0
            on_ground = True

    # Prevent Mario from falling through the bottom of the screen
    if mario_y + mario_height > SCREEN_HEIGHT:
        mario_y = SCREEN_HEIGHT - mario_height
        mario_velocity_y = 0
        on_ground = True

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Draw Mario
    pygame.draw.rect(screen, RED, mario_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()