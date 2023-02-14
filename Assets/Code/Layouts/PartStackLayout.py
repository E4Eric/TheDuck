import copy

def layout(ctx, available, me):
    # Get our chunk of 'available' using the 'panel'  layout
    panelLayout = ctx.assetManager.layoutCodeCache['panel']
    available = panelLayout.layout(ctx, available, me)

    # Now use the PartStack's 'drawRect' to lay out the internals
    dr = me['drawRect']
    adjusted = ctx.assetManager.adjustAvailableForStyle(me, dr)

    # First the View Tabs...a packed list of labels
    # Hack!! Need to allow different 'kids' lists rather than assuming 'contents'
    packLayout = ctx.assetManager.layoutCache['pack']
    afterPPack = packLayout(adjusted, me)

    # We need three parts to the layout...Parts Tabs, current Part's toolbar (/w/ menu affordance if needed) and the width od the min/Max buttons
    tabsWidth = afterPPack.x

    # Get the selected tab's toolbar
    selected = next(iter(me['contents']))


    return available
