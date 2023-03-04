import copy

def hpack(ctx, available, me):
    dr = copy.copy(available)

    totalWidth = 0
    maxHeight = 0

    # reserve space now to get positioning correct
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        kidAvailable = ctx.assetManager.layout(kidAvailable, kid)
        kr = ctx.getMEData(kid, 'drawRect')
        totalWidth += kr.w
        maxHeight = max(maxHeight, kr.h)

    # Pass 2: Set the width o the kids to the mas width found
    for kid in me['contents']:
        ctx.getMEData(kid, 'drawRect').h = maxHeight

    dr.w = totalWidth
    dr.h = maxHeight
    dr = ctx.assetManager.inflateRectForStyle(me, dr)
    ctx.setMEData(me, 'drawRect', dr)

    available.x += dr.w
    available.w -= dr.w

    return available

def vpack(ctx, available, me):
    dr = copy.copy(available)

    totalHeight = 0
    maxWidth = 0

    # reserve space now to get positioning correct
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        kidAvailable = ctx.assetManager.layout(kidAvailable, kid)
        kr = ctx.getMEData(kid, 'drawRect')
        totalHeight += kr.h
        maxWidth = max(maxWidth, kr.w)

    # Pass 2: Set the width o the kids to the mas width found
    for kid in me['contents']:
        ctx.getMEData(kid, 'drawRect').w = maxWidth

    dr.h = totalHeight
    dr.w = maxWidth
    dr = ctx.assetManager.inflateRectForStyle(me, dr)
    ctx.setMEData(me, 'drawRect', dr)

    available.y += dr.h
    available.h -= dr.h

    return available


def layout(ctx, available, me):
    if 'contents' not in me:
        return available   # No-op
    sd = ctx.assetManager.getStyleData(me['style'])
    if sd['side'] == 'top':
        return hpack(ctx, available, me)
    if sd['side'] == 'left':
        return vpack(ctx, available, me)

    return available
