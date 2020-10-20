## Moves around and kills NPCs
import random
import time
import base
from botapi import *

def CreateBot():
    return NpcKillBot()

################################################################
class ClosestNpcFilter(IShipFilter):
    npc_list = []
    def isOk(self, ship):
        return ship.isNpc and (ship.name in map(lambda x: x['name'], self.npc_list) or len(self.npc_list) == 0)

FILTER_NPC = ClosestNpcFilter()

class NpcKillBot(base.BotBase):
    _target_id = -1
    _current_ammo = 0
    _current_range = 600

    def __init__(self):
        base.BotBase.__init__(self, 'npckill')

    def selectShip(self, ship):
        if 'npcList' in self._cfg:
            want_ammo, want_range = next((x['ammo'], x['range']) for x in self._cfg['npcList'] if x['name'] == ship.name)
            if want_ammo > 0:
                print("Switching ammo to", want_ammo,"and range to", want_range)
                self.acts.sendKeys(str(want_ammo))
                self._current_ammo = want_ammo
                if want_range > 0:
                    self._current_range = want_range
        base.BotBase.selectShip(self, ship)

    def onBotLoopStart(self):
        if 'npcList' in self._cfg:
            FILTER_NPC.npc_list = self._cfg['npcList']
        print("Simple NPC killer loaded.")

    def onTick(self):
        if self._target_id > 0:
            ship = GetShipByUid(self.new_map.ships, self._target_id);
            if (ship is None):
                self._target_id = -1
                self._wait_to_stop_moving = False # to allow the bot to move quickly elsewhere
                print("Target gone.")
                return
            if self.new_map.hero.ship.calcDistance(ship) > self._current_range:
                if not self._wait_to_stop_moving:
                    print("Move into proximity of target.")
                    self.moveTo(ship.randomPosInRadius(50))
            elif self.new_map.hero.selectedTarget != ship.uid and not self._wait_to_select:
                self.selectShip(ship)
            return

        ship = GetClosestShip(self.new_map.hero.ship, self.new_map.ships, FILTER_NPC);
        if ship is not None:
            self._target_id = ship.uid
            if self.new_map.hero.ship.calcDistance(ship) > 800:
                self.moveTo(ship.randomPosInRadius(50))
            else:
                self.selectShip(ship)

        if not self.new_map.hero.ship.moving and not (self._wait_to_start_moving or self._wait_to_stop_moving) and self.new_map.map.width > 100:
            self.randomMove()
        return;
    def onHeroTargetUpdate(self):
        base.BotBase.onHeroTargetUpdate(self)
        print("Selected:", self.old_map.hero.selectedTarget, " to ", self.new_map.hero.selectedTarget)
        if self.new_map.hero.selectedShip is not None:
            print("Attack " + self.new_map.hero.selectedShip.toString())
            self.attackShip(self.new_map.hero.selectedShip)
