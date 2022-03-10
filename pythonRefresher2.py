#Day 2 
#03/07/2022
#functions.py from traversary Media 

# a function is a block of code which only runs when it is called. In python
# we do not use curly brackets, we use indentation with tabs or spaces 

#create function 
def sayHello(name = "Kevin"):
    print(f'Hello {name}')

#return values 
def getSum(num1, num2):
    totalSum = num1 + num2
    return totalSum

#function call 
num = getSum(3, 4)
print(num)

#lambda function is a small anonymous function
#A lambda function can take any number of arguments, but can only have one expression
# very similar to haskell 
getSum = lambda num1, num2:num1 + num2

print(getSum(10,3))


#conditional if /else 
x = 10
y = 30

#comparison operators(==, !=, >, <, >=, <=)

if  x > y:
    print(f'{x} is greater than {y}')
elif x == y:
    print("x is equal to y")
else:
    print("y is greater than x ")
    
#nested if 
if x > 2:
    if x <= 10:
        print("x is greater than 2 and less than or equal to 10")
#logical operators, or not 
if x > 2 and x <= 10:
    print("x is greater than 2 and less than or equal to 10")

# not 
if not (x == y):
    print("x is not equal to y")

#membership operators (not, not in)
numbers = [1,2,3,4,5,6,7,10]

if x in numbers:
    print(x in numbers)
    
if y not in numbers:
    print(y not in numbers)
    
#loop 
people = ['John', 'Paul', 'Sara', 'Susan']

#simple for loop 
for person in people:
    print(f"current person: {person}")

#Break 1:01:45 -traversy media
