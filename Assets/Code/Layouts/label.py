import copy


def layout(ctx, available, me):
    dr = copy.copy(available)
    sd = ctx.assetManager.getStyleData(me['style'])

    # Hack!! assume horizontal, no icon and a three pixel 'gap'

    iconW = 0
    iconH = 0
    if 'icon' in me:
        icon = ctx.assetManager.getIconImage(me['icon'])
        iconW = ctx.window.getImageWidth(icon)
        iconH = ctx.window.getImageHeight(icon)

    textW = 0
    textH = 0
    if 'label' in me:
        textW = ctx.window.getTextWidth(me['label'], sd['fontSpec'])
        textH = ctx.window.getTextHeight(me['label'], sd['fontSpec'])

    dr.w = textW + iconW
    dr.h = max(iconH, textH)

    # put in the label gap if necessary
    if 'label' in me:
        if 'icon' in me:
            if 'labelGap' in sd:
                dr.w += sd['labelGap']

    me['drawRect'] = dr

    ctx.assetManager.inflateDrawRectForStyle(me)
    available.x += me['drawRect'].w
    available.w -= me['drawRect'].w

    return available
