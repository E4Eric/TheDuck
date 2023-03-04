import copy


def layout(ctx, available, me):
    # take it all
    dr = copy.copy(available)

    # create the part itself
    if 'qtWidget' not in me:
        partModule = ctx.assetManager.getPart(me['partType'])
        partModule.createPart(ctx, me)

    widget = me['qtWidget']
    ctx.setMEData(me, 'drawRect', dr)

    # place the widget 'inside' the frame
    dr = ctx.assetManager.adjustAvailableForStyle(me, dr)
    widget.setGeometry(dr.x, dr.y, dr.w, dr.h)

    available.w = 0
    available.h = 0
    return available
