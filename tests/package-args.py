def 

def return_args(args):
    for i, arg in enumerate(args):
        arg{i} = arg
    return arg1, arg2, arg3, arg4

# Example usage
packed_args = (1, 2, 3, 4)
result = return_args(*packed_args)
print(result)
