import pygame as pg

class pieceClass:
    def __init__(self, type):
        self.size = 135
        self.image = pg.transform.scale(pg.image.load("Assets/" + type + ".PNG"), (self.size, self.size))
        self.type = type
        self.vert = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.horz = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.captured = False
        self.activated = False
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
                if game.board.mouseOver in self.getValidSquares(game) and game.turn == self.name[3]:
                    self.activated = True
                    if game.turn == 'W':
                        game.turn = 'B'
                    else:
                        game.turn = 'W'
                    if game.board.mouseOver in game.board.occupied:
                        game.board.tiles[game.board.mouseOver].piece.captured = True
                    self.pos = game.board.mouseOver
                    newName = self.type[0] + self.pos + self.type[1]
                    if self.type[1] == 'W':
                        game.whitePieces[newName] = game.whitePieces[self.name]
                        del game.whitePieces[self.name]
                    else:
                        game.blackPieces[newName] = game.blackPieces[self.name]
                        del game.blackPieces[self.name]
                    self.name = newName
                self.x = game.board.tiles[self.pos].x + game.board.coords[0]
                self.y = game.board.tiles[self.pos].y + game.board.coords[1]
            self.get_rect()

class pawnClass(pieceClass):
    def __init__(self, color):
        super().__init__('p' + color)
    # generate all possible squares first, then eliminate the invalid ones
    # pawns are unique because they attack diagonally
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
        if self.horz.index(self.pos[0]) + 1 < 8:
            diagonals.append(self.horz[self.horz.index(self.pos[0]) + 1] + y)
        if self.horz.index(self.pos[0]) - 1 >= 0:
            diagonals.append(self.horz[self.horz.index(self.pos[0]) - 1] + y)
        for pos in diagonals:
            if pos in game.board.occupied and game.board.tiles[pos].piece.name[3] != self.name[3]:
                valid.append(pos)
        return valid

class rookClass(pieceClass):
    def __init__(self, color):
        super().__init__('r' + color)
    def getValidSquares(self, game):
        valid = []
        # up
        condition = False
        distance = 1
        while not condition:
            newIndex = self.vert.index(self.pos[1]) + distance
            if newIndex < 8:
                pos = self.pos[0] + self.vert[newIndex]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # right
        condition = False
        distance = 1
        while not condition:
            newIndex = self.horz.index(self.pos[0]) + distance
            if newIndex < 8:
                pos = self.horz[newIndex] + self.pos[1]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # down
        condition = False
        distance = 1
        while not condition:
            newIndex = self.vert.index(self.pos[1]) - distance
            if newIndex >= 0:
                pos = self.pos[0] + self.vert[newIndex]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # left
        condition = False
        distance = 1
        while not condition:
            newIndex = self.horz.index(self.pos[0]) - distance
            if newIndex >= 0:
                pos = self.horz[newIndex] + self.pos[1]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return valid

class horseClass(pieceClass):
    def __init__(self, color):
        super().__init__('h' + color)
    def getValidSquares(self, game):
        valid = []
        for distanceSet in [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]:
            distanceA = distanceSet[0]
            distanceB = distanceSet[1]
            newIndexH = self.horz.index(self.pos[0]) + distanceA
            newIndexV = self.vert.index(self.pos[1]) + distanceB
            onBoard = newIndexH < 8 and newIndexH >= 0 and newIndexV < 8 and newIndexV >= 0
            if onBoard:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
                if not pos in game.board.occupied or game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
        return valid

class bishopClass(pieceClass):
    def __init__(self, color):
        super().__init__('b' + color)
    def getValidSquares(self, game):
        valid = []
        # upright
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) + distance
            newIndexV = self.vert.index(self.pos[1]) + distance
            if newIndexH < 8 and newIndexV < 8:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # downright
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) + distance
            newIndexV = self.vert.index(self.pos[1]) - distance
            if newIndexH < 8 and newIndexV >= 0:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # downleft
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) - distance
            newIndexV = self.vert.index(self.pos[1]) - distance
            if newIndexH >= 0 and newIndexV >= 0:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # upleft
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) - distance
            newIndexV = self.vert.index(self.pos[1]) + distance
            if newIndexH >= 0 and newIndexV < 8:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return valid

class kingClass(pieceClass):
    def __init__(self, color):
        super().__init__('k' + color)
    def getValidSquares(self, game):
        valid = []
        # kingside castle
        if not self.activated and not 'f1' in game.board.occupied and not 'g1' in game.board.occupied and 'h1' in game.board.occupied and not game.board.tiles['h1'].piece.activated:
            valid.append('g1')
        return valid

class queenClass(pieceClass):
    def __init__(self, color):
        super().__init__('q' + color)
    def getValidSquares(self, game):
        valid = []
        # upright
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) + distance
            newIndexV = self.vert.index(self.pos[1]) + distance
            if newIndexH < 8 and newIndexV < 8:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # downright
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) + distance
            newIndexV = self.vert.index(self.pos[1]) - distance
            if newIndexH < 8 and newIndexV >= 0:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # downleft
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) - distance
            newIndexV = self.vert.index(self.pos[1]) - distance
            if newIndexH >= 0 and newIndexV >= 0:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # upleft
        condition = False
        distance = 1
        while not condition:
            newIndexH = self.horz.index(self.pos[0]) - distance
            newIndexV = self.vert.index(self.pos[1]) + distance
            if newIndexH >= 0 and newIndexV < 8:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # up
        condition = False
        distance = 1
        while not condition:
            newIndex = self.vert.index(self.pos[1]) + distance
            if newIndex < 8:
                pos = self.pos[0] + self.vert[newIndex]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # right
        condition = False
        distance = 1
        while not condition:
            newIndex = self.horz.index(self.pos[0]) + distance
            if newIndex < 8:
                pos = self.horz[newIndex] + self.pos[1]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # down
        condition = False
        distance = 1
        while not condition:
            newIndex = self.vert.index(self.pos[1]) - distance
            if newIndex >= 0:
                pos = self.pos[0] + self.vert[newIndex]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        # left
        condition = False
        distance = 1
        while not condition:
            newIndex = self.horz.index(self.pos[0]) - distance
            if newIndex >= 0:
                pos = self.horz[newIndex] + self.pos[1]
            else:
                break
            if pos in game.board.occupied:
                condition = True
                if game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return valid
