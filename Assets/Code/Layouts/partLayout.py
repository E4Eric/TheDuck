import copy


def layout(window, available, me):
    # take it all
    dr = copy.copy(available)

    # create the part itself
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is None:
        partModule = window.assetManager.getPart(me['partType'])
        partModule.createPart(window, me)

    widget = window.getMEData(me, 'qtWidget')
    window.setMEData(me, 'drawRect', dr)

    # place the widget 'inside' the frame
    dr = window.assetManager.adjustAvailableForStyle(me, dr)
    widget.setGeometry(dr.x, dr.y, dr.w, dr.h)

    available.w = 0
    available.h = 0
    return available
