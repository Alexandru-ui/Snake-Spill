import pygame
import random
import sys
import requests
from io import BytesIO

# Initialiser pygame
pygame.init()

# Skjermstørrelse og innstillinger
WIDTH, HEIGHT = 1920, 1080
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Farger (RGB-verdier)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Klokke for kontroll av hastighet
clock = pygame.time.Clock()

# Font for poengvisning
font = pygame.font.Font(None, 36)

# Variabel for om bakgrunnsbildet skal vises eller ikke
background_enabled = True  # Sett til True for å vise bakgrunnen, False for å skjule

# Last ned bakgrunnsbildet
def load_background_image():
    url = "https://cdn.tutsplus.com/cdn-cgi/image/width=480/mobile/uploads/legacy/Corona-SDK_Build-A-Snake-Game/1/6.png"
    response = requests.get(url)
    img = BytesIO(response.content)
    background_image = pygame.image.load(img)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    return background_image

# Retninger som slangen kan bevege seg i
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    global background_enabled  # Bruk global variabel

    # Initialiser spillvariabler
    background_image = load_background_image()  # Last bakgrunnsbildet

    snake = [(5, 5), (4, 5), (3, 5)]  # Slangen starter med tre segmenter
    direction = RIGHT  # Startretning
    food = place_food(snake)  # Plasser mat på et tilfeldig sted
    score = 0  # Startpoeng
    speed = 15  # Startfart

    running = True  # Variabel som holder spillet i gang
    while running:
        # Håndtere hendelser (for eksempel lukking av vindu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Sjekk tastetrykk for å slå bakgrunnen av og på
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Trykk på 'B' for å slå bakgrunn på/av
                    background_enabled = not background_enabled

        # Håndtere tastetrykk (for å endre retningen på slangen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != DOWN:
            direction = UP
        if keys[pygame.K_DOWN] and direction != UP:
            direction = DOWN
        if keys[pygame.K_LEFT] and direction != RIGHT:
            direction = LEFT
        if keys[pygame.K_RIGHT] and direction != LEFT:
            direction = RIGHT
        
        # Oppdater slangens posisjon
        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # Sjekk kollisjon med vegger eller seg selv
        if (new_head in snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= WIDTH // CELL_SIZE or new_head[1] >= HEIGHT // CELL_SIZE):
            running = False

        # Legg til ny posisjon i slangen (nytt hode)
        snake.insert(0, new_head)

        # Sjekk om slangen spiser mat
        if new_head == food:
            score += 1
            speed += 0.5
            food = place_food(snake)
        else:
            snake.pop()

        # Tegn alt på skjermen
        if background_enabled:  # Hvis bakgrunn skal vises, tegn den
            screen.blit(background_image, (0, 0))

        draw_snake(snake)
        draw_food(food)
        draw_score(score)

        pygame.display.flip()
        clock.tick(speed)

    # Vis 'Game Over'-skjerm når spillet er over
    show_game_over(score)

def place_food(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1)
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1)
        if (x, y) not in snake:
            return (x, y)

def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else (0, 100, 0)
        pygame.draw.rect(screen, color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 30))
    screen.blit(text, text_rect)

def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()

if __name__ == "__main__":
    main()