## Simple script that moves around and collects boxes
import base 
from botapi import *
import random
import time

        # You can use the following member functions of self.acts to operate your ship:
        # self.acts.moveTo(x, y)
        # self.acts.selectShip(Ship)
        # self.acts.attackShip(Ship)
        # self.acts.reviveHero()
        # self.acts.startRepair()
        # self.acts.stopRepair()
        # self.acts.sendKeys(keys)
        # (only for SF) self.acts.doAction(string msg)
        # (only for PS) self.acts.sendNotification(string msg)
        # (only for PS) self.acts.leaveHarbour()

def CreateBot():
    return SimpleBot()

################################################################
class ClosestNpcFilter(IShipFilter):
    def isOk(self, ship):
        return ship.isNpc
class ClosestBoxFilter(IBoxFilter):
    def isOk(self, box):
        return box.category == box.NORMAL or box.type == 2

FILTER_NPC = ClosestNpcFilter()
FILTER_NORMAL_BOX = ClosestBoxFilter()

class SimpleBot(base.BotBase):
    _wait_to_start_moving = False
    _wait_to_stop_moving = False
    _target_id = -1

    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        # this opens the console window. You can comment it to avoid opening
        self.acts.allocateConsoleWindow()
        print("Simple collector bot loaded.")

    # interval tick, runs every X ms
    def onTick(self):
        # avoid spamming moveTo
        if self._wait_to_stop_moving:
            return

        box = GetClosestBox(self.new_map.hero.ship, self.new_map.boxes, FILTER_NORMAL_BOX);
        if box is not None:
            if self._target_id == box.uid:
                return
            print("Collect Box: " + box.toString())
            self.acts.collectBox(box)
            self._target_id = box.uid
            self._wait_to_start_moving = True
            self._wait_to_stop_moving = True
            return

        if not self.new_map.hero.ship.moving and not self._wait_to_start_moving and self.new_map.map.width > 100:
            x, y = random.randint(100, self.new_map.map.width - 200), random.randint(100, self.new_map.map.height - 200)
            print("Move to ", x, y)
            self.acts.moveTo(x, y)
            self._wait_to_start_moving = True
            self._target_id = -1
        return;
    def onHeroStartsMoving(self):
        # print("hero starts moving")
        self._wait_to_start_moving = False
        return
    def onHeroStopsMoving(self):
        # print("hero Stops moving")
        self._wait_to_start_moving = False
        self._wait_to_stop_moving = False
        return

    # def onWalletUpdate(self):
    #     # in Darkorbit: vipCurr is Uridium and defCurr are Credits
    #     if self.old_map.hero.wallet.defCurr != self.new_map.hero.wallet.defCurr:
    #         print("Standard currency changed to", self.new_map.hero.wallet.defCurr)
    #     if self.old_map.hero.wallet.vipCurr != self.new_map.hero.wallet.vipCurr:
    #         print("Premium currency changed to", self.new_map.hero.wallet.vipCurr)
    # def onShipListUpdate(self):
    #     print("old/new shipsList length: " + str(self.old_map.ships.size()) + "->" + str(self.new_map.ships.size()))
    #     ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_NPC);
    #     if ship is not None:
    #         print("Closest NPC: " + ship.toString() + ": ", ship.x, "|", ship.y)

