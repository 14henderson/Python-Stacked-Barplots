

def wrapper(func):
    print("Before function call")
    func()
    print("After function call")
    return func

@wrapper
def func():
    print("Hello, World!")


func()