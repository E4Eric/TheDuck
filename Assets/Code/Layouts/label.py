import copy


def layout(ctx, available, me):
    dr = copy.copy(available)

    style = me['style']
    sd = ctx.assetManager.getStyleData(style)
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

    # 'wrap' ourselves in our style, growing as necessary
    dr = ctx.assetManager.inflateRectForStyle(me, dr)
    ctx.setMEData(me, 'drawRect', dr)

    if side == 'top':
        available.x += dr.w
        available.w -= dr.w

    if side == 'left':
        available.y += dr.h
        available.h -= dr.h

    return available
