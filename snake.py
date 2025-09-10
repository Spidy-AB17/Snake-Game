import pygame
import random
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()

# --- Load Sounds (replace with your wav files if available) ---
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
    special_sound = pygame.mixer.Sound("special.mp3")  # NEW
except:
    eat_sound = None
    gameover_sound = None
    special_sound = None


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 215, 0)
BG_COLOR = (230, 240, 255)
BORDER_COLOR = (40, 40, 40)
SPECIAL_COLOR = (255, 100, 0)

# Screen size
WIDTH = 600
HEIGHT = 400

# Create game window
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYTHON 🐍 ")

# Clock
clock = pygame.time.Clock()
SNAKE_SIZE = 15
snake_speed = 12  # base speed

# Fonts
title_font = pygame.font.SysFont("comicsansms", 50, bold=True)
menu_font = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansms", 32, bold=True)


def draw_score(score):
    """Draws a modern scoreboard at top center"""
    score_text = score_font.render(f"Score: {score}", True, YELLOW)
    shadow = score_font.render(f"Score: {score}", True, BLACK)
    dis.blit(shadow, [WIDTH / 2 - score_text.get_width() / 2 + 2, 8 + 2])
    dis.blit(score_text, [WIDTH / 2 - score_text.get_width() / 2, 8])


def draw_snake(snake_list):
    """Draw snake with rounded body and a head with eyes & tongue"""
    for i, (x, y) in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head
            pygame.draw.circle(dis, DARK_GREEN, (x, y), SNAKE_SIZE // 2 + 2)
            # Eyes
            pygame.draw.circle(dis, WHITE, (x - 3, y - 3), 2)
            pygame.draw.circle(dis, WHITE, (x + 3, y - 3), 2)
            pygame.draw.circle(dis, BLACK, (x - 3, y - 3), 1)
            pygame.draw.circle(dis, BLACK, (x + 3, y - 3), 1)
            # Tongue
            pygame.draw.line(dis, RED, (x, y + 5), (x, y + 12), 2)
            pygame.draw.line(dis, RED, (x, y + 12), (x - 3, y + 15), 2)
            pygame.draw.line(dis, RED, (x, y + 12), (x + 3, y + 15), 2)
        else:  # Body
            pygame.draw.circle(dis, GREEN, (x, y), SNAKE_SIZE // 2)


def message_screen(msg, size=30, color=RED, y_offset=0):
    """Utility for centered messages"""
    font = pygame.font.SysFont("bahnschrift", size)
    text = font.render(msg, True, color)
    dis.blit(text, [WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 + y_offset])


def game_loop():
    global snake_speed
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1
    score = 0
    foods_eaten = 0

    food_x = random.randrange(20, WIDTH - 20, 10)
    food_y = random.randrange(50, HEIGHT - 20, 10)

    # Special food
    special_active = False
    special_start_time = 0
    special_x, special_y = 0, 0

    while not game_over:

        while game_close:
            dis.fill(BG_COLOR)
            draw_score(score)
            message_screen("You Lost!", 40, RED, -40)
            message_screen("Press C-Play Again or Q-Quit", 25, BLACK, 20)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_speed = 12
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -SNAKE_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = SNAKE_SIZE
                    dx = 0

        # Border check
        if x >= WIDTH - 10 or x < 10 or y >= HEIGHT - 10 or y < 40:
            if gameover_sound: gameover_sound.play()
            game_close = True

        x += dx
        y += dy
        dis.fill(BG_COLOR)

        # Borders
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, WIDTH, 40])  # top
        pygame.draw.rect(dis, BORDER_COLOR, [0, 0, 10, HEIGHT])  # left
        pygame.draw.rect(dis, BORDER_COLOR, [WIDTH - 10, 0, 10, HEIGHT])  # right
        pygame.draw.rect(dis, BORDER_COLOR, [0, HEIGHT - 10, WIDTH, 10])  # bottom

        # Food
        pygame.draw.circle(dis, RED, (food_x, food_y), SNAKE_SIZE // 2)

        # Special food
        if special_active:
            if int(time.time() * 2) % 2 == 0:
                pygame.draw.circle(dis, SPECIAL_COLOR, (special_x, special_y), SNAKE_SIZE)
            if time.time() - special_start_time > 5:
                special_active = False

        # Snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                if gameover_sound: gameover_sound.play()
                game_close = True

        draw_snake(snake_list)
        draw_score(score)
        pygame.display.update()

        # Eating food
        if abs(x - food_x) < SNAKE_SIZE and abs(y - food_y) < SNAKE_SIZE:
            if eat_sound: eat_sound.play()
            food_x = random.randrange(20, WIDTH - 20, 10)
            food_y = random.randrange(50, HEIGHT - 20, 10)
            snake_length += 1
            score += 1
            foods_eaten += 1
            if score % 5 == 0:
                snake_speed += 1
            if foods_eaten % 7 == 0:
              special_active = True
              special_start_time = time.time()
              special_x = random.randrange(20, WIDTH - 20, 10)
              special_y = random.randrange(50, HEIGHT - 20, 10)
              if special_sound: 
                 special_sound.play()   # 🎵 pop sound when special food appears


        # Eating special food
        if special_active and abs(x - special_x) < SNAKE_SIZE and abs(y - special_y) < SNAKE_SIZE:
            if eat_sound: eat_sound.play()
            score += 5
            snake_length += 2
            special_active = False

        clock.tick(snake_speed)

    pygame.quit()
    quit()


def instructions_screen():
    """Instructions before game starts"""
    running = True
    while running:
        dis.fill(BG_COLOR)
        title = title_font.render("Instructions", True, DARK_GREEN)
        dis.blit(title, [WIDTH / 2 - title.get_width() / 2, 40])

        rules = [
            "1. Use Arrow keys to move the snake.",
            "2. Eat red balls to grow +1 point.",
            "3. Every 7 foods → big blinking ball (+5 points).",
            "   But it disappears in 5 seconds!",
            "4. Hitting borders or yourself = Game Over.",
            "5. Speed increases as score grows."
        ]
        font = pygame.font.SysFont("bahnschrift", 25)
        for i, line in enumerate(rules):
            text = font.render(line, True, BLACK)
            dis.blit(text, [50, 120 + i * 30])

        message_screen("Press B to go Back", 25, RED, 120)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                running = False


def main_menu():
    """Main menu with Start / Instructions / Quit"""
    running = True
    while running:
        dis.fill(BG_COLOR)
        title = title_font.render("Snake Game 🐍", True, DARK_GREEN)
        dis.blit(title, [WIDTH / 2 - title.get_width() / 2, 60])

        start_text = menu_font.render("1. Start Game", True, BLACK)
        inst_text = menu_font.render("2. Instructions", True, BLACK)
        quit_text = menu_font.render("3. Quit", True, BLACK)

        dis.blit(start_text, [WIDTH / 2 - start_text.get_width() / 2, 160])
        dis.blit(inst_text, [WIDTH / 2 - inst_text.get_width() / 2, 210])
        dis.blit(quit_text, [WIDTH / 2 - quit_text.get_width() / 2, 260])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()
                elif event.key == pygame.K_2:
                    instructions_screen()
                elif event.key == pygame.K_3:
                    running = False
                    pygame.quit()
                    quit()


# Start from main menu
main_menu()
