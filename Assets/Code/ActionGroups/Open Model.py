import json


def canExecute(window, me):
    return 'lclickAction' in me

def execute(window, me):
    from PyQt5.QtWidgets import QFileDialog

    filename, _ = QFileDialog.getOpenFileName(window, "Open Model", "../Models", "Model Files (*.json);;All Files (*)")
    if filename:
        # Hack to hide the menus
        window.parent.clearLayers()

        print(f"You selected: {filename}")
        modelPath = filename
        with open(modelPath, 'r') as modelData:
            appModel = json.load(modelData)

        me = window.getPart("Model Explorer")
        modelWidget = window.getMEData(me, 'qtWidget')
        modelWidget.setEditorModel(appModel)
