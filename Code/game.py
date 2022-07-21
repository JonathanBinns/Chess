from Code.pieces import *
from Code.board import boardClass

class gameClass:
    def __init__(self):
        self.board = boardClass()
        self.mouseHolding = None
        self.turn = "W"
        self.reset()
    def pieceReset(self, piece, dict):
        piece.x = self.board.tiles[piece.pos].x + self.board.coords[0]
        piece.y = self.board.tiles[piece.pos].y + self.board.coords[1]
        piece.get_rect()
        dict[piece.name] = piece
    def reset(self):
        self.whitePieces = {}
        self.blackPieces = {}
        piecesList = [
        "pa",
        "pb",
        "pc",
        "pd",
        "pe",
        "pf",
        "pg",
        "ph",
        "ra",
        "hb",
        "bc",
        "qd",
        "ke",
        "bf",
        "hg",
        "rh"
        ]
        for pieceName in piecesList:
            if pieceName[0] == 'p':
                piece = pawnClass('W')
                piece.name = pieceName + '2' + 'W'
                piece.pos = pieceName[1] + '2'
                self.pieceReset(piece, self.whitePieces)
                piece = pawnClass('B')
                piece.name = pieceName + '7' + 'B'
                piece.pos = pieceName[1] + '7'
                self.pieceReset(piece, self.blackPieces)
            elif pieceName[0] == 'r':
                piece = rookClass('W')
                piece.name = pieceName + '1' + 'W'
                piece.pos = pieceName[1] + '1'
                self.pieceReset(piece, self.whitePieces)
                piece = rookClass('B')
                piece.name = pieceName + '8' + 'B'
                piece.pos = pieceName[1] + '8'
                self.pieceReset(piece, self.blackPieces)
            elif pieceName[0] == 'h':
                piece = horseClass('W')
                piece.name = pieceName + '1' + 'W'
                piece.pos = pieceName[1] + '1'
                self.pieceReset(piece, self.whitePieces)
                piece = horseClass('B')
                piece.name = pieceName + '8' + 'B'
                piece.pos = pieceName[1] + '8'
                self.pieceReset(piece, self.blackPieces)
            elif pieceName[0] == 'b':
                piece = bishopClass('W')
                piece.name = pieceName + '1' + 'W'
                piece.pos = pieceName[1] + '1'
                self.pieceReset(piece, self.whitePieces)
                piece = bishopClass('B')
                piece.name = pieceName + '8' + 'B'
                piece.pos = pieceName[1] + '8'
                self.pieceReset(piece, self.blackPieces)
            elif pieceName[0] == 'q':
                piece = queenClass('W')
                piece.name = pieceName + '1' + 'W'
                piece.pos = pieceName[1] + '1'
                self.pieceReset(piece, self.whitePieces)
                piece = queenClass('B')
                piece.name = pieceName + '8' + 'B'
                piece.pos = pieceName[1] + '8'
                self.pieceReset(piece, self.blackPieces)
            elif pieceName[0] == 'k':
                piece = kingClass('W')
                piece.name = pieceName + '1' + 'W'
                piece.pos = pieceName[1] + '1'
                self.pieceReset(piece, self.whitePieces)
                piece = kingClass('B')
                piece.name = pieceName + '8' + 'B'
                piece.pos = pieceName[1] + '8'
                self.pieceReset(piece, self.blackPieces)
    def render(self, window):
        self.board.render(window, self)
        self.board.highlights = []
        self.board.occupied = []
        pieces = {**self.whitePieces, **self.blackPieces}
        for pieceName in pieces:
            self.board.occupied.append(pieces[pieceName].pos)
            if pieces[pieceName].captured:
                if pieceName in self.whitePieces:
                    del self.whitePieces[pieceName]
                else:
                    del self.blackPieces[pieceName]
        for pieceName in pieces:
            pieces[pieceName].render(window, self)
        if self.mouseHolding != None:
            piece = pieces[self.mouseHolding]
            piece.render(window, self)
            if piece.name[3] == self.turn:
                self.board.highlights += piece.getValidSquares(self)
