import pygame as pg

# the buttons are simple: they return a value when clicked
# they contain two surface objects: self.image and self.imageSmall
# the image appears small unless the mouse is hovering over it, which helps indicate interactability to the user
# having buttons of multiple sizes became complicated, so it was necessary to add a scale value to change the overall scale of both images
# scale needed to be factored into screen blitting, since screen blitting is based on the topleft of the image
class buttonClass:
    # buttons are created as attributes for the uiClass
    # they are given some initial values that determine what image the button gets, where the button goes, and how big the button is
    # it also sets the self.clicked boolean to False
    def __init__(self, name, coords, scale = 500):
        self.image = pg.transform.scale(pg.image.load("Assets/UI/" + name + ".png"), (scale, scale))
        self.imageSmall = pg.transform.scale(pg.image.load("Assets/UI/" + name + ".png"), (scale - 100, scale - 100))
        self.size = "small"
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.clicked = False
        self.scale = scale
    # get_rect is a simple function, it sets the self.rect attribute to the correct place for collision purposes
    # I needed to implement the scale variable to account for differently sized buttons
    def get_rect(self):
        scale = self.scale
        self.rect = self.image.get_rect(topleft = (self.x - (500 - scale) / 2, self.y - (500 - scale) / 2))
    # render handles the drawing of and functionality of the button
    # when clicked, the button's .clicked value is set to True and the information can be interpreted appropriately at higher levels
    def render(self, window):
        scale = self.scale
        if self.size == "small":
            window.screen.blit(self.imageSmall, (self.x + 50 - (500 - scale) / 2, self.y + 50 - (500 - scale) / 2))
        else:
            window.screen.blit(self.image, (self.x - (500 - scale) / 2, self.y - (500 - scale) / 2))
        self.get_rect()
        mouseOver = self.rect.collidepoint(window.mouse['mx'], window.mouse['my'])
        self.clicked = False
        if mouseOver:
            self.size = "big"
            if window.mouse['m1']:
                self.clicked = True
        else:
            self.size = "small"

# the UI object is responsible for all the buttons as well as the display of pieces captured during the game
# the self.result value is essential for switching the gameState in the main loop
class uiClass:
    # because the UI object is responsible for rendering the initial difficulty selection menu as well as
    # the buttons and piece capture display in the game screen, I seperated the init into two sections.
    # in these two sections, the different assets are saved and preloaded to be used later in the loop
    def __init__(self):
        self.reset()
        # menu attributes
        self.ChooseDifficulty = pg.image.load("Assets/UI/ChooseBotDifficulty.png")
        menuButtonDict = {
        "easy": (110, 400),
        "medium": (710, 400),
        "hard": (1310, 400)
        }
        self.menuButtons = []
        for name in menuButtonDict:
            button = buttonClass(name, menuButtonDict[name])
            self.menuButtons.append(button)
        button = buttonClass("quit", (150, 150), 250)
        self.menuButtons.append(button)
        # gameUI attributes
        self.checkmate = pg.image.load("Assets/UI/checkmate.png")
        resignButtonDict = {
        "resignmenu": {
        "pos": (1650, 780),
        "scale": 300
        },
        "resignreset": {
        "pos": (1650, 300),
        "scale": 300
        }
        }
        self.resignButtons = []
        for name in resignButtonDict:
            button = buttonClass(name, resignButtonDict[name]["pos"], resignButtonDict[name]["scale"])
            self.resignButtons.append(button)
        self.pieces = {}
        for name in ['pW', 'pB', 'hW', 'hB', 'bW', 'bB', 'rW', 'rB', 'qW', 'qB']:
            self.pieces[name] = pg.transform.scale(pg.image.load("Assets/" + name + ".PNG"), (60, 60))
    # resetting is called to initialize the object and then to put it back to a default state after that
    # the two captured dictionaries keep track of how many pieces were captured by both players
    def reset(self):
        self.result = ""
        self.timer = 0
        ref = {}
        self.whiteCaptured = {
        "pawns": 0,
        "horses": 0,
        "bishops": 0,
        "rooks": 0,
        "queens": 0
        }
        self.blackCaptured = {
        "pawns": 0,
        "horses": 0,
        "bishops": 0,
        "rooks": 0,
        "queens": 0
        }
    # renderMenu simply draws the assets for the main menu to the screen in the location that was specified and saved during initialization
    # the menu consists of four buttons: the three difficulty buttons and then the quit button
    def renderMenu(self, window):
        window.screen.blit(self.ChooseDifficulty, (650, 200))
        for button in self.menuButtons:
            button.render(window)
            if button.clicked:
                self.result = button.name
    # pieceRow renders the smaller icon of the pieces captured to the left side of the screen
    # pieceRow is used as a part of renderGameUI
    def pieceRow(self, window, pieceName, pieceNum, xDelta, yDelta = 0):
        image = self.pieces[pieceName]
        iteration = pieceNum
        yDeltaReturn = 0
        start = 1060
        if pieceName[1] == 'W':
            start = -38
            iteration *= -1
            yDelta *= -1
        while iteration != 0:
            window.screen.blit(image, (350 - xDelta, start - (58 * iteration) - yDelta))
            yDeltaReturn += 58
            iteration -= 1
            if pieceName[1] == 'W':
                iteration += 2
        return yDeltaReturn
    # there are two buttons to render during the game:
    # one of them resigns and resets the game, the other resigns and returns the player to the menu
    # on the left side, any captured pieces are displayed for both players
    # xDelta is used to space out the pieces horizontally in an even way
    # pieceRow handles the vertical spacing for the pieces
    def renderGameUI(self, window):
        for button in self.resignButtons:
            button.render(window)
            if button.clicked:
                self.result = button.name
        xDelta = 0
        if self.whiteCaptured["pawns"] > 0:
            self.pieceRow(window, 'pB', self.whiteCaptured["pawns"], xDelta)
            xDelta += 58
        if self.whiteCaptured["horses"] > 0 or self.whiteCaptured["bishops"] > 0:
            yDelta = self.pieceRow(window, 'bB', self.whiteCaptured["bishops"], xDelta)
            self.pieceRow(window, 'hB', self.whiteCaptured["horses"], xDelta, yDelta)
            xDelta += 58
        if self.whiteCaptured["rooks"] > 0:
            self.pieceRow(window, 'rB', self.whiteCaptured["rooks"], xDelta)
            xDelta += 58
        if self.whiteCaptured["queens"] > 0:
            self.pieceRow(window, 'qB', self.whiteCaptured["queens"], xDelta)
        xDelta = 0
        if self.blackCaptured["pawns"] > 0:
            self.pieceRow(window, 'pW', self.blackCaptured["pawns"], xDelta)
            xDelta += 58
        if self.blackCaptured["horses"] > 0 or self.blackCaptured["bishops"] > 0:
            yDelta = self.pieceRow(window, 'bW', self.blackCaptured["bishops"], xDelta)
            self.pieceRow(window, 'hW', self.blackCaptured["horses"], xDelta, yDelta)
            xDelta += 58
        if self.blackCaptured["rooks"] > 0:
            self.pieceRow(window, 'rW', self.blackCaptured["rooks"], xDelta)
            xDelta += 58
        if self.blackCaptured["queens"] > 0:
            self.pieceRow(window, 'qW', self.blackCaptured["queens"], xDelta)
    # renderCheckmateScreen is a simple function, it just draws the image that informs the player the game is over
    # the timer is there to add a short time buffer between the last move being made and the checkmate screen being drawn
    def renderCheckmateScreen(self, window):
        self.timer += window.tick
        if self.timer > 1500:
            window.screen.blit(self.checkmate, (500, 250))
