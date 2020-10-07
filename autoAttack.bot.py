## Attacks selected/locked targets
import base 
from botapi import *

def CreateBot():
    return AutoAttackBot()

################################################################

class AutoAttackBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        print("AutoAttack loaded.")
    def onHeroTargetUpdate(self):
        print("Hero target changed from " + str(self.old_map.hero.target) + " to " + str(self.new_map.hero.target))
        if self.new_map.hero.target != 0:
            # Attack any ship that your ship selected:
            ship_idx = GetShipByUid(self.new_map.ships, self.new_map.hero.target);
            if (ship_idx < 0):
                return
            ship = self.new_map.ships[ship_idx]
            print("Attack " + ship.serialize())
            self.acts.attackShip(ship)
