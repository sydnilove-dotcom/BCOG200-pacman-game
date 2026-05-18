Sales pitch:
- I am creating a simple game of pacman. The player will be playing as the character "pacman" and their goal is to eat pellets around the map to increase their score while avoiding the ghosts 
on the map that will be moving at random.

move_pacman: will move pacman around the map, for its current position: tuple[x,y], for direction string("up","down","left","right")
eat_pellets: will prompt pacman to eat the pellets once it overlaps: position: tuple[x,y], pellets will be an (x,y) list of coorinates, score will be an (int)
move_ghost: will set the randomized movement of the ghosts: for this i will use a self.move_directions function
Also will need to check if ghost has hit the pacman because that means the player loses the game I will use:
check_ghost_collision(pacman_pos, ghost_pos) for both positions i will use a tuple/list[x,y] and return True or False


People may use this game if they just want to play a simple alternate coded version of pac man and learn about some basic coding functions and different ways you can apply them

I can input a map file to create the game board instead of doing it bit by bit in the code
