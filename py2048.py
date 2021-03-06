import pygame
from random import randint

"""
Python implementation of the game 2048, created with pygame for the HuskyHacks3
hackathon with help from programarcadegames.com and the pygame documentation..

Created by Jason Crouse, 9/30/17
"""

# initialize constants for the tile size, buffer between tiles, and the window
# dimensions
TILE_DIMEN = 100
BUFFER = 5
WINDOW_DIMEN = (TILE_DIMEN * 4) + (5 * BUFFER)
TILE_COLOR = (255, 255, 198)
CELL_COLOR = (220,220,220)
BUFFER_COLOR = (255, 255, 255)


# ---------- Set up the classes necessary for the grid of tiles ----------

class Tile:
    """
    A Tile on the 2048 grid.
    """
    def __init__(self, x, y, value):
        """
        Initializes the Tile.

        :param x: the x-coordinate of the tile in grid coordinates, not pixels
        :param y: the y-coordinate of the tile in grid coordinates, not pixels
        :param value: the value of the Tile which will always be 2^n where n > 0
                      or None to represent an empty cell
        """
        self.value = value
        self.x = x
        self.y = y

    def draw_tile(self, surface):
        """
        Draws an individual tile.

        :param surface: the surface on which the tile will be drawn
        """
        if self.value is None:
            color = CELL_COLOR
        else:
            color = TILE_COLOR

        pygame.draw.rect(surface, color,
                         [self.x * (TILE_DIMEN + BUFFER) + BUFFER,
                          self.y * (TILE_DIMEN + BUFFER) + BUFFER,
                          TILE_DIMEN, TILE_DIMEN])

        if self.value is not None:
            font = pygame.font.SysFont("Arial", TILE_DIMEN)
            val = font.render(str(self.value), True, (0, 0, 0))
            x_val = self.x * (TILE_DIMEN + BUFFER) + BUFFER + (TILE_DIMEN / 3)
            y_val = self.y * (TILE_DIMEN + BUFFER) + BUFFER + (TILE_DIMEN / 6)
            surface.blit(val, (x_val, y_val))

    def collide_with(self, other_tile):
        """
        Handles collisions between two tiles.

        :param other_tile: Tile
        """
        # TODO
        if self.value is None:
            return
        elif other_tile.value is None:
            other_tile.value = self.value
            self.value = None
        elif self.value == other_tile.value:
            other_tile.value *= 2
            self.value = None
            global score
            score += other_tile.value
        return


class Grid:
    """
    Represents the grid of the game, in which the tiles exist and move around.
    """
    def __init__(self, cell_dimen, buffer):
        """
        Initializes the grid for the game, with the cells being squares of
        the given dimension.

        :param cell_dimen: integer
        :param buffer: integer
        """
        self.cell_dimen = cell_dimen
        self.buffer = buffer
        self.grid = []
        self.__build_grid()

    def __build_grid(self):
        """
        Initializes the grid for 2048 as a 2-dimensional array of tiles,
        which starts with two randomly placed tiles of value 2. Only allowed
        to be called when a new Grid object is created.
        """
        the_grid = []
        for row in range(4):
            a_row = []
            for column in range(4):
                a_row.append(Tile(row, column, None))
            the_grid.append(a_row)

        self.spawn_twos(2, the_grid)

        self.grid = the_grid

    def draw_grid(self, surface):
        """
        Draws all of the tiles in the grid.
        :param surface: the surface on which the grid will be drawn
        :return:
        """
        for arr in self.grid:
            for tile in arr:
                tile.draw_tile(surface)

    def spawn_twos(self, num_twos, the_grid):
        # initializes two random tiles that have value 2
        num_tiles = 0
        num_tries = 0
        while num_tiles < num_twos and num_tries < 2000:
            row = randint(0, 3)
            col = randint(0, 3)

            if the_grid[row][col].value is None:
                the_grid[row][col] = Tile(row, col, 2)
                num_tiles += 1
            num_tries += 1

        # ends the game if we get stuck in a loop while trying to spawn new
        # tiles, indicating that the board is full
        if num_tries >= 2000:
            global game_over
            game_over = True

    # TODO can these be abstracted?
    def go_down(self):
        for col in range(4):
            for row in range(3):
                this_one = self.grid[col][row]
                to_the_down = self.grid[col][row + 1]
                this_one.collide_with(to_the_down)
        self.spawn_twos(1, self.grid)

    def go_left(self):
        for row in range(4):
            for col in range(3, 0, -1):
                this_one = self.grid[col][row]
                to_the_left = self.grid[col - 1][row]
                this_one.collide_with(to_the_left)
        self.spawn_twos(1, self.grid)

    def go_right(self):
        for row in range(4):
            for col in range(3):
                this_one = self.grid[col][row]
                to_the_right = self.grid[col + 1][row]
                this_one.collide_with(to_the_right)
        self.spawn_twos(1, self.grid)

    def go_up(self):
        for col in range(4):
            for row in range(3, 0, -1):
                this_one = self.grid[col][row]
                to_the_down = self.grid[col][row - 1]
                this_one.collide_with(to_the_down)
        self.spawn_twos(1, self.grid)

# ---------- Actually runs the 2048 game! ----------

# Initialize PyGame, set window size, create the screen
pygame.init()
pygame.display.set_caption("py2048")
size = (WINDOW_DIMEN, WINDOW_DIMEN + (WINDOW_DIMEN // 8))
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
grid = Grid(TILE_DIMEN, BUFFER)
font = pygame.font.SysFont("Arial", WINDOW_DIMEN // 8)

# main game loop
score = 0
finished = False
game_over = False
while not finished:
    # ---------- handle key events or quitting ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                grid.go_left()
            elif event.key == pygame.K_RIGHT:
                grid.go_right()
            elif event.key == pygame.K_UP:
                grid.go_up()
            elif event.key == pygame.K_DOWN:
                grid.go_down()

    # ---------- draw the game ---------

    # fill the background, then draw the grid and update the surface
    screen.fill((0, 0, 0))
    grid.draw_grid(screen)

    # adds the score to the screen
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    x_val = screen.get_width() / 2 - text_rect.width / 2
    y_val = screen.get_height() - int(1.3 * text_rect.height)
    screen.blit(text, [x_val, y_val])

    # draws the game over screen if the game is over
    if game_over:
        screen.fill((255, 255, 255))
        text = font.render("Game Over. Score: " + str(score), True, (0, 0, 0))
        text_rect = text.get_rect()
        x_val = screen.get_width() / 2 - text_rect.width / 2
        y_val = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [x_val, y_val])

    pygame.display.flip()


# Close the window and quit after the game ends (the window is exited)
pygame.quit()