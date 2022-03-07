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

# delete a tuples 
# del fruits1
'''
Day-2 Python Refresher 
03/07/2022
'''
print("\n******** Day 2***********")

# set is a collection which is unordere and unindexed. No duplicate members 

#create set 
fruits_set = {'Apples', 'Oranges', 'Mango'}
#check if in set 
print('Apples' in fruits_set)

#remove from set 
fruits_set.remove('Mango')

#add iten in set 
fruits_set.add("Pear")
print(fruits_set)

fruits_set.add('Apples')
#clear set 
# fruits_set.clear()

print(fruits_set)


# A dictionary is a collection which is unordered changeable and indexed. No duplicates 

# create dict 
person = {
    'first_name': 'John',
    'last_name' : 'Smith',
    'age' : '25'
}

#using construtor 
# person2 = dict(first_name = 'Sara', last_name='Williams')

# print(person2)
#Get values 
print(person['first_name'])
print(person.get('last_name'))

# add key/value 
person['phone'] = '555-555-5555'

#Get dict keys 
print(person.keys())
# print(person, type(person))

#Get items 
print(person.items())


#copy dictionary 
person2 = person.copy()
person2['city'] = "Lawrenceville"

#remove item 
del(person['age'])
person.pop('phone')

#clear 
person.clear()

#get length 
print(len(person2))

#list of dict 
people = [
    {'name' : 'MArtha', 'age':30},
    {'name' : 'kevin', 'age' : 25}
]

print(people[1]['name'])