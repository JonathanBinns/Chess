from Code.window import windowClass
from Code.game import gameClass

window = windowClass()
game = gameClass()

while window.isRunning():
    window.processing()
    window.screen.fill((110, 130, 120))
    game.render(window)
