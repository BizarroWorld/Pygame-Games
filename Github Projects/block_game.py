import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 20
PLAYER_SPEED = 8
OBSTACLE_SPEED_MIN = 3
OBSTACLE_SPEED_MAX = 8
OBSTACLE_FREQUENCY = 30 
BG_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Dodger")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

def game_loop():
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 20
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    obstacles = []
    

    score = 0
    game_over = False
    frame_count = 0
    difficulty_timer = 0
    current_max_speed = OBSTACLE_SPEED_MAX
    current_frequency = OBSTACLE_FREQUENCY
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    return True 
        
        if game_over:
            screen.fill(BG_COLOR)
            game_over_text = font.render("Game Over! Score: " + str(score), True, TEXT_COLOR)
            restart_text = font.render("Press R to restart", True, TEXT_COLOR)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
            pygame.display.flip()
            clock.tick(60)
            continue
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += PLAYER_SPEED
        
        difficulty_timer += 1
        if difficulty_timer >= 1000: 
            current_max_speed = min(current_max_speed + 1, 15)
            current_frequency = max(current_frequency - 2, 10)
            difficulty_timer = 0
        
        frame_count += 1
        if frame_count >= current_frequency:
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
            obstacle_speed = random.randint(OBSTACLE_SPEED_MIN, current_max_speed)
            obstacles.append([pygame.Rect(obstacle_x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), obstacle_speed])
            frame_count = 0
        
        for obstacle in obstacles[:]:
            obstacle[0].y += obstacle[1]
            
            if obstacle[0].y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
            
            if player_rect.colliderect(obstacle[0]):
                game_over = True
        
        screen.fill(BG_COLOR)
        
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        
        for obstacle in obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle[0])
        
        score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    return False  

def main():
    restart = True
    while restart:
        restart = game_loop()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()