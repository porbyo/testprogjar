import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data
 
class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex=0
    
class Game:
    def __init__(self, player0, currentIndex):
        self.turn = 0
        self.owner=[[False for x in range(3)] for y in range(3)]
        self.boardx = [[False for x in range(3)] for y in range(3)]
        self.boardy = [[False for x in range(3)] for y in range(3)]
        self.player0=player0
        self.player1=None
        self.gameid=currentIndex
 
    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue==None:
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
            
        else:
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame","playernum":0,"player":0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame","playernum":1,"player":1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue=None
 
print "STARTING SERVER ON LOCALHOST"
boxesServe=BoxesServer()
while True:
    boxesServe.Pump()
    sleep(0.01)
