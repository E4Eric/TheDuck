import copy

# State
highlightME = None

# Menu handling
mainMenuItem = None
openSubMenus = []

# Drag support
dragController = None

listenerRegistered = False

################################################
## Highlight Handling
################################################
def highlightListener(ctx, me, attName, oldVal, newVal):
    print(f'highlight Changed: was {oldVal} is {newVal}')
    ctx.window.update()

def registerHighlightListener(ctx):
    ctx.subscribe('highlighter', highlightListener)

def highlightElement(ctx, me):
    global highlightME, listenerRegistered
    if not listenerRegistered:
        registerHighlightListener(ctx)
        listenerRegistered = True

    # To get highlighting you simply supply a '(Over)' version of your style
        me['style'] = me['style'] + " (Over)"
        highlightME = me
        highlightME['Highlighted'] = True
        ctx.publish(highlightME, 'Highlighted', False, True)


def clearHighlight(ctx):
    global highlightME  # Declare highlightME as a global variable
    if highlightME != None:
        style = highlightME['style']
        style = style.rstrip(' (Over)')
        highlightME['style'] = style
        ctx.window.update()

        ctx.publish(highlightME, 'Highlighted', True, False)
        highlightME = None

################################################
## Tooltip Handling
################################################
def showTooltip(ctx, me):
    if 'tooltip' not in me:
        return

    # construct the model element to represent the tooltip
    tooltip = me['tooltip']
    tooltipME = { "style": "Tooltip", 'label': tooltip }

    # now position it correctly, give it plenty of room
    dr = ctx.getMEData(me, 'drawRect')
    available = copy.copy(dr)
    available.x = dr.x
    available.y = dr.y + dr.h + 5
    available.w = 10000
    available.h = 10000

    layoutCode = ctx.assetManager.getLayout('label')
    layoutCode.layout(ctx, available, tooltipME)

    ctx.displayManager.addLayer("tooltip", tooltipME)

def clearTooltip(ctx):
    ctx.displayManager.removeLayer('tooltip')

################################################
## Menu Handling
################################################
def clearSubMenus(ctx):
    global openSubMenus, mainMenuItem
    for layerName in reversed(openSubMenus):
        ctx.displayManager.removeLayer(layerName)
    openSubMenus.clear()
    mainMenuItem = None

def showMenu(ctx, me, x, y):
    global openSubMenus, highlightME

    if 'submenu' not in me:
        return

    dr = ctx.getMEData(me, 'drawRect')
    submenu = me['submenu']

    ctx.displayManager.showPartInWidget(submenu, "Menu", x, y)


    # layerName = f"Sub Menu  {len(openSubMenus)}"
    # ctx.displayManager.addLayer(layerName, submenu)
    # openSubMenus.append(layerName)

def showDropDown(ctx, me):
    global mainMenuItem

    if mainMenuItem != me:
        clearSubMenus(ctx)

    mainMenuItem = me
    dr = ctx.getMEData(me, 'drawRect')
    showMenu(ctx, me, dr.x, dr.y + dr.h)

def showSubMenu(ctx, me):
    global openSubMenus, mainMenuItem, highlightME

    if 'submenu' not in me:
        return

    dr = ctx.getMEData(me, 'drawRect')
    showMenu(ctx, me, dr.x + dr.w - 2, dr.y - 2)

def enter(me, x ,y):
    global mainMenuItem, dragController

    # Hightlight handling...if the style has a ' (Over)' defined switchto it
    style = me['style']
    if ctx.assetManager.testForStyle(style + " (Over)"):
        highlightElement(ctx, me)

    # If the main menu is open and we go over another one then open it
    if mainMenuItem != None and 'Main Menu Item' in me['style'] and me != mainMenuItem:
        showDropDown(ctx, me)

    if 'dragController' in me:
        dragController = ctx.assetManager.getController(me['dragController'])
        dragController.enter(ctx, me, x, y)

def leave(me, x, y):
    global dragController
    if dragController != None:
        if not dragController.isDragging():
            dragController.leave(ctx, me)
            dragController = None

    clearHighlight(ctx)
    clearTooltip(ctx)

def mouseMove(ctx, me, x, y):
    global dragController
    if dragController != None:
        dragController.mouseMove(ctx, me, x, y)


def lclick(ctx, me, x, y):
    global mainMenuItem
    style = me['style']
    if 'Main Menu Item' in style and 'submenu' in me:
        if me == mainMenuItem:
            clearSubMenus(ctx)
        else:
            showDropDown(ctx, me)

    # HACK!! this test is too generic...
    if 'Menu' not in style:
        clearSubMenus(ctx)

    # Execute meu / toolbar actions
    if 'lclickAction' in me:
        actionModule = ctx.assetManager.getAction(me['lclickAction'])
        if actionModule.canExecute(ctx, me):
            actionModule.execute(ctx, me)

def hover(ctx, me):
    showTooltip(ctx, me)    # if any
    if 'Menu Item' in me['style']:
        if 'Main Menu Item' not in me['style'] and 'submenu' in me:
            showSubMenu(ctx, me)

def mouseButtonPressed(ctx, button, x, y):
    if dragController != None:
        dragController.mouseButtonPressed(ctx, button, x, y)
def mouseButtonReleased(ctx, button, x, y):
    if dragController != None:
        dragController.mouseButtonReleased(ctx, button, x, y)