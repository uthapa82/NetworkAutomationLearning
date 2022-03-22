#python has functions for creating, reading, updating and deleting files 

# open files
from argparse import _MutuallyExclusiveGroup, MetavarTypeHelpFormatter
from itertools import tee


myFile = open('myfile.txt', 'w')

#Get some info
print("Name:", myFile.name)
print("Is closed : ", myFile.closed)
print('Opening Mode: ', myFile.mode)

#write to the file 
myFile.write("I love Python ")
myFile.write("I enjoy my life")
myFile.close()

#append to file 
myFile = open('myfile.txt', 'a')
myFile.write(" I am learning network automation using Python")

#read from the file 
myFile = open('myfile.txt', 'r+')
text = myFile.read(100)
print(text)
