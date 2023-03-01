import copy


def canExecute(ctx, me):
    return 'lclickAction' in me

def execute(ctx, me):
    action = me['lclickAction']
    print(f'** executing "{action}" ')
