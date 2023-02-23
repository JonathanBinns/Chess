from stockfish import Stockfish
import random as r

class stockfishBox:
    def __init__(self):
        self.engine = Stockfish(path = "stockfish/stockfish_15_x64_avx2.exe")
        self.difficulty = 6 # the lower this number is, the more accurate the moves the bot makes
    def setDifficulty(self, num):
        self.difficulty = num
    def makeMove(self, game):
        moveList = self.engine.get_top_moves(self.difficulty)
        move = moveList[r.randint(1, len(moveList)) - 1]['Move']
        start = move[0:2]
        end = move[2:4]
        if end in game.board.occupied:
            game.board.tiles[end].piece.captured = True
        if self.engine.will_move_be_a_capture(move) == Stockfish.Capture.EN_PASSANT:
            game.board.tiles[end[0] + str(int(end[1]) - 1)].piece.captured = True
        if move == "e8c8" and game.board.tiles['e8'].piece.type == 'kB':
            game.board.tiles['a8'].piece.pos = 'd8'
            game.board.tiles['a8'].piece.updatePos(game)
        if move == "e8g8" and game.board.tiles['e8'].piece.type == 'kB':
            game.board.tiles['h8'].piece.pos = 'f8'
            game.board.tiles['h8'].piece.updatePos(game)
        game.board.tiles[start].piece.pos = end
        game.board.tiles[start].piece.updatePos(game)
        game.update(move)
        if move[-1] in ['q', 'r', 'b', 'h']:
            game.promote(end, move[-1])
        game.board.occupied.remove(start)
        game.turn = 'W'
