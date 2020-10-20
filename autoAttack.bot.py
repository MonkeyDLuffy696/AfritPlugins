## Attacks selected ships
import base
from botapi import *

def CreateBot():
    return AutoAttackBot()

################################################################

class AutoAttackBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self, 'autoAttack')
    def onBotLoopStart(self):
        print("AutoAttack loaded.")

    def onHeroTargetUpdate(self):
        # Attack any ship that your ship selected:
        if self.new_map.hero.selectedShip is not None:
            self.attackShip(self.new_map.hero.selectedShip)
