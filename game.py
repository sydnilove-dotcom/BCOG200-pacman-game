import pygame
import random
from collections import deque
from map import game_map as starting_map
#update+add docstrings, type hints, and comments throughout --- IGNORE ---
# must run via python3 game.py
# map size and screen setup
CELL_SIZE = 40
ROWS = len(starting_map)
COLS = len(starting_map[0])
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 50
REPLAY_BUTTON = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 45, 120, 35)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GHOST_BLUE = (0, 120, 255)

screen = None
font = None
clock = None
game_map = [list(row) for row in starting_map]
score = 0
game_over = False
win = False
ghosts = []
eaten_ghosts = []
EXTRA_GHOST_STARTS = [(1, 13), (9, 13)]
frightened = False
frightened_end_time = 0
next_frightened_start = 0
FRIGHTENED_INTERVAL = 10000
FRIGHTENED_LENGTH = 7000
GHOST_POINTS = 200
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
GHOST_MOVE_DELAY = 6


def make_ghost(row: int, col: int, under: str) -> dict:
    """Create the dictionary used to track one ghost."""
    return {
        "row": row,
        "col": col,
        "start_row": row,
        "start_col": col,
        "under": under,
    }


def reset_game():
    """Restore the game to its starting state for a new round."""
    global game_map, score, game_over, win
    global frightened, frightened_end_time, next_frightened_start

    game_map = [list(row) for row in starting_map]
    score = 0
    game_over = False
    win = False
    frightened = False
    frightened_end_time = 0
    next_frightened_start = pygame.time.get_ticks() + FRIGHTENED_INTERVAL
    setup_ghosts()


def find_character(symbol: str) -> tuple[int, int] | None:
    """Return the row and column of the first matching map symbol."""
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == symbol:
                return row, col


def find_ghost(row: int, col: int) -> dict | None:
    """Return the ghost at a map position, if one is there."""
    for ghost in ghosts:
        if ghost["row"] == row and ghost["col"] == col:
            return ghost


def find_open_tile() -> tuple[int, int] | None:
    """Find an open tile where a ghost can safely respawn."""
    for symbol in [" ", ".", "o"]:
        position = find_character(symbol)
        if position is not None:
            return position


def is_open_for_ghost(row: int, col: int) -> bool:
    """Return True when a ghost can move onto a map tile."""
    return game_map[row][col] != "#" and game_map[row][col] != "G"


def find_next_step_toward(
    start_row: int,
    start_col: int,
    target_row: int,
    target_col: int,
) -> tuple[int, int] | None:
    """Use breadth-first search to find the next step toward a target."""
    queue = deque([(start_row, start_col, [])])
    visited = {(start_row, start_col)}

    while queue:
        row, col, path = queue.popleft()

        if row == target_row and col == target_col:
            return path[0] if path else (start_row, start_col)

        for dx, dy in DIRECTIONS:
            new_row = row + dy
            new_col = col + dx

            if (new_row, new_col) in visited:
                continue

            if game_map[new_row][new_col] == "#":
                continue

            has_ghost = game_map[new_row][new_col] == "G"
            is_target = (new_row, new_col) == (target_row, target_col)

            if has_ghost and not is_target:
                continue

            visited.add((new_row, new_col))
            queue.append((new_row, new_col, path + [(new_row, new_col)]))


def setup_screen():
    """Create the Pygame window, font, and clock."""
    global screen, font, clock

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman")
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()


def setup_ghosts():
    """Create the starting ghost list from the map and extra positions."""
    ghosts.clear()
    eaten_ghosts.clear()

    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == "G":
                ghosts.append(make_ghost(row, col, " "))

    for row, col in EXTRA_GHOST_STARTS:
        if game_map[row][col] in [".", "o", " "]:
            ghosts.append(make_ghost(row, col, game_map[row][col]))
            game_map[row][col] = "G"


def start_frightened_mode():
    """Turn ghosts blue for a limited time."""
    global frightened, frightened_end_time

    frightened = True
    frightened_end_time = pygame.time.get_ticks() + FRIGHTENED_LENGTH


def respawn_eaten_ghosts():
    """Return eaten ghosts to the board after frightened mode ends."""
    while eaten_ghosts:
        ghost = eaten_ghosts.pop()
        row = ghost["start_row"]
        col = ghost["start_col"]

        if game_map[row][col] in ["#", "P", "G"]:
            row, col = find_open_tile()

        ghost["row"] = row
        ghost["col"] = col
        ghost["under"] = game_map[row][col]
        game_map[row][col] = "G"
        ghosts.append(ghost)


def update_frightened_mode():
    """Start or stop frightened mode based on the current timer."""
    global frightened, next_frightened_start

    now = pygame.time.get_ticks()

    if frightened and now >= frightened_end_time:
        frightened = False
        respawn_eaten_ghosts()

    if not frightened and now >= next_frightened_start:
        start_frightened_mode()
        next_frightened_start = now + FRIGHTENED_INTERVAL


def count_pellets():
    """Count all uneaten pellets, including pellets under ghosts."""
    total = 0
    for row in game_map:
        total += row.count(".")
        total += row.count("o")
    for ghost in ghosts:
        if ghost["under"] in [".", "o"]:
            total += 1
    return total


