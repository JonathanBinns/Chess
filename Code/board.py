import pygame as pg
import math

# tileClass objects are the tiles that make up the game
# the tiles are uniform squares that make up the chessboard
class tileClass:
    # the tiles are created specifically within the boardClass object,
    # so the __init__ function is simply creating placeholder attributes
    def __init__(self, size):
        self.size = size
        self.rect = None
        self.piece = None
    # for the tile object, rendering means simply being drawn
    # boardCoords allows all the tiles to be moved to the coordinates of the board together
    def render(self, window, boardCoords):
        self.rect = pg.draw.rect(window.screen, self.color, (self.x + boardCoords[0], self.y + boardCoords[1], self.size, self.size))

# the board is an object made up of an organized matrix of tileClass objects
# the board object handles complex and dynamic attributes for every tile object, which is necessary for locating pieces on the board
class boardClass:
    # the board is centered with its coords and several other attributes are set to default
    # tileGen creates all the tiles for the board and saves them to a dictionary (self.tiles)
    def __init__(self):
        self.coords = (420, 0)
        self.mouseOver = ""
        self.highlights = []
        self.occupied = []
        self.timer = 0
        self.tileGen()
    # tileGen creates tiles from two parallel lists- these are the coordinates of the board
    def tileGen(self):
        self.tiles = {}
        vert = ['1', '2', '3', '4', '5', '6', '7', '8']
        horz = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.colors = {
        "black": (0, 45, 120),
        "white": (250, 225, 215)
        }
        currentColor = "black"
        size = 135
        for letter in horz:
            for number in vert:
                tile = tileClass(size)
                tile.x = size * horz.index(letter)
                tile.y = size * 7 - size * vert.index(number)
                tile.color = self.colors[currentColor]
                tile.type = currentColor
                tile.id = letter + number
                tile.highlight = False
                self.tiles[tile.id] = tile
                if number != '8':
                    if currentColor == "white": currentColor = "black"
                    elif currentColor == "black": currentColor = "white"
    # rendering goes through the self.tiles dictionary and renders all of the tiles for the board
    # if they are in the highlighted list, they are highlighted by changing their RGB color according to a sin wave function
    # I used a sin wave to oscillate between the default color and a contrasting highlight color
    # self.mouseOver is used to determine where to move a piece when it is dropped by the player
    def render(self, window, game):
        self.timer += window.tick / 200
        for tileName in self.highlights:
            self.tiles[tileName].highlight = True
        self.mouseOver = ""
        for tileName in self.tiles:
            tile = self.tiles[tileName]
            tile.render(window, self.coords)
            mouseCoords = (window.mouse["mx"], window.mouse["my"])
            if tile.rect.collidepoint(mouseCoords):
                self.mouseOver = tile.id
            if tile.highlight:
                percent = (1 + math.sin(self.timer)) / 4
                if tile.type == "white":
                    R = (35 * percent) + (200 * (1 - percent))
                    G = (35 * percent) + (200 * (1 - percent))
                    B = (50 * percent) + (250 * (1 - percent))
                elif tile.type == "black":
                    R = (225 * percent) + (0 * (1 - percent))
                    G = (195 * percent) + (45 * (1 - percent))
                    B = (185 * percent) + (120 * (1 - percent))
                tile.color = (R, G, B)
            else:
                tile.color = self.colors[tile.type]
            tile.highlight = False
            if tileName in self.occupied:
                pieces = {**game.whitePieces, **game.blackPieces}
                for pieceName in pieces:
                    if pieces[pieceName].pos == tileName:
                        tile.piece = pieces[pieceName]
                        break