import pygame  # Importerer pygame for spillutvikling
import random  # Importerer random for å lage tilfeldig matplassering
import sys  # Importerer sys for systemkommandoer (som avslutning av programmet)
import os  # Importerer os (ikke brukt her, men kan brukes for filhåndtering)

# Initialiser pygame
pygame.init()

# Skjermstørrelse og innstillinger
WIDTH, HEIGHT = 900, 700  # Definerer bredde og høyde på skjermen
CELL_SIZE = 20  # Definerer størrelsen på cellene til slangen og maten
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Lager skjerm med ønsket størrelse
pygame.display.set_caption("Snake Game")  # Setter tittelen på spillvinduet

# Farger (RGB-verdier)
WHITE = (255, 255, 255) 
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)  # Mørk bakgrunnsfarge

# Klokke for kontroll av hastighet
clock = pygame.time.Clock()

# Font for poengvisning
font = pygame.font.Font(None, 36)  # Lager font for poengsummen, størrelse 36

# Retninger som slangen kan bevege seg i
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    # Initialiser spillvariabler
    snake = [(5, 5), (4, 5), (3, 5)]  # Slangen starter med tre segmenter
    direction = RIGHT  # Startretning
    food = place_food(snake)  # Plasser mat på et tilfeldig sted
    score = 0  # Startpoeng
    speed = 10  # Startfart

    running = True  # Variabel som holder spillet i gang
    while running:
        # Håndtere hendelser (for eksempel lukking av vindu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        head = snake[0]  # Hent posisjonen til hodet på slangen
        new_head = (head[0] + direction[0], head[1] + direction[1])  # Beregn ny posisjon for hodet

        # Sjekk kollisjon med vegger eller seg selv
        if (new_head in snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= WIDTH // CELL_SIZE or new_head[1] >= HEIGHT // CELL_SIZE):
            running = False  # Slutt spillet hvis slangen treffer seg selv eller veggen

        # Legg til ny posisjon i slangen (nytt hode)
        snake.insert(0, new_head)

        # Sjekk om slangen spiser mat
        if new_head == food:
            score += 1  # Øk poengsummen
            speed += 0.5  # Øk hastigheten
            food = place_food(snake)  # Plasser ny mat
        else:
            snake.pop()  # Fjern halen på slangen (slangen vokser ikke hvis den ikke har spist mat)

        # Tegn alt på skjermen
        screen.fill(BACKGROUND_COLOR)  # Fyll skjermen med bakgrunnsfarge
        draw_snake(snake)  # Tegn slangen
        draw_food(food)  # Tegn maten
        draw_score(score)  # Tegn poengsummen

        # Oppdater skjermen
        pygame.display.flip()
        clock.tick(speed)  # Begrens spillets hastighet

    # Vis 'Game Over'-skjerm når spillet er over
    show_game_over(score)

def place_food(snake):
    """Plasser mat på et tilfeldig sted som ikke kolliderer med slangen."""
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1)  # Velg tilfeldig x-posisjon
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1)  # Velg tilfeldig y-posisjon
        if (x, y) not in snake:  # Hvis posisjonen ikke er på slangen
            return (x, y)  # Returner posisjonen for maten

def draw_snake(snake):
    """Tegn slangen på skjermen."""
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else (0, 100, 0)  # Farger hodet lysere enn kroppen
        pygame.draw.rect(screen, color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    """Tegn maten på skjermen."""
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    """Vis poengsummen på skjermen."""
    text = font.render(f"Score: {score}", True, WHITE)  # Lag tekst for poeng
    text_rect = text.get_rect(center=(WIDTH // 2, 30))  # Plasser teksten midt på skjermen øverst
    screen.blit(text, text_rect)

def show_game_over(score):
    """Vis 'Game Over'-skjermen og gi mulighet til å starte på nytt."""
    screen.fill(BLACK)  # Fyll skjermen med svart bakgrunn
    game_over_text = font.render("Game Over", True, RED)  # Lag tekst for Game Over
    score_text = font.render(f"Final Score: {score}", True, WHITE)  # Lag tekst for sluttscore
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)  # Tekst for å starte på nytt eller avslutte

    # Plasser og vis tekstene på skjermen
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()  # Oppdater skjermen

    # Vent på brukerinput for å starte på nytt eller avslutte
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart hvis R trykkes
            main()
        if keys[pygame.K_q]:  # Avslutt hvis Q trykkes
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()  # Start spillet når skriptet kjøres
