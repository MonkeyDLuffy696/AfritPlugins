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
    GAME = game
    
    global BOTS
    BOTS = []
    return

def AddBot(bot):
    print("Add bot ", bot)
    BOTS.append(bot)
def SetActivators(ptr_activators):
    for bot in BOTS:
        bot.acts = CastActivatorsFromPointer(ptr_activators)
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
            # There are more events

def CreateBot():
    return BotBase()
class BotBase:
    old_map = None
    new_map = None
    acts = None
    def __init__(self):
        return

# You can use the following member functions of self.acts to operate your ship:
# self.acts.moveTo(x, y)
# self.acts.selectShip(Ship)
# self.acts.attackShip(Ship)
# self.acts.reviveHero()
# self.acts.startRepair()
# self.acts.stopRepair()
# self.acts.sendKeys(keys)
# (only for PS) self.acts.sendNotification(string msg)
# (only for PS) self.acts.leaveHarbour()

    def onHeroUpdate(self):
        return
    def onBotLoopStart(self):
        return
    def onTick(self):
        return
    def onMapUpdate(self):
        return
    def onWalletUpdate(self):
        return
    def onHeroTargetUpdate(self):
        return
    def onShipListUpdate(self):
        return
    def onBoxListUpdate(self):
        return
    def onDeath(self):
        return
    def onHeroEntered(self):
        return
    def onHeroStartsMoving(self):
        return
    def onHeroStopsMoving(self):
        return
