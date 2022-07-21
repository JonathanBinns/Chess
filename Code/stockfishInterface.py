from stockfish import Stockfish

class stockfishBox:
    def __init__(self):
        self.engine = Stockfish(path = "stockfish/stockfish_15_x64_avx2.exe")
        self.engine.set_elo_rating(1)
    def makeMove(self, game):
        move = self.engine.get_best_move()
        start = move[0:2]
        end = move[2:4]
        if end in game.board.occupied:
            game.board.tiles[end].piece.captured = True
        game.board.tiles[start].piece.pos = end
        game.board.tiles[start].piece.updatePos(game)
        game.update(move)
        game.turn = 'W'
