from stockfish import Stockfish

class stockfishBox:
    def __init__(self):
        self.engine = Stockfish(path = "stockfish/stockfish_15_x64_avx2.exe")
        self.engine.set_skill_level(15)
        #self.move = 0
    def makeMove(self, game):
        move = self.engine.get_best_move()
        #move = ['c7c5', 'c5c4', 'c4d3'][self.move]
        #self.move += 1
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
        game.turn = 'W'
