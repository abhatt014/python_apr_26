# def calu():
#     val1=int(input("enter 1st val"))
#     val2=int(input("enter 2nd val"))
#     res= val1+val2
#     print(res)

# calu()
# calu()
# calu()



# def greet_person(name): # 'name' is a parameter
#     print(f"Hello, {name}!")

# def add_numbers(a, b):
#  result = a + b
#  print(f"The sum of {a} and {b} is {result}")


# greet_person("Alice") # "Alice" is an argument
# greet_person("Bob")
# add_numbers(5, 3) # Output: The sum of 5 and 3 is 8
# add_numbers(10, 30)

def add_numbers_return(a, b):
    c = a + b
    return c  # Returns the value of c

def get_greeting(name):
    return f"Welcome, {name}!"
    
sum_result = add_numbers_return(10, 7)  # Returned value assigned to sum_result
print(f"Returned sum: {sum_result}")    # Output: Returned sum: 17
print(add_numbers_return(1, 2))         # Output: 3
message = get_greeting("Charlie")
print(message)  # Output: Welcome, Charlie!
