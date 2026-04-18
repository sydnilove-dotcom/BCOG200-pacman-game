import pygame
import random
from map import game_map
#must run via python3 game.py
pygame.init()
#map size and screen setup
CELL_SIZE = 40
ROWS = len(game_map)
COLS = len(game_map[0])
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

game_map = [list(row) for row in game_map]
score = 0
game_over = False
win = False
ghost_under = " "


def find_character(symbol):
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == symbol:
                return row, col


def count_pellets():
    total = 0
    for row in game_map:
        total += row.count(".")
        total += row.count("o")
    return total


def draw_game():
    screen.fill(BLACK)

    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            tile = game_map[row][col]

            if tile == "#":
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif tile == ".":
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 4)
            elif tile == "o":
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 8)
            elif tile == "P":
                pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 4)
            elif tile == "G":
                pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 4)

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))

    if game_over:
        lose_text = font.render("Game Over!", True, RED)
        screen.blit(lose_text, (WIDTH // 2 - 80, HEIGHT - 40))

    if win:
        win_text = font.render("You Win!", True, YELLOW)
        screen.blit(win_text, (WIDTH // 2 - 70, HEIGHT - 40))

    pygame.display.update()


def move_pacman(dx, dy):
    global score, game_over, win

    row, col = find_character("P")
    new_row = row + dy
    new_col = col + dx
    next_tile = game_map[new_row][new_col]

    if next_tile == "#":
        return

    if next_tile == ".":
        score += 10
    elif next_tile == "o":
        score += 50
    elif next_tile == "G":
        game_map[row][col] = " "
        game_map[new_row][new_col] = "P"
        game_over = True
        return

    game_map[row][col] = " "
    game_map[new_row][new_col] = "P"

    if count_pellets() == 0:
        win = True

#work on adding more ghosts and increasing speed as score icreases for more difficulty
def move_ghost():
    global ghost_under, game_over

    row, col = find_character("G")
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        new_row = row + dy
        new_col = col + dx
        next_tile = game_map[new_row][new_col]

        if next_tile == "#":
            continue

        if next_tile == "G":
            continue

        game_map[row][col] = ghost_under

        if next_tile == "P":
            ghost_under = " "
            game_map[new_row][new_col] = "G"
            game_over = True
            return

        if next_tile in [".", "o", " "]:
            ghost_under = next_tile
            game_map[new_row][new_col] = "G"
            return


running = True
ghost_timer = 0

while running:
    clock.tick(10)
    ghost_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over and not win:
            if event.key == pygame.K_LEFT:
                move_pacman(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_pacman(1, 0)
            elif event.key == pygame.K_UP:
                move_pacman(0, -1)
            elif event.key == pygame.K_DOWN:
                move_pacman(0, 1)

    if ghost_timer >= 5 and not game_over and not win:
        move_ghost()
        ghost_timer = 0

    draw_game()

pygame.quit()
