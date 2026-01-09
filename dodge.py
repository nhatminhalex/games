import pygame
import random
def main():
# 1. Setup and Initialization
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Avoid the Falling Blocks!")
    clock = pygame.time.Clock()

# Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 100)
    BLUE = (50, 50, 255)
    GREEN = (0, 255, 100) # Added a color for the second enemy

# Player Properties
    player_size = 50
    player_pos = [WIDTH // 2, HEIGHT - player_size - 10]

# Obstacle 1 Properties
    enemy_size = 50
    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
    enemy_speed = 5

# Obstacle 2 Properties (Fixed: Started at -200 so they are staggered)
    enemy2_size = 50
    enemy2_pos = [random.randint(0, WIDTH - enemy2_size), -200] 
    enemy2_speed = 5

    score = 0
    running = True

# 2. Main Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 10
    # 3. Game Logic
    # Move Enemy 1
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > HEIGHT:
            enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
            score += 1
            enemy_speed += 0.1

    # Move Enemy 2
        enemy2_pos[1] += enemy2_speed
        if enemy2_pos[1] > HEIGHT:
            enemy2_pos = [random.randint(0, WIDTH - enemy2_size), 0]
            score += 1
            enemy2_speed += 0.1
    # Collision Detection
        p_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        e_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
        e2_rect = pygame.Rect(enemy2_pos[0], enemy2_pos[1], enemy2_size, enemy2_size)

        if p_rect.colliderect(e_rect) or p_rect.colliderect(e2_rect):
            print(f"Game Over! Final Score: {score}")
            running = False

    # 4. Rendering (Drawing)
        screen.fill((0, 0, 0)) 
    
        pygame.draw.rect(screen, BLUE, p_rect)   # Draw Player
        pygame.draw.rect(screen, RED, e_rect)    # Draw Enemy 1
        pygame.draw.rect(screen, GREEN, e2_rect) # FIXED: Added drawing for Enemy 2

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()