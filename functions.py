def simple_func(arg1, arg2):
    print("simple_func1", simple_func("引数1", "引数2"))
def spam(arg1, arg2, arg3, arg4, arg5):
    print(arg1,arg2,arg3,arg4,arg5)
spam(1, 2, 3, arg4=4, arg5=5)

args = (2, 3)
kwags = {'arg4': 4, 'arg5': 5}

spam(1, *args, **kwags)

spam(*[1, 2], *[3, 4], 5)
spam(**{'arg1': 1, 'arg2': 2, 'arg3':3, 'arg4': 4, 'arg5': 5})