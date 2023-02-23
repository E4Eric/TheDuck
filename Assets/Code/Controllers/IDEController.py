import copy

# State
highlightME = None

# Menu handling
mainMenuItem = None
openSubMenus = []

################################################
## Highlight Handling
################################################
def highlightElement(ctx, me):
    global highlightME  # Declare highlightME as a global variable
    style = me['style']
    if ctx.assetManager.testForStyle(style + " (Over)"):
        me['style'] = me['style'] + " (Over)"
        ctx.window.update()
        highlightME = me

def clearHighlight(ctx):
    global highlightME  # Declare highlightME as a global variable
    if highlightME != None:
        style = highlightME['style']
        style = style.rstrip(' (Over)')
        highlightME['style'] = style
        ctx.window.update()
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
    dr = me['drawRect']
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
    global openSubMenus
    for layerName in reversed(openSubMenus):
        ctx.displayManager.removeLayer(layerName)
    openSubMenus.clear()

def showMenu(ctx, me, x, y):
    global openSubMenus, highlightME

    if 'submenu' not in me:
        return

    dr = me['drawRect']
    submenu = me['submenu']

    # position it correctly, give it plenty of room
    available = copy.copy(dr)
    available.x = x
    available.y = y
    available.w = 10000
    available.h = 10000

    layoutCode = ctx.assetManager.getLayout('pack')
    layoutCode.layout(ctx, available, submenu)

    layerName = f"Sub Menu  {len(openSubMenus)}"
    ctx.displayManager.addLayer(layerName, submenu)
    openSubMenus.append(layerName)

def showDropDown(ctx, me):
    global openSubMenus, mainMenuItem, highlightME

    if 'submenu' not in me:
        return
    if mainMenuItem == me:
        return  # already open
    if mainMenuItem != me:
        clearSubMenus(ctx)

    mainMenuItem = me

    dr = me['drawRect']
    showMenu(ctx, me, dr.x, dr.y + dr.h)
def showSubMenu(ctx, me):
    global openSubMenus, mainMenuItem, highlightME

    if 'submenu' not in me:
        return

    dr = me['drawRect']
    showMenu(ctx, me, dr.x + dr.w - 2, dr.y - 2)

def enter(ctx, me):
    global mainMenuItem

    # Hightlight handling...if the style has a ' (Over)' defined switchto it
    highlightElement(ctx, me)

    # If the main menu is open and we go over another one then open it
    if mainMenuItem != None and 'Main Menu Item' in me['style'] and me != mainMenuItem:
        showDropDown(ctx, me)

def leave(ctx, me):
    clearHighlight(ctx)
    clearTooltip(ctx)


def lclick(ctx, me, x, y):
    global mainMenuItem
    style = me['style']
    if 'Main Menu Item' in style and 'submenu' in me:
        if me == mainMenuItem:
            clearSubMenus(ctx)
            mainMenuItem = None
        else:
            showDropDown(ctx, me)

    if 'lclickAction' in me:
        actionModule = ctx.assetManager.getAction(me['lclickAction'])
        if actionModule.canExecute(ctx, me):
            actionModule.execute(ctx, me)

def hover(ctx, me):
    showTooltip(ctx, me)    # if any
    if 'Menu Item' in me['style']:
        if 'Main Menu Item' not in me['style'] and 'submenu' in me:
            showSubMenu(ctx, me)

