import json
from RuntimeContext import RuntimeContext


def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create a tree view
    # widget = ModelEditor(ctx.window, ctx, me)
    # me['qtWidget'] = widget
    modelPath = "../Models/EditorModel.json"
    with open(modelPath, 'r') as modelData:
        appModel = json.load(modelData)
    myCTX = RuntimeContext(appModel, ctx)

    window = myCTX.window
    me['qtWidget'] = window
    window.setParent(ctx.window)
    myCTX.window.show()

def setFocus(ctx, me):
    pass # print('Set Focus:', me['label'])
