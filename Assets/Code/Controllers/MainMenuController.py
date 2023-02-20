import copy


def enter(ctx, me):
    style = me['style']
    if ctx.assetManager.testForStyle(style + " (Over)"):
        me['style'] = style + " (Over)"
        ctx.window.update()

def leave(ctx, me):
    style = me['style']
    style = style.rstrip(' (Over)')
    me['style'] = style
    ctx.window.update()

def lclick(ctx, me):
    print(f'Open Menu: {me["label"]}')
    # now position it correctly, give it plenty of room
    submenu = me['submenu']

    dr = me['drawRect']
    available = copy.copy(dr)
    available.x = dr.x
    available.y = dr.y + dr.h
    available.w = 10000
    available.h = 10000

    layoutCode = ctx.assetManager.getLayout('pack')
    layoutCode.layout(ctx, available, submenu)

    ctx.displayManager.addLayer("Drop Down", submenu)
