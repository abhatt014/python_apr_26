from faker import Faker
fake=Faker()
print(f"SNO\tNAME:\t\tADDRESS")
for i in range(10):
    name=fake.name()
    address=fake.address() 
    print(f"{i+1}\t{name}:\t\t{address}")

