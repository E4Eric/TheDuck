import copy


def layout(window, available, me):
    # take it all
    dr = copy.copy(available)

    # create the part itself
    if 'qtWidget' not in me:
        partModule = window.assetManager.getPart(me['partType'])
        partModule.createPart(window, me)

    widget = me['qtWidget']
    window.setMEData(me, 'drawRect', dr)

    # place the widget 'inside' the frame
    dr = window.assetManager.adjustAvailableForStyle(me, dr)
    widget.setGeometry(dr.x, dr.y, dr.w, dr.h)

    available.w = 0
    available.h = 0
    return available
