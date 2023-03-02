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

        self.partRegistry = {}
        # We have everything we need, start it up
        self.run()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def registerPart(self, me, partName):
        if 'partName' not in me:
            return

        partName = me['partName']
        self.partRegistry[partName] = me

    def getPart(self, partName):
        if partName in self.partRegistry:
            return self.partRegistry[partName]
        return None

# Load the model
parser = argparse.ArgumentParser()
parser.add_argument('-model', '--model_name', type=str, required=False,
                    help='Name of the model to be used')
args = parser.parse_args()
modelPath = args.model_name
if modelPath == None:
    modelPath = "../Models/NewDuck.json"

with open(modelPath, 'r') as modelData:
    appModel = json.load(modelData)

# We have a model , create the runtime context
ctx = RuntimeContext(appModel)
