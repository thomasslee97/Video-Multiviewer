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
    def __init__(self):
        self.root = Quadrant()

class Quadrant:
    def __init__(self, parent=None):
        self.children = [None, None, None, None]
        self.width = None
        self.height = None
        self.parent = parent

    def add_tile(self, position):
        pos = position.value
        if self.children[pos] == None:
            self.children[pos] = Tile(self)
            return self.children[pos]

class Tile:
    def __init__(self, parent):
        self.id = None
        self.height = None
        self.width = None
        self.parent = parent
