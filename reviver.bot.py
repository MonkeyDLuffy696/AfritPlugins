## Revives you upon death
import base 
from botapi import *

def CreateBot():
    return ReviverBot()

################################################################

class ReviverBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        print("Revive after death script loaded.")
    def onDeath(self):
        print("Reviving...")
        self.acts.reviveHero()
    def onHeroEntered(self):
        print("Hero ship ready.")
