try:
    val1=int(input("enter 1st val"))
    val2=int(input("enter 2nd val"))
    res = val1/val2
    print(res)
except ZeroDivisionError:
    print("Error: Cannot divide by zero! use diff value")
except ValueError:
    print("use only numbers, alphabets cant be divided")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    print("code executed successfully")
