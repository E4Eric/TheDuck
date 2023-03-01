import argparse
import sys, os, copy, json, importlib
from PyQt5 import QtGui, QtWidgets
import QTPlatform, time
import AssetManager, DisplayManager,  UIEventProxy

class RuntimeContext():
    def __init__(self, appModel):
        self.appModel = appModel
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QTPlatform.QTPlatform(self)

        # Set up the managers
        self.assetManager = AssetManager.AssetManager(self)
        self.displayManager = DisplayManager.DisplayManager(self)
        self.curController = self.assetManager.getController(self.appModel['curController'])
        self.eventProxy = UIEventProxy.UIEventProxy(self, self.curController)

        # We have everything we need, start it up
        self.run()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

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
parser = argparse.ArgumentParser()
parser.add_argument('-model', '--model_name', type=str, required=True,
                    help='Name of the model to be used')
args = parser.parse_args()

modelPath = args.model_name
print(f"The model name is {modelPath}")
# modelPath = "../Models/NewDuck.json"
with open(modelPath, 'r') as modelData:
    appModel = json.load(modelData)

# We have a model , create the runtime context
ctx = RuntimeContext(appModel)
