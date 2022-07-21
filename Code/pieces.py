import pygame as pg

class pieceClass:
    def __init__(self, type):
        self.size = 135
        self.image = pg.transform.scale(pg.image.load("Assets/" + type + ".PNG"), (self.size, self.size))
        self.type = type
        self.vert = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.horz = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.captured = False
    def get_rect(self):
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    def render(self, window, game):
        window.screen.blit(self.image, (self.x, self.y))
        mouseCoords = (window.mouse["mx"], window.mouse["my"])
        if self.rect.collidepoint(mouseCoords) and window.mouse["m1"] and game.mouseHolding == None:
            game.mouseHolding = self.name
        if game.mouseHolding == self.name:
            self.x = mouseCoords[0] - self.size / 2
            self.y = mouseCoords[1] - self.size / 2
            if not window.mouse["m1"]:
                game.mouseHolding = None
                if game.board.mouseOver in self.getValidSquares(game):
                    if game.board.mouseOver in game.board.occupied:
                        game.board.tiles[game.board.mouseOver].piece.captured = True
                    self.pos = game.board.mouseOver
                    self.name = self.type[0] + self.pos + self.type[1]
                self.x = game.board.tiles[self.pos].x + game.board.coords[0]
                self.y = game.board.tiles[self.pos].y + game.board.coords[1]
            self.get_rect()

class pawnClass(pieceClass):
    def __init__(self, color):
        super().__init__('p' + color)
    # generate all possible squares first, then eliminate the invalid ones
    # pawns are unique because they attack diagonally
    # pa7B
    def getValidSquares(self, game):
        valid = []
        if self.name[3] == 'W':
            valid.append(self.pos[0] + str(int(self.pos[1]) + 1))
            if self.pos[1] == '2' and not self.pos[0] + str(int(self.pos[1]) + 1) in game.board.occupied:
                valid.append(self.pos[0] + str(int(self.pos[1]) + 2))
        else:
            valid.append(self.pos[0] + str(int(self.pos[1]) - 1))
            if self.pos[1] == '7' and not self.pos[0] + str(int(self.pos[1]) - 1) in game.board.occupied:
                valid.append(self.pos[0] + str(int(self.pos[1]) - 2))
        for pos in valid:
            if pos in game.board.occupied:
                valid.remove(pos)
        diagonals = []
        if self.name[3] == 'W':
            y = str(int(self.pos[1]) + 1)
        else:
            y = str(int(self.pos[1]) - 1)
        if not self.horz.index(self.pos[0]) + 1 > 7:
            diagonals.append(self.horz[self.horz.index(self.pos[0]) + 1] + y)
        if not self.horz.index(self.pos[0]) - 1 < 0:
            diagonals.append(self.horz[self.horz.index(self.pos[0]) - 1] + y)
        for pos in diagonals:
            if pos in game.board.occupied and game.board.tiles[pos].piece.name[3] != self.name[3]:
                valid.append(pos)
        return valid

class rookClass(pieceClass):
    def __init__(self, color):
        super().__init__('r' + color)

class horseClass(pieceClass):
    def __init__(self, color):
        super().__init__('h' + color)

class bishopClass(pieceClass):
    def __init__(self, color):
        super().__init__('b' + color)

class kingClass(pieceClass):
    def __init__(self, color):
        super().__init__('k' + color)

class queenClass(pieceClass):
    def __init__(self, color):
        super().__init__('q' + color)
