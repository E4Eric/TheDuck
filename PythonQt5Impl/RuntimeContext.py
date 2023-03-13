import builtins
import sys
from PyQt5 import QtWidgets
import QTPlatform, time
import AssetManager, DisplayManager,  UIEventProxy


class RuntimeContext():
    def __init__(self, appModel, parentContext):
        self.appModel = appModel
        self.parentContext = parentContext
        if parentContext == None:
            self.app = QtWidgets.QApplication(sys.argv)

        self.window = QTPlatform.QTPlatform(self, appModel, None)

        # Set up the managers
        self.assetManager = AssetManager.AssetManager(self)
        self.displayManager = DisplayManager.DisplayManager(self)

        self.listeners = {}
        self.curController = self.setController(self.appModel['curController'])
        self.eventProxy = UIEventProxy.UIEventProxy(self, self.curController)

        # Share the runtime data caches
        if parentContext == None:
            self.meData = {}
            self.partRegistry = {}
        else:
            self.meData = parentContext.meData
            self.partRegistry = parentContext.partRegistry

    def setController(self, controllerName):
        module = self.assetManager.getController(controllerName)
        controller = module.createController(self)
        return controller

    def setMEData(self, me, key, value):
        if 'id' not in me:
            me['id'] = builtins.id(me)
        id = me['id']
        if id not in self.meData:
            self.meData[id] = {}
        meData = self.meData[id][key] = value

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
