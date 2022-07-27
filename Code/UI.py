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
    def reset(self):
        self.result = ""
        ref = {
        "pawns": 8,
        "horses": 2,
        "bishops": 2,
        "rooks": 2,
        "queen": 1
        }
        self.whiteCaptured = ref
        self.blackCaptured = ref
    def renderMenu(self, window):
        window.screen.blit(self.ChooseDifficulty, (650, 200))
        for button in self.menuButtons:
            button.render(window)
            if button.clicked:
                self.result = button.name
    def renderGameUI(self, window, game):
        for button in self.resignButtons:
            button.render(window)
            if button.clicked:
                self.result = button.name

        ## add captured stuff
