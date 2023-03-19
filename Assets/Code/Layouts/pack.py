import copy

def hpack(window, available, me):
    dr = copy.copy(available)

    totalWidth = 0
    maxHeight = 0

    # reserve space now to get positioning correct
    kidAvailable = window.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        kidAvailable = window.assetManager.layout(kidAvailable, kid)
        kr = window.getMEData(kid, 'drawRect')
        totalWidth += kr.w
        maxHeight = max(maxHeight, kr.h)

    # Pass 2: Set the width o the kids to the mas width found
    for kid in me['contents']:
        window.getMEData(kid, 'drawRect').h = maxHeight

    dr.w = totalWidth
    dr.h = maxHeight
    dr = window.assetManager.inflateRectForStyle(me, dr)
    window.setMEData(me, 'drawRect', dr)

    available.x += dr.w
    available.w -= dr.w

    return available

def vpack(window, available, me):
    dr = copy.copy(available)

    totalHeight = 0
    maxWidth = 0

    # reserve space now to get positioning correct
    kidAvailable = window.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        kidAvailable = window.assetManager.layout(kidAvailable, kid)
        kr = window.getMEData(kid, 'drawRect')
        totalHeight += kr.h
        maxWidth = max(maxWidth, kr.w)

    # Pass 2: Set the width o the kids to the mas width found
    for kid in me['contents']:
        window.getMEData(kid, 'drawRect').w = maxWidth

    dr.h = totalHeight
    dr.w = maxWidth
    dr = window.assetManager.inflateRectForStyle(me, dr)
    window.setMEData(me, 'drawRect', dr)

    available.y += dr.h
    available.h -= dr.h

    return available


def layout(window, available, me):
    if 'contents' not in me:
        return available   # No-op
    sd = window.assetManager.getStyleData(me['style'])
    if sd['side'] == 'top':
        return hpack(window, available, me)
    if sd['side'] == 'left':
        return vpack(window, available, me)

    return available
