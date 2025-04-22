import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 8
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_FONT_SIZE = 64
INSTRUCTION_FONT_SIZE = 24
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
instruction_font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_dashed_line():
    dash_length = 20
    for y in range(0, HEIGHT, dash_length * 2):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + dash_length), 2)

def reset_ball():
    ball_rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])
    return ball_rect, ball_speed_x, ball_speed_y

def show_menu():
    menu_active = True
    
    while menu_active:
        screen.fill(BLACK)
        draw_text("PING PONG", score_font, WHITE, WIDTH // 2, HEIGHT // 4)
        draw_text("1 - Single Player (vs AI)", instruction_font, WHITE, WIDTH // 2, HEIGHT // 2 - 30)
        draw_text("2 - Two Players", instruction_font, WHITE, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("ESC - Quit", instruction_font, WHITE, WIDTH // 2, HEIGHT // 2 + 90)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "two_player"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(FPS)

def game_loop(mode):
    left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect, ball_speed_x, ball_speed_y = reset_ball()
    
    left_score = 0
    right_score = 0
    
    game_active = True
    
    ai_difficulty = 0.8
    
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        
        if mode == "two_player":
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += PADDLE_SPEED
        else:
            ideal_y = ball_rect.centery - PADDLE_HEIGHT // 2
            
            if random.random() > ai_difficulty:
                ideal_y += random.randint(-30, 30)
            
            if right_paddle.centery < ideal_y and right_paddle.bottom < HEIGHT:
                right_paddle.y += min(PADDLE_SPEED, ideal_y - right_paddle.centery)
            elif right_paddle.centery > ideal_y and right_paddle.top > 0:
                right_paddle.y -= min(PADDLE_SPEED, right_paddle.centery - ideal_y)
        
        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y
        
        if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
            ball_speed_y *= -1
        
        if ball_rect.colliderect(left_paddle) or ball_rect.colliderect(right_paddle):
            ball_speed_x *= -1
            
            ball_speed_y += random.uniform(-1, 1)
            
            ball_speed_y = max(min(ball_speed_y, BALL_SPEED_Y * 1.5), -BALL_SPEED_Y * 1.5)
        
        if ball_rect.left <= 0:
            right_score += 1
            ball_rect, ball_speed_x, ball_speed_y = reset_ball()
            
        if ball_rect.right >= WIDTH:
            left_score += 1
            ball_rect, ball_speed_x, ball_speed_y = reset_ball()
        
        screen.fill(BLACK)
        
        draw_dashed_line()
        
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball_rect)
        
        draw_text(str(left_score), score_font, WHITE, WIDTH // 4, 50)
        draw_text(str(right_score), score_font, WHITE, 3 * WIDTH // 4, 50)
        
        mode_text = "Single Player" if mode == "single" else "Two Players"
        draw_text(mode_text, instruction_font, WHITE, WIDTH // 2, 20)
        
        draw_text("W/S - Left Paddle", instruction_font, WHITE, 120, HEIGHT - 20)
        if mode == "two_player":
            draw_text("↑/↓ - Right Paddle", instruction_font, WHITE, WIDTH - 120, HEIGHT - 20)
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        mode = show_menu()
        
        result = game_loop(mode)

if __name__ == "__main__":
    main()