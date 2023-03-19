import copy


def layout(window, available, me):
    side = me['side']
    if 'size' in me:
        size = me['size']

    # first layout on top
    dr = copy.copy(available)

    # '-1' means take it all
    if size == -1:
        available.w = 0
        available.h = 0
    elif side == 'top':
        dr.h = size
        available.y += size
        available.h -= size

    elif side == 'bottom':
        dr.y = (available.y + available.h) - size
        dr.h = size
        available.h -= size
    elif side == 'left':
        dr.w = size
        available.x += size
        available.w -= size
    elif side == 'right':
        dr.x = (available.x + available.w) - size
        dr.w = size
        available.w -= size

    # drawRect set...layout the kids inside me
    # grab room for the style first since we layout inside us...
    kidAvailable = window.assetManager.adjustAvailableForStyle(me, dr)
    if 'contents' in me:
        for kid in me['contents']:
            kidAvailable = window.assetManager.layout(kidAvailable, kid)

    window.setMEData(me, 'drawRect', dr)

    return available
