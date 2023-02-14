import copy


def layout(ctx, available, me):
    pct = me['percentage'] / 100
    side = me['side']

    # first layout on top
    me['drawRect'] = copy.copy(available)

    height = int(available.h * pct + 0.5)
    width = int(available.w * pct + 0.5)
    if side == 'top':
        me['drawRect'].h = height
        available.y += height
        available.h -= height

    if side == 'bottom':
        me['drawRect'].y = (available.y + available.h) - height
        me['drawRect'].h = height
        available.h -= height

    if side == 'left':
        me['drawRect'].w = width
        available.x += width
        available.w -= width

    if side == 'right':
        me['drawRect'].x = (available.x + available.w) - width
        me['drawRect'].w = width
        available.w -= width

    # drawRect set...layout the kids inside me
    # grab room for the style first since we layout inside us...
    kidAvailable = ctx.assetManager.adjustAvailableForStyle(me, me['drawRect'])
    if 'contents' in me:
        for kid in me['contents']:
            kidAvailable = ctx.assetManager.layout(kidAvailable, kid)

    return available
