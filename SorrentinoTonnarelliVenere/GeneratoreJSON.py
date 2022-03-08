import json
import string
import random as random

"""
In this method a random dictionary is created, the first element is a name,
the second one is a weight"
"""

def generate_random_string():
   S = random.randint(1,4)  # number of characters in the string.  
   # call random.choices() string module to find the string in Uppercase + numeric data.  
   ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
   return str(ran)

def new_dict_with_weight(string):   
    return dict(name=string,weight=random.randint(1,10))

def new_dict_without_weight(string):
    return dict(name=string)
      
def new_cons(array,dim): 
    m = random.randint(1,dim)
    var = set()
    while len(var) < m:
        var.add(array[random.randint(0,len(array)-1)])
    return dict(sets = list(var))
 


   
n = random.randint(1, 10)
s = []
for k in range (1,n):
    s.append(generate_random_string())
"""
We have to declare a list of n dictionaries in order to parse it in a
json array of objects
"""

sub = []
for i in range(1,n):
    if random.randint(0,1) == 1:
        sub.append(new_dict_without_weight(s[i-1]))
    else:
        sub.append(new_dict_with_weight(s[i-1]))
        
    
cons = []
for j in range(1,n):
    cons.append(new_cons(s,n))

problem = []
problem.append(dict(subsets=sub,constraints=cons))

with open("sample.json", "w") as outfile:
    json.dump(problem, outfile)
    












