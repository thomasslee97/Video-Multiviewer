from enum import Enum, unique

@unique
class Direction(Enum):
    '''Stores directions in which the Multiview can be split.

    '''

    HORIZONTAL = 0
    VERTIAL = 1

class Multiview:
    '''Stores the state of the multiview.

    Attributes:
        tiles (list): List of tiles in the multiview.
        width (int): Width of the multiview.
        height (int): Height of the multiview.

    '''

    def __init__(self, width, height):
        '''Initialises the multiview.

        '''

        self.tiles = []
        self.width = width
        self.height = height

    def add_tile(self, tile):
        '''Adds a tile to the tiles list.

        Args:
            tile (Tile): Tile to add.

        '''

        self.tiles.append(tile)

    def find_tile_at_pos(self, x, y):
        '''Returns the tile containing the position x, y

        Args:
            x (int): x position of the point.
            y (int): y position of the point.

        Returns:
            The tile at the given position.

        '''

        # Iterate over tiles.
        for i in range(0, len(self.tiles)):
            # If the point is within the tile, return the tile.
            if self.tiles[i].coord_in_tile(x, y):
                return self.tiles[i]
                
        return None

class Tile:
    '''Stores information about a tile.

    Attributes:
        width (int): Width of the tile.
        height (int): Height of the tile.
        xpos (int): Position of the tile (left edge).
        ypos (int): Position of the tile (top edge).
        pad_video (pad): Video pad.
        pad_audio (pad): Audio pad.
        video_source (VideoSource): Video Source object associated with the tile.
        uri (str): URI of the file playing on the tile.
        audio_enabled (bool): Whether to play the audio on the file.

    '''

    def __init__(self):
        self.width = None
        self.height = None
        self.xpos = None
        self.ypos = None
        self.pad_video = None
        self.pad_audio = None
        self.video_source = None
        self.uri = None
        self.audio_enabled = False
    
    def coord_in_tile(self, x, y):
        '''Returns True if x anf y are within a Tile.

        Args:
            x, y (int): The coordinate to check.

        Returns:
            True if x and y are within the Tile.

        '''

        return (x >= self.xpos) and (x <= self.xpos + self.width) and (y >= self.ypos) and (y <= self.ypos + self.height)
