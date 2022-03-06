#python refresher syntax 
#created 03/06/2022
'''
multiline, docstring 
can also use """ ***comments** """ 
used to define function descriptions 
'''

x = 1 #int 
y = 1.5 #float 
name  = 'John' #string 
is_cool = True # bool

# multiple assignments
x, y, name, is_cool = (1, 2.5, 'John', True)
print("Hello John")
print(x, y, name, is_cool)

#casting 
x = str(x)
y = int(y)
#print(type(y))

#string 
name = "Upendra"
age = 24

#concatenation 
print("Hello, my name is " + name + 'and I am ' + str(age))

#arguments by position
print('My name is {name} and I and I am {age}'.format(name=name, age=age))

#F-Strings (3.6+)
print(f"Hello, my name is {name} and I am {age}")

#sring methods 
s = "hello world"
#.upper(), .swapcase(), .len(), .replace
# .count(s) .endswith('d'), .split()-> list/array, .find('r'), .isalnum(). isalpha(), isnumeric()
# print(s.capitalize())
# print(s.swapcase())
# print(s.replace('hello', 'hi'))

#list ==> more common way 
numbers = [1, 2, 3, 4, 5]
#use constructor 
# number2= list ((1, 2, 3, 4, 5))
# print(number2)

print(numbers)

#append to the list 
fruits = ['apple', 'mango', 'orange']
print(len(fruits))
fruits.append("Pears")
fruits.remove('apple')
fruits.insert(2, 'Peach')
fruits.pop(1)
print(fruits)
fruits.reverse()
print(fruits)
fruits[0] = 'Guava'
fruits.sort()
print(fruits)

#create tuples 
fruits1 = ('apple','banana', 'orange', 'mango')
print(fruits1)