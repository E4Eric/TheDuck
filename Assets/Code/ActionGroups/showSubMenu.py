
def canExecute(cts, me):
    return 'items' in me

def execute(ctx, me):
    print("showSubMenu:")
    for item in me['items']:
        print("  ", item.label)

