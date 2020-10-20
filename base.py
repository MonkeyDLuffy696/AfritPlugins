import json
import random
from botapi import *

##### DO NOT CHANGE THIS FILE             #####
##### AutoUpdater overwrites all changes! #####

BOTS = []
GAME = 0 # 1=DO, 2=SF, 3=PS

def is_do():
    return GAME == 1
def is_sf():
    return GAME == 2
def is_ps():
    return GAME == 3


def SetGame(game):
    global GAME
    global BOTS
    GAME = game
    BOTS = []

def AddBot(bot):
    print("Add bot ", bot)
    BOTS.append(bot)
def SetActivators(ptr_activators):
    for bot in BOTS:
        bot.acts = CastActivatorsFromPointer(ptr_activators)
        bot.updateConfig()
        bot.onBotLoopStart()
def SetWorldData(ptr_old_map, ptr_new_map):
    fn_cast = None
    if is_do():
        fn_cast = CastDOWorldFromPointer
    elif is_sf():
        fn_cast = CastSFWorldFromPointer
    elif is_ps():
        fn_cast = CastPSWorldFromPointer
    for bot in BOTS:
        bot.old_map = fn_cast(ptr_old_map)
        bot.new_map = fn_cast(ptr_new_map)
def OnEvent(evt):
    # Everytime when an event comes through, you can see the map data before the event was recognized (self.old_map) and after the event was recognized (self.new_map)
    for bot in BOTS:
        if evt == EventType_tick:
            bot.onTick()
        elif evt == EventType_map:
            bot.onMapUpdate()
        elif evt == EventType_shipsList:
            bot.onShipListUpdate()
        elif evt == EventType_boxesList:
            bot.onBoxListUpdate()
        elif evt == EventType_heroTarget:
            bot.onHeroTargetUpdate()
        elif evt == EventType_wallet:
            bot.onWalletUpdate()
        elif evt == EventType_death:
            bot.onDeath()
        elif evt == EventType_heroEntered:
            bot.onHeroEntered()
        elif evt == EventType_heroStartsMoving:
            bot.onHeroStartsMoving()
        elif evt == EventType_heroStopsMoving:
            bot.onHeroStopsMoving()
        elif evt == EventType_heroShip:
            bot.onHeroUpdate()
        elif evt == EventType_selectShipFailed:
            bot.onSelectShipFailed()

def CreateBot():
    return BotBase("base")
class BotBase:
    old_map = None
    new_map = None
    acts = None

    _base_name = ""
    def __init__(self, base_name):
        self._base_name = base_name

    _cfg = {}
    def updateConfig(self):
        conf = "scripts/" + self._base_name + "/config.json"
        try:
            with open(conf, "r") as config_raw:
                cfg = json.load(config_raw)
            self._cfg = cfg
        except IOError:
            print("Warning: No config file found (" + conf + ")")
            return

    _wait_to_start_moving = False
    _wait_to_stop_moving = False
    def moveTo(self, p):
        self.acts.moveTo(p)
        self._wait_to_start_moving = True
        self._wait_to_stop_moving = True
    def randomMove(self):
        x, y = random.randint(100, self.new_map.map.width - 200), random.randint(100, self.new_map.map.height - 200)
        print("Randomly moving to", x, y)
        self.acts.moveTo(x, y)
        self._wait_to_start_moving = True
    def collectBox(self, box):
        print("Collect Box: " + box.toString())
        self.acts.collectBox(box)
        self._wait_to_start_moving = True
        self._wait_to_stop_moving = True

    _wait_to_select = False
    def selectShip(self, ship):
        print("Select ship: " + ship.toString())
        self.acts.selectShip(ship)
        self._wait_to_select = True
    def attackShip(self, ship):
        print("Attack ship: " + ship.toString())
        self.acts.attackShip(ship)

    def onHeroTargetUpdate(self):
        self._wait_to_select = False
    def onSelectShipFailed(self):
        self._wait_to_select = False
    def onHeroStartsMoving(self):
        self._wait_to_start_moving = False
    def onHeroStopsMoving(self):
        self._wait_to_start_moving = False
        self._wait_to_stop_moving = False

    def onTick(self):
        return
    def onHeroUpdate(self):
        return
    def onBotLoopStart(self):
        return
    def onMapUpdate(self):
        return
    def onWalletUpdate(self):
        return
    def onShipListUpdate(self):
        return
    def onBoxListUpdate(self):
        return
    def onDeath(self):
        return
    def onHeroEntered(self):
        return
