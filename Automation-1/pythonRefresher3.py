#A module is basically a file contatining a set of functions to include in your application.
# There are core python modules, modules you can install using the pip package manager 

import datetime
from datetime import date 
import time 
from time import time 

#import custom modules 
from validator import validate_email as v

#today = datatime.date.today()
today = date.today()
print(today)

timestamp = time()
print(timestamp)

#custom modules 
email = 'test@test.com'
if v(email):
    print("Email is valid")
else:
    print("Email is bad")