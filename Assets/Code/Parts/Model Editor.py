import json

def setAppModel(appModel):
    print('set Model')

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    modelPath = me['modelPath']
    with open(modelPath, 'r') as modelData:
        appModel = json.load(modelData)

    childWindow = window.createChild(appModel)
    window.setMEData(me, 'qtWidget', childWindow)

    if 'partName' in me:
        window.registerPart(me, me['partName'])
    childWindow.show()

def setFocus(ctx, me):
    pass # print('Set Focus:', me['label'])
