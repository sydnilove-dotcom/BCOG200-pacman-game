# BCOG200 Pacman Game

For my final project, I decided to create a fun game of Pacman. My game is
based on the original Pacman game, where the player moves Pacman around a maze,
eats pellets to increase their score, and avoids ghosts.

The game also includes a few extra features. The ghosts chase Pacman, but every
10 seconds they turn blue and run away. During that time, Pacman can eat the
ghosts for extra points. After a win or loss, the player can click the replay
button to restart the game.

## How to Run the Game

If you have never run this game before, you need Python and Pygame installed
first. Can run through visual studio code afterwards (my preferred method)

### 1. Install Python

Download and install Python from https://www.python.org/downloads/.

After installing, check that Python works by opening Terminal and running:

```bash
python3 --version
```

### 2. Install Pygame

Pygame is the library this project uses to draw the game window, Pacman, ghosts,
pellets, and walls.

Install it with:

```bash
python3 -m pip install pygame
```

If you are using `uv`, you can install the project dependencies with:

```bash
uv sync
```

### 3. Run the Game

In Terminal, go to the project folder:

```bash
cd path/to/BCOG200-final-project
```

Then run:

```bash
python3 game.py
```

Use the arrow keys to move Pacman around the maze. Eat all the pellets to win,
and avoid the ghosts unless they are blue.

## How to Run Tests

Run the tests with:

```bash
python3 -m unittest discover
```

## Main Functions

1. `move_pacman`
   This function moves the Pacman character based on what the player inputs.

2. `move_ghost`
   This function moves one ghost toward Pacman or away from Pacman when the
   ghost is frightened.

3. `move_ghosts`
   This function moves all of the ghosts during the game.

4. `count_pellets`
   This function counts how many pellets are left so the game knows when the
   player wins.
