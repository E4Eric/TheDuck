import json
def createPart(ctx, part):
    print('create Part: ', part['label'])

    # Create the needed Model Elements
    tabLabel = { "style": "Part", "icon": part['icon'], "label": part['label'] }

    toolItems = []
    for action in part['toolActions']:
        toolItem = { "style": "Tool Item", "icon": action }
    toolBar = { "style": "Tool Bar", "contents": [
                  { "style": "Tool Item", "icon": "New" },
                  { "style": "Tool Item", "icon": "Save" },
                  { "style": "Tool Item", "icon": "Save All" }
                ]
              }


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
