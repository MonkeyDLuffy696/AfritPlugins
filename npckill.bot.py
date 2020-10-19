## Simple script that moves around and kills NPCs
import base 
from botapi import *
import random
import time

def CreateBot():
    return NpcKillBot()

################################################################
class ClosestNpcFilter(IShipFilter):
    def isOk(self, ship):
        return ship.isNpc

FILTER_NPC = ClosestNpcFilter()

class NpcKillBot(base.BotBase):
    _wait_to_start_moving = False
    _wait_to_stop_moving = False
    _wait_to_select = False
    _target_id = -1

    def __init__(self):
        base.BotBase.__init__(self)

    def onBotLoopStart(self):
        # this opens the console window. You can comment it to avoid opening
        self.acts.allocateConsoleWindow()
        print("Simple NPC killer loaded.")

    def random_move(self):
        x, y = random.randint(100, self.new_map.map.width - 200), random.randint(100, self.new_map.map.height - 200)
        print("Randomly moving to", x, y)
        self.acts.moveTo(x, y)
        self._wait_to_start_moving = True

    def move_to(self, p):
        self.acts.moveTo(p)
        self._wait_to_start_moving = True
        self._wait_to_stop_moving = True

    # interval tick, runs every X ms
    def onTick(self):

        if self._target_id > 0:
            ship = GetShipByUid(self.new_map.ships, self._target_id);
            if (ship is None):
                self._target_id = -1
                print("Target gone.")
                self._wait_to_stop_moving = False # to allow the bot to move quickly elsewhere
                return
            if self.new_map.hero.ship.calcDistance(ship) > 500:
                if not self._wait_to_stop_moving:
                    print("Move into proximity of target.")
                    self.move_to(ship.randomPosInRadius(50))
            elif self.new_map.hero.selectedTarget != ship.uid and not self._wait_to_select:
                print("Select ship: " + ship.toString())
                self.acts.selectShip(ship)
                self._wait_to_select = True
            return

        if self._wait_to_stop_moving:
            return

        # print("atttarget:",self.new_map.hero.ship.target)

        ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_NPC);
        if ship is not None:
            self._target_id = ship.uid
            if self.new_map.hero.ship.calcDistance(ship) > 800:
                self.move_to(ship.randomPosInRadius(50))
            else:
                print("Choose ship: " + ship.toString())
                self.acts.selectShip(ship)
                self._wait_to_select = True

        if not self.new_map.hero.ship.moving and not self._wait_to_start_moving and self.new_map.map.width > 100:
            self.random_move()
        return;
    def onHeroTargetUpdate(self):
        self._wait_to_select = False
        print("selected:", self.old_map.hero.selectedTarget, " to ", self.new_map.hero.selectedTarget)
        if self.new_map.hero.selectedTarget > 0: # and self.hero().selectedTarget == self._target_id:
            # Attack any ship that your ship selected:
            ship = GetShipByUid(self.new_map.ships, self.new_map.hero.selectedTarget);
            if (ship is None):
                return
            print("Attack " + ship.toString())
            self.acts.attackShip(ship)
            self._attacking_since = time.perf_counter()
    def onHeroStartsMoving(self):
        # print("hero starts moving")
        self._wait_to_start_moving = False
        self._reset_delay = time.perf_counter()
        return
    def onHeroStopsMoving(self):
        # print("hero Stops moving")
        self._wait_to_start_moving = False
        self._wait_to_stop_moving = False
        return
