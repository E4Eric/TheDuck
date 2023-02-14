
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
modelPath = "../Models/BabyDuck.json"
with open(modelPath, 'r') as modelData:
    appModel = json.load(modelData)

# We have a model and a graphics engine, create the runtime context
app = QtWidgets.QApplication(sys.argv)
ctx = RuntimeContext(appModel)

# ...time to load the assets (NOTE: from here on *always* use the context)
ctx.window.show()
sys.exit(app.exec_())