def draw_game():
    """Draw the map, characters, score, messages, and replay button."""
    screen.fill(BLACK)

    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            tile = game_map[row][col]

            if tile == "#":
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif tile == ".":
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                pygame.draw.circle(screen, WHITE, center, 4)
            elif tile == "o":
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                pygame.draw.circle(screen, WHITE, center, 8)
            elif tile == "P":
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                pygame.draw.circle(screen, YELLOW, center, CELL_SIZE // 2 - 4)
            elif tile == "G":
                ghost_color = GHOST_BLUE if frightened else RED
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                pygame.draw.circle(screen, ghost_color, center, CELL_SIZE // 2 - 4)

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))

    if game_over:
        lose_text = font.render("Game Over!", True, RED)
        screen.blit(lose_text, (WIDTH // 2 - 80, HEIGHT - 82))

    if win:
        win_text = font.render("You Win!", True, YELLOW)
        screen.blit(win_text, (WIDTH // 2 - 70, HEIGHT - 82))

    if game_over or win:
        pygame.draw.rect(screen, WHITE, REPLAY_BUTTON)
        replay_text = font.render("Replay", True, BLACK)
        replay_rect = replay_text.get_rect(center=REPLAY_BUTTON.center)
        screen.blit(replay_text, replay_rect)

    pygame.display.update()


def move_pacman(dx: int, dy: int) -> None:
    """Move Pacman and update score, win state, or loss state."""
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
        if frightened:
            ghost = find_ghost(new_row, new_col)

            if ghost is None:
                return

            if ghost["under"] == ".":
                score += 10
            elif ghost["under"] == "o":
                score += 50

            score += GHOST_POINTS
            ghosts.remove(ghost)
            eaten_ghosts.append(ghost)
            game_map[row][col] = " "
            game_map[new_row][new_col] = "P"

            if count_pellets() == 0:
                win = True
            return

        game_map[row][col] = " "
        game_map[new_row][new_col] = "P"
        game_over = True
        return

    game_map[row][col] = " "
    game_map[new_row][new_col] = "P"

    if count_pellets() == 0:
        win = True


def move_ghost(ghost: dict) -> None:
    """Move one ghost toward Pacman or away during frightened mode."""
    global game_over, score

    pacman_row, pacman_col = find_character("P")
    row = ghost["row"]
    col = ghost["col"]
    possible_moves = []

    if not frightened:
        next_step = find_next_step_toward(row, col, pacman_row, pacman_col)

        if next_step is None:
            return

        new_row, new_col = next_step
        next_tile = game_map[new_row][new_col]
        game_map[row][col] = ghost["under"]

        if next_tile == "P":
            ghost["under"] = " "
            game_map[new_row][new_col] = "G"
            ghost["row"] = new_row
            ghost["col"] = new_col
            game_over = True
            return

        ghost["under"] = next_tile
        game_map[new_row][new_col] = "G"
        ghost["row"] = new_row
        ghost["col"] = new_col
        return

    for dx, dy in DIRECTIONS:
        new_row = row + dy
        new_col = col + dx
        next_tile = game_map[new_row][new_col]

        if not is_open_for_ghost(new_row, new_col):
            continue

        distance = abs(new_row - pacman_row) + abs(new_col - pacman_col)
        possible_moves.append((distance, dx, dy))

    if not possible_moves:
        return

    best_distance = max(move[0] for move in possible_moves)
    best_moves = [move for move in possible_moves if move[0] == best_distance]
    _, dx, dy = random.choice(best_moves)
    new_row = row + dy
    new_col = col + dx
    next_tile = game_map[new_row][new_col]

    game_map[row][col] = ghost["under"]

    if next_tile == "P":
        if frightened:
            score += GHOST_POINTS
            ghosts.remove(ghost)
            eaten_ghosts.append(ghost)
            return

        ghost["under"] = " "
        game_map[new_row][new_col] = "G"
        ghost["row"] = new_row
        ghost["col"] = new_col
        game_over = True
        return

    ghost["under"] = next_tile
    game_map[new_row][new_col] = "G"
    ghost["row"] = new_row
    ghost["col"] = new_col


def move_ghosts():
    """Move every active ghost once."""
    for ghost in ghosts[:]:
        if not game_over:
            move_ghost(ghost)


def main():
    """Run the Pygame event loop."""
    setup_screen()
    reset_game()
    running = True
    ghost_timer = 0

    while running:
        clock.tick(10)
        ghost_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (game_over or win) and REPLAY_BUTTON.collidepoint(event.pos):
                    reset_game()
                    ghost_timer = 0

            if event.type == pygame.KEYDOWN and not game_over and not win:
                if event.key == pygame.K_LEFT:
                    move_pacman(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_pacman(1, 0)
                elif event.key == pygame.K_UP:
                    move_pacman(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_pacman(0, 1)

        if not game_over and not win:
            update_frightened_mode()

        if ghost_timer >= GHOST_MOVE_DELAY and not game_over and not win:
            move_ghosts()
            ghost_timer = 0

        draw_game()

    pygame.quit()


if __name__ == "__main__":
    main()
