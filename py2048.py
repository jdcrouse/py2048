import pygame

"""
Python implementation of the game 2048, created with pygame for the HuskyHacks3
hackathon using programarcadegames.com and the pygame documentation for help.

Created by Jason Crouse, 9/30/17
"""

# TODO LIST
# [] display tile values
# [] random setup with only two tiles of value 2, the rest empty (how to do mt?)
# [] scoring
# [] interpret keyboard input (left, right, up, down)
# [] implement game rules

# initialize constants for the tile size, buffer between tiles, and the window
# dimensions
TILE_DIMEN = 80
BUFFER = 5
WINDOW_DIMEN = (TILE_DIMEN * 4) + (5 * BUFFER)
TILE_COLOR = (220,220,220)
BUFFER_COLOR = (255, 255, 255)


# ---------- Set up the classes necessary for the grid of tiles ----------

class Tile:
    """
    A Tile on the 2048 grid.
    """
    def __init__(self, x, y, value):
        """
        Initializes the Tile
        :param x: the x-coordinate of the tile in grid coordinates, not pixels
        :param y: the y-coordinate of the tile in grid coordinates, not pixels
        :param value: the value of the Tile (will always be 2^n where n > 0)
        """
        self.value = value
        self.x = x
        self.y = y

    def draw_tile(self, surface):
        """
        Draws an individual tile.

        :param surface: the surface on which the tile will be drawn
        """
        pygame.draw.rect(surface, TILE_COLOR,
                         [self.x * (TILE_DIMEN + BUFFER) + BUFFER,
                          self.y * (TILE_DIMEN + BUFFER) + BUFFER,
                          TILE_DIMEN, TILE_DIMEN])


class Grid:
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
        # this variable is for randomizing later:
        # num_tiles = 0
        the_grid = []
        for row in range(4):
            a_row = []
            for column in range(4):
                a_row.append(Tile(row, column, 2))
            the_grid.append(a_row)
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


# ---------- Actually runs the 2048 game! ----------

# Initialize PyGame, set window size, create the screen
pygame.init()
size = (WINDOW_DIMEN, WINDOW_DIMEN)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
grid = Grid(TILE_DIMEN, BUFFER)

# main game loop
score = 0
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # fill the background, then draw the grid and update the surface
    screen.fill((0, 0, 0))
    grid.draw_grid(screen)
    pygame.display.flip()

# TODO display game over screen with score here!!!


# Close the window and quit after the game ends
pygame.quit()