import copy


def layout(ctx, available, me):
    side = me['side']
    if 'size' in me:
        size = me['size']
    if 'percentage' in me:
        if side == 'top' or side == 'bottom':
            size = (me['percentage'] / 100.0) * available.h
        else:
            size = (me['percentage'] / 100.0) * available.w

    # first layout on top
    me['drawRect'] = copy.copy(available)
    if side == 'top':
        me['drawRect'].h = size
        available.y += size
        available.h -= size

    if side == 'bottom':
        me['drawRect'].y = (available.y + available.h) - size
        me['drawRect'].h = size
        available.h -= size

    if side == 'left':
        me['drawRect'].w = size
        available.x += size
        available.w -= size

    if side == 'right':
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
