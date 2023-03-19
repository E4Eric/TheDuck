import os, sys, argparse
import json

from PyQt5 import QtWidgets

import QTPlatform

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

# add ourselves to the sys path
sys.path.append(os.getcwd())

# We have a model , create the window to show it
app = QtWidgets.QApplication(sys.argv)
window = QTPlatform.QTPlatform(app, appModel, None)
# ctx = RuntimeContext(appModel, None)
window.setGeometry(100, 100, 1200, 750)
window.show()
sys.exit(app.exec_())


