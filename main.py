from Code.window import windowClass
from Code.game import gameClass

window = windowClass()
game = gameClass()
gameState = "menu"

while window.isRunning():
    window.processing()
    window.screen.fill((90, 70, 50))
