import copy


def canExecute(ctx, me):
    return 'submenu' in me

def execute(ctx, me):
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

