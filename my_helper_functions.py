# my_helper_functions.py
def greet(name):
 return f"Hello, {name} from my_helper_functions!"

def add(a, b):
 return a + b

if __name__ == "__main__":
    print(f"This line will always print when my_helper_functions.py is loaded. __name__ is: {__name__}")
    print("my_helper_functions.py is being run directly!")
    user_name = input("Enter your name: ")
    print(greet(user_name))
    result = add(10, 5)
    print(f"The sum of 10 and 5 is: {result}")
    print("This is example usage or test code.")
