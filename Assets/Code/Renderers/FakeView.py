

def draw(ctx, me):
    styleImage = ctx.assetManager.getStyleImage(me['style'])
    visible = ctx.window.crop(styleImage, 0, 0, me['drawRect'].w, me['drawRect'].h)
    ctx.window.drawIcon(me['drawRect'].x, me['drawRect'].y, visible)
