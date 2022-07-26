from Code.pieces import *
from Code.board import boardClass
from Code.stockfishInterface import stockfishBox

class gameClass:
    def __init__(self):
        self.board = boardClass()
        self.stockfish = stockfishBox()
        self.reset()
    def pieceReset(self, piece, dict):
        piece.x = self.board.tiles[piece.pos].x + self.board.coords[0]
        piece.y = self.board.tiles[piece.pos].y + self.board.coords[1]
        piece.get_rect()
        dict[piece.name] = piece
    def update(self, move):
        self.moves.append(move)
        self.stockfish.engine.set_position(self.moves)
    def reset(self):
        self.mouseHolding = None
        self.turn = 'W'
        self.stockfish.engine.set_position([])
        self.timer = 0
        self.moves = []
        self.specialCapture = {} # used for en passant and potentially other weird captures
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
    def promote(self, position, piece = 'q'):
        name = self.board.tiles[position].piece.name # 'W' or 'B'
        if name[3] == 'W':
            if piece == 'q':
                piece = queenClass('W')
                piece.name = 'q' + position + 'W'
                piece.pos = position
                self.pieceReset(piece, self.whitePieces)
            elif piece == 'r':
                piece = rookClass('W')
                piece.name = 'r' + position + 'W'
                piece.pos = position
                self.pieceReset(piece, self.whitePieces)
            elif piece == 'b':
                piece = bishopClass('B')
                piece.name = 'b' + position + 'B'
                piece.pos = position
                self.pieceReset(piece, self.whitePieces)
            elif piece == 'h':
                piece = horseClass('W')
                piece.name = 'h' + position + 'W'
                piece.pos = position
                self.pieceReset(piece, self.whitePieces)
            del self.whitePieces[name]
        else:
            if piece == 'q':
                piece = queenClass('B')
                piece.name = 'q' + position + 'B'
                piece.pos = position
                self.pieceReset(piece, self.blackPieces)
            elif piece == 'r':
                piece = rookClass('B')
                piece.name = 'r' + position + 'B'
                piece.pos = position
                self.pieceReset(piece, self.blackPieces)
            elif piece == 'b':
                piece = bishopClass('B')
                piece.name = 'b' + position + 'B'
                piece.pos = position
                self.pieceReset(piece, self.blackPieces)
            elif piece == 'h':
                piece = horseClass('B')
                piece.name = 'h' + position + 'B'
                piece.pos = position
                self.pieceReset(piece, self.blackPieces)
            del self.blackPieces[name]
    def render(self, window):
        if self.turn == 'B':
            self.timer += window.tick
            if self.timer > 600:
                self.stockfish.makeMove(self)
        else:
            self.timer = 0
        if window.input["spaceT"]:
            self.reset()
        self.board.render(window, self)
        self.board.highlights = []
        self.board.occupied = []
        self.board.bControl = []
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
        movelist = []
        if self.turn == 'W':
            for pieceName in self.whitePieces:
                movelist += self.whitePieces[pieceName].getValidSquares(self)
            if len(movelist) == 0:
                print("Black Wins by Checkmate!")
        else:
            for pieceName in self.blackPieces:
                movelist += self.blackPieces[pieceName].getValidSquares(self)
            if len(movelist) == 0:
                print("White Wins by Checkmate!")
        if self.mouseHolding != None:
            piece = pieces[self.mouseHolding]
            piece.render(window, self)
            if piece.name[3] == self.turn and self.turn == 'W':
                self.board.highlights += piece.getValidSquares(self)
        elif len(self.moves) > 0 and self.turn == 'W':
            self.board.highlights.append(self.moves[-1][2:4])
