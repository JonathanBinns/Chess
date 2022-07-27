from Code.window import windowClass
from Code.game import gameClass
from Code.UI import uiClass

window = windowClass()
game = gameClass()
UI = uiClass()
gameState = "menu"

# the main loop of the program
while window.isRunning():
    window.processing()
    window.screen.fill((90, 70, 50))
    if gameState == "menu":
        UI.renderMenu(window)
        if UI.result != "":
            game.reset()
            game.setDifficulty(UI.result)
            gameState = "play"
            UI.reset()
    elif gameState == "play":
        game.render(window, UI)
        UI.renderGameUI(window)
        if UI.result == "resignreset":
            game.reset()
            UI.reset()
        elif UI.result == "resignmenu":
            game.reset()
            gameState = "menu"
            UI.reset()
        if game.checkmate:
            UI.renderCheckmateScreen(window)
