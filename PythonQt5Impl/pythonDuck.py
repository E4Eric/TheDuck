import argparse
import json
import os
import sys

from RuntimeContext import RuntimeContext

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

# We have a model , create the runtime context
ctx = RuntimeContext(appModel, None)
ctx.window.setGeometry(100, 100, 1200, 750)
ctx.window.show()
sys.exit(ctx.app.exec_())


