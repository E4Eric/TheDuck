

def draw(ctx, me):
    styleImage = ctx.assetManager.getStyleImage(me['style'])
    dr = ctx.getmeData(*me, 'drawRect')
    visible = ctx.window.crop(styleImage, 0, 0, dr.w, dr.h)
    dr = ctx.getMEData(me, 'drawRect')
    ctx.window.drawIcon(dr.x, dr.y, visible)
