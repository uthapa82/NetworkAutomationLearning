## a class is like a blueprint for creating objects. An object has properties and methods(functions)
# associated with it. Almost everything in python is an object

#Create class 

class User:
    # constructor 
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        
    def greeting(self):
        return f'My name is {self.name} and I am {self.age}'
    
    def has_birthday(self):
        self.age += 1 

#extend class
class Customer(User):
    # constructor 
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        self.balance = 0
    def set_balance(self, balance):
        self.balance = balance
        
    def greeting(self):
       return f'My name is {self.name} and I am {self.age} and my balance is {self.balance}'
    
# initialize user object 
brad = User("Upendra Thapa", 'tupen@gmail.com', 25)

#Init Customer 
janet = Customer("Pradeep Ojha", "pojaha@gmail.com", 25)

janet.set_balance(500)
#print(janet.greeting())
print(brad.name)
print(brad.email)
print(brad.age)
        
brad.has_birthday()
print(brad.greeting())