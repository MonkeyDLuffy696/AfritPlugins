## Selects close NPCs/enemies (radius 800)
import base
from botapi import *

def CreateBot():
    return AutoSelectBot()

################################################################

class ClosestNpcFilter(IShipFilter):
    def isOk(self, ship):
        return ship.isNpc

FILTER_NPC = ClosestNpcFilter()

class AutoSelectBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        print("AutoSelect loaded.");

    def onShipListUpdate(self):
        ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_NPC);
        if ship is None or (not ship.isNpc and not ship.isEnemy):
            return
        if ship.calcDistance(self.new_map.hero.ship) < 800 and (self.new_map.hero.ship.target <= 0 or self.new_map.ships[GetShipByUid(self.new_map.ships, self.new_map.hero.ship.target)].calcDistance(self.new_map.hero.ship) > 600):
            print("Select: " + ship.toString(), "(", ship.x, "|", ship.y, ")")
            self.acts.selectShip(ship)
