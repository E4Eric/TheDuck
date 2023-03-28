import copy
import json


def canExecute(window, me):
    return 'lclickAction' in me

# Define a function to remove the id fields recursively
def remove_id_fields(model):
    if isinstance(model, dict):
        # Remove the id field if it exists
        if "id" in model:
            print(f'deleting id[{model["id"]}]')
            del model["id"]
        # Recursively remove the id fields from any nested objects
        for key in model:
            remove_id_fields(model[key])
    elif isinstance(model, list):
        # Recursively remove the id fields from any objects in the list
        for item in model:
            remove_id_fields(item)

    return model

def execute(window, me):
    from PyQt5.QtWidgets import QFileDialog

    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(window, 'Save As...', 'myModel.json', 'JSON Files (*.json)',
                                              options=options)
    if fileName:
        print('Selected file name:', fileName)
        modelPath = fileName
        with open(modelPath, 'w') as modelFile:
            # Remove the generated ids
            correctedModel = copy.deepcopy(window.parent.appModel)
            remove_id_fields(correctedModel)
            formattedJson = json.dumps(correctedModel, indent=2)
            print(formattedJson)
            modelFile.write(formattedJson)
