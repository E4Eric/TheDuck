import json

def createPart(window, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    modelPath = "../Models/EditorModel.json"
    with open(modelPath, 'r') as modelData:
        appModel = json.load(modelData)

    childWindow = window.createChild(appModel)
    me['qtWidget'] = childWindow
    childWindow.show()

def setFocus(ctx, me):
    pass # print('Set Focus:', me['label'])
