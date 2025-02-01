import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 5
WINNING_SCORE = 10  # Number of enemies to destroy to win

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Fighter")

# Load assets
player_img = pygame.image.load("assets/fighter.png")
enemy_img = pygame.image.load("assets/fighter2.png")
background_img = pygame.image.load("assets/background_large.jpg")
bullet_img = pygame.image.load("assets/bullet.png")  # Load player bullet image
bullet_img = pygame.transform.scale(bullet_img, (15, 15))  # Resize bullet image

player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

# Game classes
class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.speed = PLAYER_SPEED
        self.bullets = []

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - 50:
            self.x += self.speed
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - 50:
            self.y += self.speed

    def shoot(self):
        self.bullets.append(Bullet(self.x + 20, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img  # Use the loaded bullet image
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = ENEMY_BULLET_SPEED
        self.width = 5
        self.height = 10

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed = ENEMY_SPEED
        self.enemy_bullets = []

    def move(self):
        self.y += self.speed

    def shoot(self):
        self.enemy_bullets.append(EnemyBullet(self.x + 20, self.y + 50))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

# Display Game Over Message
def show_message(message):
    font = pygame.font.Font(None, 30)
    text = font.render(message, True, RED)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH // 8, HEIGHT // 2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main game loop
def game_loop():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    score = 0

    while running:
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Move and draw bullets
        for bullet in player.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                enemies.append(Enemy())

            # Enemy shooting logic
            if random.random() < 0.01:  # 1% chance each frame to shoot
                enemy.shoot()

            # Move enemy bullets
            for enemy_bullet in enemy.enemy_bullets[:]:
                enemy_bullet.move()
                if enemy_bullet.y > HEIGHT:
                    enemy.enemy_bullets.remove(enemy_bullet)

        # Collision detection
        for enemy in enemies[:]:
            for bullet in player.bullets[:]:
                if enemy.x < bullet.x < enemy.x + 50 and enemy.y < bullet.y < enemy.y + 50:
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    enemies.append(Enemy())
                    score += 1
                    if score >= WINNING_SCORE:
                        running = False
                        show_message("You Win! Press R to Restart or Q to Quit")
                    break

            # Check if enemy collides with player
            if enemy.x < player.x + 50 and enemy.x + 50 > player.x and enemy.y < player.y + 50 and enemy.y + 50 > player.y:
                running = False  # End game if player is hit
                show_message("Game Over! Press R to Restart or Q to Quit")

            # Check if enemy bullets hit the player
            for enemy_bullet in enemy.enemy_bullets[:]:
                if enemy_bullet.x < player.x + 50 and enemy_bullet.x + 5 > player.x and enemy_bullet.y < player.y + 50 and enemy_bullet.y + 10 > player.y:
                    running = False  # End game if player is hit
                    show_message("Game Over! Press R to Restart or Q to Quit")

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the game
game_loop()
