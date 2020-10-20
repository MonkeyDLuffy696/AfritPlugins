## Move randomly and collect boxes
import base
from botapi import *
import random
import time

def CreateBot():
    return BoxCollectBot()

################################################################
class ClosestBoxFilter(IBoxFilter):
    def isOk(self, box):
        return box.category == box.NORMAL or box.type == 2

FILTER_NORMAL_BOX = ClosestBoxFilter()

class BoxCollectBot(base.BotBase):
    _target_id = -1

    def __init__(self):
        base.BotBase.__init__(self, 'boxcollect')
    def onBotLoopStart(self):
        print("Box collector loaded.")

    def onTick(self):
        if self._wait_to_stop_moving:
            return

        box = GetClosestBox(self.new_map.hero.ship, self.new_map.boxes, FILTER_NORMAL_BOX);
        if box is not None:
            if self._target_id == box.uid:
                return
            self.collectBox(box)
            self._target_id = box.uid

        if not self.new_map.hero.ship.moving and not self._wait_to_start_moving:
            self.randomMove()
            self._target_id = -1
        return;
