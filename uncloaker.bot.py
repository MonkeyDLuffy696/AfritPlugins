## Uncloaks all ships around you (only for Darkorbit)
import base
from botapi import *

def CreateBot():
    return UncloakBot()

################################################################

class UncloakBot(base.BotBase):
    def __init__(self):
        base.BotBase.__init__(self, 'uncloaker')

    def onBotLoopStart(self):
        print("Uncloak script loaded.");

    def onTick(self):
        for ship in self.new_map.ships:
            if not ship.isNpc and ship.cloaked:
                print("Uncloak: " + ship.name + " (", ship.x, "|", ship.y, ")")
                self.acts.uncloakShip(ship)
