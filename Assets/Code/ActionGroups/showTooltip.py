
def canExecute(cts, me):
    return 'tooltip' in me

def execute(ctx, me):
    print("showTooltip:", me['tooltip'])

