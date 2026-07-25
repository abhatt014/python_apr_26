import my_helper_functions

if __name__ == "__main__":
    print(f"Running main_app.py. __name__ here is: {__name__}")
    message = my_helper_functions.greet("Bob")
    print(message)
    sum_result = my_helper_functions.add(7, 3)
    print(f"From main_app, the sum is: {sum_result}")
