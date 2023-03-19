import copy


def layout(window, available, me):
    if 'contents' not in me:
        return available   # No-op

    dr = copy.copy(available)
    sd = window.assetManager.getStyleData(me['style'])

    adjusted = window.assetManager.adjustAvailableForStyle(me, available)
    side = sd['side']

    # reserve the are we need for our style frame
    maxHeight = 0
    if side == 'top' or side == 'bottom':
        # reserve space now to get positioning correct
        kidAvailable = copy.copy(adjusted)
        totalHeight = 0
        startWidth = kidAvailable.w
        startX = kidAvailable.x

        spacer = None
        for kid in me['contents']:
            # right adjustment
            if kid['style'] == 'spacer':
                spacer = kid
                continue

            kidAvailable = window.assetManager.layout(kidAvailable, kid)
            if kidAvailable.w < 0:  # ..overflow, wrap
                kidAvailable.x = startX
                kidAvailable.w = startWidth
                kidAvailable.y += maxHeight
                kidAvailable.h -= maxHeight
                kidAvailable = window.assetManager.layout(kidAvailable, kid)
                totalHeight += maxHeight
                maxHeight = window.getMEData(kid, 'drawRect').h

            maxHeight = max(maxHeight, window.getMEData(kid, 'drawRect').h)

        totalHeight += maxHeight

        if spacer != None:
            dx = 0
            for kid in me['contents']:
                if kid['style'] == 'spacer':
                    dx = kidAvailable.w
                    continue

                if dx > 0:
                    kr = window.getMEData(kid, 'drawRect')
                    kr = kr.offset(dx, 0)

        # here we need to only change the height for the style
        styleData = window.assetManager.getStyleData(me['style'])
        totalHeight += styleData['th'] + styleData['tm'] + styleData['bh'] + styleData['bm']
        dr.h = totalHeight

    if side == 'top':
        available.y += dr.h
    elif side == 'bottom':
        dy = available.h - dr.h
        dr.offset(0, dy)

    window.setMEData(me, 'drawRect', dr)

    available.h -=  dr.h
    return available
