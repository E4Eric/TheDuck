import copy


def layout(ctx, available, me):
    dr = copy.copy(available)

    sd = ctx.assetManager.getStyleData(me['style'])
    side = sd['side']

    labelGap = 0
    iconW = 0
    iconH = 0
    if 'icon' in me:
        icon = ctx.assetManager.getIconImage(me['icon'])
        iconW = ctx.window.getImageWidth(icon)
        iconH = ctx.window.getImageHeight(icon)

    textW = 0
    textH = 0
    if 'label' in me and 'labelGap' in sd:
        # if we have both a label and an icon we set the 'labelGap'
        if 'icon' in me:
            labelGap = sd['labelGap']

        textW = ctx.window.getTextWidth(me['label'], sd['fontSpec'])
        textH = ctx.window.getTextHeight(me['label'], sd['fontSpec'])

    if side == 'top':
        dr.w = textW + iconW + labelGap
        dr.h = max(iconH, textH)

    if side == 'left':
        dr.w = max(iconW, textW)
        dr.h = textH + iconH + labelGap

    me['drawRect'] = dr

    # 'wrap' ourselves in our style, growing as necessary
    ctx.assetManager.inflateDrawRectForStyle(me)

    if side == 'top':
        available.x += me['drawRect'].w
        available.w -= me['drawRect'].w

    if side == 'left':
        available.y += me['drawRect'].h
        available.h -= me['drawRect'].h

    return available
