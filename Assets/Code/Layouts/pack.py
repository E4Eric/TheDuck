import copy

def hpack(ctx, available, me):
    me['drawRect'] = copy.copy(available)

    totalWidth = 0
    maxHeight = 0

    # reserve space now to get positioning correct
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        ctx.assetManager.layout(kidAvailable, kid)
        kidAvailable.x += kid['drawRect'].w
        kidAvailable.w -= kid['drawRect'].w
        totalWidth += kid['drawRect'].w
        maxHeight = max(maxHeight, kid['drawRect'].h)

    me['drawRect'].w = totalWidth
    me['drawRect'].h = maxHeight
    ctx.assetManager.inflateDrawRectForStyle(me)

    available.x += me['drawRect'].w
    available.w -= me['drawRect'].w

    return available
def vpack(ctx, available, me):
    me['drawRect'] = copy.copy(available)

    totalHeight = 0
    maxWidth = 0

    # reserve space now to get positioning correct
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, available)
    for kid in me['contents']:
        kidCopy = copy.copy(kidAvailable)
        ctx.assetManager.layout(kidCopy, kid)
        kidAvailable.y += kid['drawRect'].h
        kidAvailable.h -= kid['drawRect'].h
        totalHeight += kid['drawRect'].h
        maxWidth = max(maxWidth, kid['drawRect'].w)

    # Pass 2: Set the width o the kids to the mas width found
    for kid in me['contents']:
        kid['drawRect'].w = maxWidth


    me['drawRect'].h = totalHeight
    me['drawRect'].w = maxWidth
    ctx.assetManager.inflateDrawRectForStyle(me)

    available.y += me['drawRect'].h
    available.h -= me['drawRect'].h

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
