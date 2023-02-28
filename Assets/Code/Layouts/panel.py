import copy


def layout(ctx, available, me):
    side = me['side']
    if 'size' in me:
        size = me['size']

    # first layout on top
    me['drawRect'] = copy.copy(available)

    # '-1' means take it all
    if size == -1:
        available.w = 0
        available.h = 0
    elif side == 'top':
        me['drawRect'].h = size
        available.y += size
        available.h -= size

    elif side == 'bottom':
        me['drawRect'].y = (available.y + available.h) - size
        me['drawRect'].h = size
        available.h -= size
    elif side == 'left':
        me['drawRect'].w = size
        available.x += size
        available.w -= size
    elif side == 'right':
        me['drawRect'].x = (available.x + available.w) - size
        me['drawRect'].w = size
        available.w -= size

    # drawRect set...layout the kids inside me
    # grab room for the style first since we layout inside us...
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, me['drawRect'])
    if 'contents' in me:
        for kid in me['contents']:
            kidAvailable = ctx.assetManager.layout(kidAvailable, kid)

    return available
