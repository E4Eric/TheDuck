import copy


def layout(ctx, available, me):
    # take it all
    me['drawRect'] = copy.copy(available)

    # create the part itself
    if 'qtWidget' not in me:
        partModule = ctx.assetManager.getPart(me['partType'])
        partModule.createPart(ctx, me)

    widget = me['qtWidget']
    dr = me['drawRect']
    widget.setGeometry(dr.x, dr.y, dr.w, dr.h)

    available.w = 0
    available.h = 0
    return available
