import time

panel = None
sd = None
panelSide = None

okToDrag = False
dragging = False

downX = None
downY = None
trackX = None
trackY = None


def resetGlobals():
    global panel, sd, panelSide, okToDrag, dragging, downX, downY, trackX, trackY
    print("reset globals")

    panel = None
    sd = None
    panelSide = None

    okToDrag = False
    dragging = False

    downX = None
    downY = None
    trackX = None
    trackY = None

def setDragging(val):
    global dragging
    dragging = val
    print(f'setDragging: {dragging}')

def isDragging():
    global dragging
    print(f'isDragging: {dragging}')
    return dragging

def setDragState(ctx, me, x, y):
    global panel, okToDrag, panelSide, sd

    dr = panel['drawRect']
    if panelSide == 'left':
        # Hack-ish...the style is expected to whow an affordance
        maxX = dr.x + dr.w
        if x >= (maxX - sd['rw']) and x <= maxX:
            okToDrag = True
            ctx.window.setPointer("EW")
        else:
            print('Cursor: Default')
            ctx.window.setPointer("Default")

    if panelSide == 'bottom':
        # Hack-ish...the style is expected to whow an affordance
        if y >= dr.y and y <= (dr.y + sd['th']):
            okToDrag = True
            ctx.window.setPointer("NS")
        else:
            print('Cursor: Default')
            ctx.window.setPointer("Default")

    if panelSide == 'right':
        # Hack-ish...the style is expected to whow an affordance
        if x >= dr.x and x <= (dr.x + sd['lw']):
            okToDrag = True
            ctx.window.setPointer("EW")
        else:
            print('Cursor: Default')
            ctx.window.setPointer("Default")

    if panelSide == 'top':
        # Hack-ish...the style is expected to whow an affordance
        maxY = dr.y + dr.h
        if y >= (maxY - sd['bh']) and y <= maxY:
            okToDrag = True
            ctx.window.setPointer("NS")
        else:
            print('Cursor: Default')
            ctx.window.setPointer("Default")

def enter(ctx, me, x, y):
    global panel, panelSide, sd

    panel = me
    sd = ctx.assetManager.getStyleData(panel['style'])
    panelSide = panel['side']

    setDragState(ctx, panel, x, y)

def leave(ctx, me):
    ctx.window.setPointer("Default")

def dragStart(ctx, panel, x, y):
    global trackX, trackY
    print('*** Drag Start ***')
    setDragging(True)
    trackX = x
    trackY = y

    dragMove(ctx, panel, x, y)

def dragMove(ctx, panel, x, y):
    global trackX, trackY
    if panelSide == 'left':
        dx = x - trackX
        panel['size'] += dx

    if panelSide == 'bottom':
        dy = y - trackY
        panel['size'] -= dy

    if panelSide == 'right':
        dx = x - trackX
        panel['size'] -= dx

    if panelSide == 'top':
        dy = y - trackY
        panel['size'] += dy

    if panel['size'] < 10:
        panel['size'] = 10
    ctx.displayManager.refresh()

    trackX = x
    trackY = y

def mouseMove(ctx, me, x, y):
    global dragging
    if dragging:
        dragMove(ctx, panel, x, y)
    else:
        setDragState(ctx, panel, x, y)

def mouseButtonPressed(ctx, button, x, y):
    global okToDrag, downX, downY

    if button == 'left' and okToDrag:
        dragStart(ctx, ctx.eventProxy.curElement, x, y)
        downX = x
        downY = y

def mouseButtonReleased(ctx, button, x, y):
    global dragging
    if dragging and button == 'left':
        setDragging(False)
        # resetGlobals()
        # setDragState(ctx, panel, x, y)


