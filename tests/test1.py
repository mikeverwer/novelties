def func(arg: bool = True) -> None:
    thing = 'dumb'
    if thing is not None and arg:
        return thing
    
print(func(True))