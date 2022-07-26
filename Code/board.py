import pygame as pg
import math

class tileClass:
    def __init__(self, size):
        self.size = size
        self.rect = None
        self.piece = None
    def render(self, window, boardCoords):
        self.rect = pg.draw.rect(window.screen, self.color, (self.x + boardCoords[0], self.y + boardCoords[1], self.size, self.size))

class boardClass:
    def __init__(self):
        self.coords = (420, 0)
        self.mouseOver = ""
        self.highlights = []
        self.occupied = []
        self.timer = 0
        self.tileGen()
    def tileGen(self):
        self.tiles = {}
        vert = ['1', '2', '3', '4', '5', '6', '7', '8']
        horz = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.colors = {
        "black": (45, 20, 0),
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
                    R = (65 * percent) + (250 * (1 - percent))
                    G = (35 * percent) + (225 * (1 - percent))
                    B = (20 * percent) + (215 * (1 - percent))
                else:
                    R = (225 * percent) + (45 * (1 - percent))
                    G = (195 * percent) + (20 * (1 - percent))
                    B = (185 * percent) + (0 * (1 - percent))
                tile.color = (R, G, B)
            else:
                tile.color = self.colors[tile.type]
            tile.highlight = False
            if tileName in self.occupied:
                piece = None
                pieces = {**game.whitePieces, **game.blackPieces}
                for pieceName in pieces:
                    if pieces[pieceName].pos == tileName:
                        tile.piece = pieces[pieceName]
                        break
