with open('data.txt', 'r') as f:
    content = f.read()
    print(content)

with open('output_with.txt', 'w') as f:
    f.write("Hello from the 'with' statement.\n")
    f.write("This file will auto-close.\n")
    print("Data written to output_with.txt")
