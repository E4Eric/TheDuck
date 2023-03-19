import builtins
import sys
from PyQt5 import QtWidgets
import QTPlatform, time
import AssetManager, DisplayManager,  UIEventProxy


class RuntimeContext():
    def __init__(self, appModel, parentContext):
        self.appModel = appModel
        self.parentContext = parentContext

        # common painter for all renderers
        self.painter = None

        # Start the app on first create
        if parentContext == None:
            self.app = QtWidgets.QApplication(sys.argv)
            self.window = QTPlatform.QTPlatform(self, appModel, None)
            # self.displayManager = DisplayManager.DisplayManager(self)
            # self.assetManager = AssetManager.AssetManager(self)
            self.listeners = {}
            self.meData = {}
            self.partRegistry = {}
        else:
            self.window = QTPlatform.QTPlatform(self, appModel, parentContext.window)

    def createChildContext(self, me):
        return RuntimeContext(me, self)

    def setMEData(self, me, key, value):
        if 'id' not in me:
            me['id'] = builtins.id(me)
        id = me['id']
        if id not in self.meData:
            self.meData[id] = {}
        self.meData[id][key] = value

    def getMEData(self, me, key):
        value = self.meData[me['id']][key]
        return value

    def subscribe(self, name, listener):
        self.listeners[name] = listener

    def removeListener(self, name):
        del self.listeners[name]

    def publish(self, me, attName, oldVal, newVal):
        for listenerName in self.listeners:
            listener = self.listeners[listenerName]
            listener(self, me, attName, oldVal, newVal)

    def registerPart(self, me, partName):
        if 'partName' not in me:
            return

        partName = me['partName']
        self.partRegistry[partName] = me

    def getPart(self, partName):
        if partName in self.partRegistry:
            return self.partRegistry[partName]
        return None
