

def draw(window, me):
    dr = window.getMEData(me, 'drawRect')
    sd = window.assetManager.getStyleData(me['style'])

    # Adjust the top/right for the style
    x = dr.x + sd['lw'] + sd['rm']
    y = dr.y + sd['th'] + sd['tm']

    if 'icon' in me:
        icon = window.assetManager.getIconImage(me['icon'])
        window.window.drawIcon(x, y, icon)
        x += window.window.getImageWidth(icon)
        if 'label' in me:
            if 'labelGap' in sd:
                x += sd['labelGap']

    if 'label' in me:
        text = me['label']
        fontSpec = ''
        if 'fontSpec' in sd:
            fontSpec = sd['fontSpec']

        window.window.drawText(x, y, text, fontSpec)
