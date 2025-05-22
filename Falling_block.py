import pygame
import random
import sys
import time
from datetime import datetime

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 600, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 128, 255)
BLOCK_COLOR = (255, 0, 0)
BUTTON_COLOR = (0, 200, 0)
PAUSE_COLOR = (200, 200, 0)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
tiny_font = pygame.font.SysFont(None, 24)

# Load background image
try:
    background = pygame.image.load("forest_background_image.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print("Error loading background image:", e)
    background = None

# Player Class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, self.width, self.height)
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)

# Falling Block Class
class Block:
    def __init__(self):
        self.size = 50
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(-150, -50)
        self.speed = random.randint(4, 8)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLOCK_COLOR, self.rect)

# Helper functions
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(window, color, (x, y, w, h))
    label = small_font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(label, label_rect)
    return pygame.Rect(x, y, w, h)

def draw_creator():
    creator_text = tiny_font.render("Created by Tulsi Bedarkar", True, BLACK)
    window.blit(creator_text, (WIDTH - creator_text.get_width() - 10, HEIGHT - creator_text.get_height() - 10))

def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    if minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} {secs} second{'s' if secs != 1 else ''}"
    else:
        return f"{secs} second{'s' if secs != 1 else ''}"

# Main Game Loop
def main():
    player = Player()
    blocks = [Block() for _ in range(5)]
    game_started = False
    game_paused = False
    game_over = False
    start_time = 0
    elapsed_time = 0

    last_duration = ""
    last_played_time = ""

    while True:
        clock.tick(60)

        if background:
            window.blit(background, (0, 0))
        else:
            window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if not game_started:
                    if start_button.collidepoint(mx, my):
                        player = Player()
                        blocks = [Block() for _ in range(5)]
                        game_over = False
                        game_started = True
                        game_paused = False
                        start_time = time.time()
                elif game_started and not game_over:
                    if pause_button.collidepoint(mx, my):
                        game_paused = not game_paused

        if not game_started:
            title = font.render("Dodge the Falling Blocks", True, BLACK)
            window.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
            start_button = draw_button("Start Game", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, BUTTON_COLOR)

            if last_duration:
                dur_text = small_font.render(f"Last duration: {last_duration}", True, BLACK)
                window.blit(dur_text, dur_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))

            if last_played_time:
                time_text = tiny_font.render(f"Last played: {last_played_time}", True, BLACK)
                window.blit(time_text, time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110)))

            draw_creator()

        elif game_started and not game_paused and not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.draw(window)

            for block in blocks:
                block.fall()
                block.draw(window)
                if block.rect.top > HEIGHT:
                    block.__init__()
                if block.rect.colliderect(player.rect):
                    game_over = True
                    game_started = False
                    elapsed_time = time.time() - start_time
                    last_duration = format_duration(elapsed_time)
                    last_played_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            pause_button = draw_button("Pause", 10, 10, 100, 40, PAUSE_COLOR)
            draw_creator()

        elif game_paused:
            paused_text = font.render("Game Paused", True, BLACK)
            window.blit(paused_text, paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pause_button = draw_button("Resume", 10, 10, 100, 40, PAUSE_COLOR)
            draw_creator()

        elif game_over:
            over_text = font.render("Game Over!", True, BLACK)
            window.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

            dur_text = small_font.render(f"Duration: {last_duration}", True, BLACK)
            window.blit(dur_text, dur_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))

            time_text = tiny_font.render(f"Last played: {last_played_time}", True, BLACK)
            window.blit(time_text, time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

            start_button = draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 + 90, 150, 50, BUTTON_COLOR)
            draw_creator()

        pygame.display.flip()

if __name__ == "__main__":
    main()
