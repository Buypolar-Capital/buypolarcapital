
year = 2016
event = 'Referendum'
print(f'Results of the {year} {event}')

yes_votes = 42_572_654
total_votes = 85_705_149
percentage = yes_votes/total_votes
print('{:-9} YES votes {:2.2%}'.format(yes_votes, percentage))

s = 'hello, there.'
print(str(s))
print(repr(s))

import math
print(f'the value of pi is approximately {math.pi:.3f}')



table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
    print(f'{name:10} ==> {phone:10d}')

for x in range(1,11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))


# f = open('filessimo.txt', 'w', encoding='utf-8')
# print(f)

with open('filessimo.txt', encoding='utf-8') as f:
    read_data = f.read()

print(f.closed)
print(f.read)


import pandas as pd

print(read_data)
# print(pd.DataFrame(read_data))


import json
x = [1, 'simple', 'list']
json.dumps(x)
print(json.dumps(x))


