def func(*args):
    return sum(args)


print(func((x for x in range(10))))