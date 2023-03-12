import pygame as pg

# pieceClass is the general class that is the parent for all piece classes
# it includes the basic functionality needed for every piece, and provides the interaction with the mouse
class pieceClass:
    # in initialization, each piece is given its basic attributes
    # the first and most important of these is the self.image attribute
    # this is a pygame surface that is
    def __init__(self, type):
        self.size = 135
        self.image = pg.transform.scale(pg.image.load("Assets/" + type + ".PNG"), (self.size, self.size))
        self.type = type
        self.color = self.type[1]
        self.vert = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.horz = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.captured = False
        self.activated = False
    def get_rect(self):
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    def updatePos(self, game):
        newName = self.type[0] + self.pos + self.type[1]
        if self.name != newName:
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
    def dropPiece(self, game):
        game.mouseHolding = None
        promotion = ''
        if game.board.mouseOver in self.getValidSquares(game) and game.turn == self.name[3] and game.turn == 'W': # this last condition limits the moveable pieces to white
            game.board.occupied.remove(self.pos)
            self.activated = True
            if self.name[0] == 'p' and game.board.mouseOver[1] == '8':
                promotion = 'q'
            game.update(self.pos + game.board.mouseOver + promotion)
            if game.turn == 'W':
                game.turn = 'B'
            else:
                game.turn = 'W'
            if game.board.mouseOver in game.board.occupied:
                game.board.tiles[game.board.mouseOver].piece.captured = True
            self.castleRule(game)
            self.pos = game.board.mouseOver
            newName = self.type[0] + self.pos + self.type[1]
            if game.specialCapture != {}:
                if newName in game.specialCapture:
                    game.board.tiles[game.specialCapture[newName]].piece.captured = True
                game.specialCapture = {}
        self.updatePos(game)
        if promotion != '':
            game.promote(game.board.mouseOver, self.name, 'q')
    def castleRule(self, game):
        if self.type[0] == 'k' and self.pos == 'e' + self.pos[1] and game.board.mouseOver == 'g' + self.pos[1]:
            game.board.tiles['h' + self.pos[1]].piece.pos = 'f' + self.pos[1]
            game.board.tiles['h' + self.pos[1]].piece.updatePos(game)
        elif self.type[0] == 'k' and self.pos == 'e' + self.pos[1] and game.board.mouseOver == 'c' + self.pos[1]:
            game.board.tiles['a' + self.pos[1]].piece.pos = 'd' + self.pos[1]
            game.board.tiles['a' + self.pos[1]].piece.updatePos(game)
    def render(self, window, game):
        window.screen.blit(self.image, (self.x, self.y))
        mouseCoords = (window.mouse["mx"], window.mouse["my"])
        if self.rect.collidepoint(mouseCoords) and window.mouse["m1"] and game.mouseHolding == None:
            game.mouseHolding = self.name
        if game.mouseHolding == self.name:
            self.x = mouseCoords[0] - self.size / 2
            self.y = mouseCoords[1] - self.size / 2
            if not window.mouse["m1"]:
                self.dropPiece(game)
            self.get_rect()
    def addEnPassantMoves(self, game, validList):
        validPlusEnPassant = validList
        enPassantMoves = []
        game.specialCapture = {}
        if int(self.pos[1]) < 8 and self.type[0] == 'p':
            if self.pos[0] != 'h':
                right = self.horz.index(self.pos[0]) + 1
                pos = self.horz[right] + '6'
                enPassantMoves.append(self.horz[right] + str(int(self.pos[1]) + 1))
                game.specialCapture[self.type[0] + pos + self.type[1]] = self.horz[right] + '5'
            if self.pos[0] != 'a':
                left = self.horz.index(self.pos[0]) - 1
                pos = self.horz[left] + '6'
                enPassantMoves.append(self.horz[left] + str(int(self.pos[1]) + 1))
                game.specialCapture[self.type[0] + pos + self.type[1]] = self.horz[left] + '5'
        return validPlusEnPassant + enPassantMoves
    def legalCheck(self, game, validList, promoteException = ''):
        engine = game.stockfish.engine
        valid = []
        # adding bug-less en passant moves
        for pos in self.addEnPassantMoves(game, validList):
            if engine.is_move_correct(self.pos + pos + promoteException):
                valid.append(pos)
        return valid

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
            if pos in game.board.occupied and game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
                valid.append(pos)
        game.specialCapture = {}  # makes en passant possible
        promotion = ''
        if self.name[3] == 'W' and self.pos[1] == '7':
            promotion = 'q'
        return self.legalCheck(game, valid, promotion)

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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return self.legalCheck(game, valid)

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
                if not pos in game.board.occupied or (game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]):
                    valid.append(pos)
        return self.legalCheck(game, valid)

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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return self.legalCheck(game, valid)

class kingClass(pieceClass):
    def __init__(self, color):
        super().__init__('k' + color)
    def getValidSquares(self, game):
        valid = []
        # kingside castle
        y = self.pos[1]
        spacesCleared = not 'f' + y in game.board.occupied and not 'g' + y in game.board.occupied and 'h' + y in game.board.occupied
        if not self.activated and spacesCleared and not game.board.tiles['h' + y].piece.activated:
            valid.append('g' + y)
        # queenside castle
        y = self.pos[1]
        spacesCleared = not 'b' + y in game.board.occupied and not 'c' + y in game.board.occupied and not 'd' + y in game.board.occupied and 'a' + y in game.board.occupied
        if not self.activated and spacesCleared and game.board.tiles['a' + y].piece != None and not game.board.tiles['a' + y].piece.activated:
            valid.append('c' + y)
        # all movements around
        for distanceSet in [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]:
            distanceA = distanceSet[0]
            distanceB = distanceSet[1]
            newIndexH = self.horz.index(self.pos[0]) + distanceA
            newIndexV = self.vert.index(self.pos[1]) + distanceB
            onBoard = newIndexH < 8 and newIndexH >= 0 and newIndexV < 8 and newIndexV >= 0
            if onBoard:
                pos = self.horz[newIndexH] + self.vert[newIndexV]
                if not pos in game.board.occupied or (game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]):
                    valid.append(pos)
        return self.legalCheck(game, valid)


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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
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
                if game.board.tiles[pos].piece != None and game.board.tiles[pos].piece.name[3] != self.name[3]:
                    valid.append(pos)
            else:
                valid.append(pos)
            distance += 1
        return self.legalCheck(game, valid)
