
def canExecute(ctx, me):
    return 'items' in me

def execute(ctx, me):
    print("showDropDown:")
    for item in me['items']:
        print("  ", item.label)

