import copy


def canExecute(cts, me):
    return 'tooltip' in me

def execute(ctx, me):
    # construct the model element to represent the tooltip
    tooltip = me['tooltip']
    tooltipME = { "style": "Tooltip", 'label': tooltip }
    print("showTooltip:", me['tooltip'])

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

