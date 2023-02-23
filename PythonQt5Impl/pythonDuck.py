
import sys, os, copy, json, importlib
from PyQt5 import QtGui, QtWidgets
import QTPlatform, time
import AssetManager, DisplayManager,  UIEventProxy

class RuntimeContext():
    def __init__(self, appModel):
        self.appModel = appModel
        self.window = QTPlatform.QTPlatform(self)

        # Set up the managers
        self.assetManager = AssetManager.AssetManager(self)
        self.displayManager = DisplayManager.DisplayManager(self)
        self.eventProxy = UIEventProxy.UIEventProxy(self)
        self.curController = self.assetManager.getController(self.appModel['curController'])

    def enter(self, me):
        if self.curController != None:
            if hasattr(self.curController, 'enter'):
                self.curController.enter(self, me)

    def leave(self, me):
        if self.curController != None:
            if hasattr(self.curController, 'leave'):
                self.curController.leave(self, me)
    def hover(self, me):
        if self.curController != None:
            if hasattr(self.curController, 'hover'):
                self.curController.hover(self, me)
    def mouseMove(self,me,  x, y):
        if self.curController != None:
            if hasattr(self.curController, 'mouseMove'):
                self.curController.enter(self, me, x, y)

    def lclick(self, me, x, y):
        print("lclick", x, y)

        if self.curController != None:
            if hasattr(self.curController, 'lclick'):
                self.curController.lclick(self, me, x, y)

    def rclick(self, me, x, y):
        print("rclick", x, y)

        if self.curController != None:
            if hasattr(self.curController, 'rclick'):
                self.curController.rclick(self, me, x, y)

    def layout(self, available, me):
        start = time.perf_counter()
        available = self.displayManager.layout(available, me)
        end = time.perf_counter()
        print('Layout: ', end - start)
        return available

    def drawModelElement(self, me):
        start = time.perf_counter()
        self.assetManager.drawModelElement(me)
        end = time.perf_counter()
        print('Drawt: ', end - start)

    def setState(self, me, fieldName, newVal):
        oldVal = me[fieldName]

        # detect No-ops
        if oldVal == newVal:
            return

        me[fieldName] = newVal
        ctx.publishStateChange(me, fieldName, oldVal, newVal)
    def publishStateChange(self, me, fieldName, oldVal, newVal):
        print(f'State {fieldName} changed from {oldVal} to {newVal}')

# Load the model
# Startup...get the model and load the necessary assets
# HACK! parse the path(s) from the args

# filename = sys.argv[1]
modelPath = "../Models/NewDuck.json"
with open(modelPath, 'r') as modelData:
    appModel = json.load(modelData)

# We have a model and a graphics engine, create the runtime context
app = QtWidgets.QApplication(sys.argv)
ctx = RuntimeContext(appModel)

# ...time to load the assets (NOTE: from here on *always* use the context)
ctx.window.show()
sys.exit(app.exec_())
