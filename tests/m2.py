# m2.py
from m1 import global_variable, update_global_variable

# Access the global variable from module1
print("Inside module2: Original global_variable =", global_variable)

# Update the global variable from module1
update_global_variable()

# Access the updated global variable
print("Inside module2: Updated global_variable =", global_variable)

def update_global_variable():
    global global_variable
    global_variable += 5
    print("Inside module1: Updated global_variable =", global_variable)