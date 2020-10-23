## Selects close NPCs/enemies (radius 800)
import base
from botapi import *

def CreateBot():
    return AutoSelectBot()

################################################################

class ClosestShipFilter(IShipFilter):
    bot = None
    def isOk(self, ship):
        return (ship.isNpc or ship.isEnemy) and ship.calcDistance(self.bot.new_map.hero.ship) < 800

FILTER_SHIP = ClosestShipFilter()

class AutoSelectBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self, 'autoSelect')
        FILTER_SHIP.bot = self
    def onBotLoopStart(self):
        print("AutoSelect loaded.");

    def onTick(self):
        if self._wait_to_select or self.new_map.hero.selectedShip is not None:
            return
        ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_SHIP);
        if ship is None:
            return
        self.selectShip(ship)
