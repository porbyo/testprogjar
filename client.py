import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


class BoxesGame(ConnectionListener):
    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]

    def initGraphics(self):
        self.normallinev = pygame.image.load("normalline.png")
        self.normallineh = pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.bar_donex = pygame.image.load("xb.png")
        self.bar_doneo = pygame.image.load("ob.png")
        self.hoverlinex = pygame.image.load("x.png")
        self.hoverlineo = pygame.image.load("o.png")
        self.score_panel = pygame.image.load("score_panel.png")
        self.winningscreen = pygame.image.load("youwin.png")
        self.gameover = pygame.image.load("gameover.png")

    def Network_place(self, data):
        # get attributes
        x = data["x"]
        y = data["y"]
        num = data["num"]
        print "num:", num
        print "playernum:", self.playernum
        if num:
            self.boardo[y][x] = True
        else:
            self.boardx[y][x] = True

        if not (num == self.playernum):
            self.turn = True
        else:
            self.turn = False

    def __init__(self):

        self.boardx = [[False for x in range(3)] for y in range(3)]
        self.boardo = [[False for x in range(3)] for y in range(3)]
        self.flag = 0

        pass

        # 1
        pygame.init()
        width, height = 305, 405
        # 2
        # initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tic Tac Toe")
        # 3
        # initialize pygame clock
        self.clock = pygame.time.Clock()

        self.initGraphics()
        address = raw_input("Address of Server: ")
        try:
            if not address:
                host, port = "localhost", 8000
            else:
                host, port = address.split(":")
            self.Connect((host, int(port)))
        except:
            print "Error Connecting to Server"
            print "Usage:", "host:port"
            print "e.g.", "localhost:31425"
            exit()
        print "Boxes client started"

        self.gameid = None
        self.num = None

        self.running = False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        # determine attributes from player #
        if self.num == 0:
            self.turn = True
            self.playernum = 0
        else:
            self.turn = False
            self.playernum = 1

    def drawBoard(self):
        for x in range(3):
            for y in range(4):
                self.screen.blit(self.normallineh, [(x) * 100 + 5, (y) * 100])
        for x in range(4):
            for y in range(3):
                self.screen.blit(self.normallinev, [(x) * 100, (y) * 100 + 5])

        for x in range(3):
            for y in range(3):
                if self.boardx[y][x]:
                    self.screen.blit(self.bar_donex, [(x) * 100 + 12.5, (y) * 100 + 12.5])
        for x in range(3):
            for y in range(3):
                if self.boardo[y][x]:
                    self.screen.blit(self.bar_doneo, [(x) * 100 + 12.5, (y) * 100 + 12.5])

        self.screen.blit(self.score_panel, [0, 305])

        # create font
        myfont = pygame.font.SysFont(None, 50)

        # create text surface
        label1 = myfont.render("Your Turn", 1, (255, 255, 255))
        label2 = myfont.render("Opponent's Turn", 1, (255, 255, 255))

        # draw surface
        if self.flag == 0:
            if self.turn == True:
                self.screen.blit(label1, (70, 340))
            else:
                self.screen.blit(label2, (11, 340))

    def finished(self):
        if (self.flag == 2 and self.playernum == 0) or (self.flag == 1 and self.playernum == 1):
            self.screen.blit(self.winningscreen, (0, 0))
        else:
            self.screen.blit(self.gameover, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()

    def wincondition(self):
        fl = 1
        if self.boardo[0][0] and fl:
            if (self.boardo[0][1] and self.boardo[0][2]) or (self.boardo[1][1] and self.boardo[2][2]) or (
                self.boardo[1][0] and self.boardo[2][0]):
                self.flag = 1
                fl = 0
                self.finished()
        if self.boardo[0][1] and fl:
            if self.boardo[1][1] and self.boardo[2][1]:
                self.flag = 1
                fl = 0
                self.finished()
        if self.boardo[0][2] and fl:
            if (self.boardo[1][2] and self.boardo[2][2]) or (self.boardo[1][1] and self.boardo[2][0]):
                self.flag = 1
                fl = 0
                self.finished()
        if self.boardo[1][0] and fl:
            if self.boardo[1][1] and self.boardo[1][2]:
                self.flag = 1
                fl = 0
                self.finished()
        if self.boardo[2][0] and fl:
            if self.boardo[2][1] and self.boardo[2][2]:
                self.flag = 1
                fl = 0
                self.finished()
        if self.boardx[0][0] and fl:
            if (self.boardx[0][1] and self.boardx[0][2]) or (self.boardx[1][1] and self.boardx[2][2]) or (
                self.boardx[1][0] and self.boardx[2][0]):
                self.flag = 2
                fl = 0
                self.finished()
        if self.boardx[0][1] and fl:
            if self.boardx[1][1] and self.boardx[2][1]:
                self.flag = 2
                fl = 0
                self.finished()
        if self.boardx[0][2] and fl:
            if (self.boardx[1][2] and self.boardx[2][2]) or (self.boardx[1][1] and self.boardx[2][0]):
                self.flag = 2
                fl = 0
                self.finished()
        if self.boardx[1][0] and fl:
            if self.boardx[1][1] and self.boardx[1][2]:
                self.flag = 2
                fl = 0
                self.finished()
        if self.boardx[2][0] and fl:
            if self.boardx[2][1] and self.boardx[2][2]:
                self.flag = 2
                fl = 0
                self.finished()

    def update(self):
        connection.Pump()
        self.Pump()

        # sleep to make the game 60 fps
        self.clock.tick(60)

        # clear the screen
        self.screen.fill(0)

        self.drawBoard()

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        mouse = pygame.mouse.get_pos()

        xpos = int(math.ceil((mouse[0] - 100) / 100.0))
        ypos = int(math.ceil((mouse[1] - 100) / 100.0))

        isoutofbounds = False

        try:
            if not (self.boardx[ypos][xpos] or self.boardo[ypos][xpos]): self.screen.blit(
                self.hoverlineo if self.playernum else self.hoverlinex, [xpos * 100 + 12.5, ypos * 100 + 12.5])
        except:
            isoutofbounds = True
            pass
        if not isoutofbounds:
            alreadyplaced = self.boardx[ypos][xpos] or self.boardo[ypos][xpos]
        else:
            alreadyplaced = False

        if pygame.mouse.get_pressed()[0] and not alreadyplaced and not isoutofbounds and self.turn == True:
            self.Send({"action": "place", "x": xpos, "y": ypos, "gameid": self.gameid, "num": self.num})

        self.wincondition()
        pygame.display.flip()


bg = BoxesGame()  # __init__ is called right here
while 1:
    bg.update()
