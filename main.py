from Code.window import windowClass
from Code.game import gameClass
from Code.UI import uiClass

window = windowClass()
game = gameClass()
UI = uiClass()
gameState = "menu"

# the main loop of the program
# what's happening on the screen is controlled by the gameState,
# which is a string that switched between "menu" and "play"
# the menu is where the bot difficulty is set
# the game is where the chess board and all the pieces are rendered and all the complex processes happen
while window.isRunning():
    window.processing()
    window.screen.fill((90, 70, 50))
    if gameState == "menu":
        UI.renderMenu(window)
        if UI.result != "" and UI.result != "quit" and UI.result in ["easy", "medium", "hard"]:
            game.reset()
            game.setDifficulty(UI.result)
            gameState = "play"
            UI.reset()
        elif UI.result == "quit":
            for key in ["left shift", "escapeT"]:
                window.input[key] = True
    elif gameState == "play":
        game.render(window, UI)
        UI.renderGameUI(window)
        if UI.result == "resignreset":
            game.reset()
            UI.reset()
        if UI.menuReturn:
            gameState = "menu"
            UI.result = ""
            UI.menuReturn = False
            game.reset()
            UI.reset()
        if game.checkmate:
            UI.renderCheckmateScreen(window)
