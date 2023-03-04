

def draw(ctx, me):
    dr = ctx.getMEData(me, 'drawRect')
    sd = ctx.assetManager.getStyleData(me['style'])

    # Adjust the top/right for the style
    x = dr.x + sd['lw'] + sd['rm']
    y = dr.y + sd['th'] + sd['tm']

    if 'icon' in me:
        icon = ctx.assetManager.getIconImage(me['icon'])
        ctx.window.drawIcon(x, y, icon)
        x += ctx.window.getImageWidth(icon)
        if 'label' in me:
            if 'labelGap' in sd:
                x += sd['labelGap']

    if 'label' in me:
        text = me['label']
        fontSpec = ''
        if 'fontSpec' in sd:
            fontSpec = sd['fontSpec']

        ctx.window.drawText(x, y, text, fontSpec)
