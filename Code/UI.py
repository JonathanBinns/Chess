import pygame as pg

class buttonClass:
    def __init__(self, name, coords, scale = 500):
        self.image = pg.transform.scale(pg.image.load("Assets/UI/" + name + ".png"), (scale, scale))
        self.imageSmall = pg.transform.scale(pg.image.load("Assets/UI/" + name + ".png"), (scale - 100, scale - 100))
        self.size = "small"
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.clicked = False
        self.scale = scale
    def get_rect(self):
        scale = self.scale
        self.rect = self.image.get_rect(topleft = (self.x - (500 - scale) / 2, self.y - (500 - scale) / 2))
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

class uiClass:
    def __init__(self):
        self.reset()
        # menu stuff
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
        # gameUI stuff
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
    def renderMenu(self, window):
        window.screen.blit(self.ChooseDifficulty, (650, 200))
        for button in self.menuButtons:
            button.render(window)
            if button.clicked:
                self.result = button.name
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
    def renderCheckmateScreen(self, window):
        self.timer += window.tick
        if self.timer > 1500:
            window.screen.blit(self.checkmate, (500, 250))
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
