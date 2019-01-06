from enum import Enum, unique

@unique
class Direction(Enum):
    HORIZONTAL = 0
    VERTIAL = 1

@unique
class QuadrantNames(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class Multiview:
    def __init__(self, width, height):
        tile = Tile()
        tile.width = width
        tile.height = height
        tile.xpos = 0
        tile.ypos = 0
        self.tiles = [tile]

    def add_tile(self, tile):
        self.tiles.append(tile)

    def find_tile_at_pos(self, x, y):
        for i in range(0, len(self.tiles)):
            if self.tiles[i].coord_in_tile(x, y):
                return self.tiles[i]

class Tile:
    def __init__(self):
        self.width = None
        self.height = None
        self.xpos = None
        self.ypos = None
        self.pad = None
    
    def coord_in_tile(self, x, y):
        return (x >= self.xpos) and (x <= self.xpos + self.width) and (y >= self.ypos) and (y <= self.ypos + self.height)
