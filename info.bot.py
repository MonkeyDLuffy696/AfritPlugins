## Prints map information
import base
from botapi import *
import time

def CreateBot():
    return InfoBot()

################################################################

class ClosestEnemyFilter(IShipFilter):
    def isOk(self, ship):
        return ship.isEnemy
FILTER_ENEMIES = ClosestEnemyFilter()

class InfoBot(base.BotBase):
    _init_time = time.perf_counter()
    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        # this opens the console window. You can comment it to avoid opening
        self.acts.allocateConsoleWindow()
        print("Info printer loaded.")

    def onHeroUpdate(self):
        if self._init_time < time.perf_counter() - 5:
            self._init_time = time.perf_counter()
            self.onMapUpdate()
            print("Hero ship:", self.new_map.hero.ship.serialize())
            if base.is_do():
                print(" Portals:", self.new_map.portals.size(),
                "; in NAZ:", self.new_map.inNaz,
                      "; Cargo load:", self.new_map.cargo.getPercentage(), "%",
                "; PET HP:", self.new_map.pet.hp.curr);
    def onHeroEntered(self):
        print("Hero ship ready.")
    def onDeath(self):
        print("Hero ship destroyed.")
    def onMapUpdate(self):
        print("Map:", self.new_map.map.name, "size:", self.new_map.map.width, self.new_map.map.height)
    def onHeroStartsMoving(self):
        wprint("Hero ship starts moving.")
    def onHeroStopsMoving(self):
        wprint("Hero ship stops moving.")
    def onWalletUpdate(self):
        # in Darkorbit: vipCurr is Uridium and defCurr are Credits
        if self.old_map.hero.wallet.defCurr != self.new_map.hero.wallet.defCurr:
            print("Standard currency changed to", self.new_map.hero.wallet.defCurr)
        if self.old_map.hero.wallet.vipCurr != self.new_map.hero.wallet.vipCurr:
            print("Premium currency changed to", self.new_map.hero.wallet.vipCurr)
    def onShipListUpdate(self):
        # print("old/new shipsList length: " + str(self.old_map.ships.size()) + "->" + str(self.new_map.ships.size()))
        ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships);
        if ship is not None:
            print("Closest Ship: " + ship.serialize())
            ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_ENEMIES);
            if ship is not None:
                wprint("Closest Enemy: " + ship.serialize())
    def onBoxListUpdate(self):
        # print("old/new boxesList length: " + str(self.old_map.boxes.size()) + "->" + str(self.new_map.boxes.size()))
        box = GetClosestBox(self.new_map.hero.ship, self.new_map.boxes);
        if box is not None:
            print("Closest Box: " + box.toString(), box.category, box.type)
