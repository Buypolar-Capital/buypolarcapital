
import math 
print(math.cos(math.pi/4))
print(math.log(1024, 2))
print(math.log(1024, 10))
print(math.log(10000000, 10))

import random
print(random.choice(['apple', 'banana', 'pear']))
print(random.sample(range(100), 10))
print(random.random())
print(random.randrange(6))

a = []
i = 0
while i <= 1:
    j = random.random()
    j = (j**random.random()*1/random.random()**2+i/math.pi)**2 + math.pi + random.random()**2
    print(j)
    a.append(j)
    i = i + 0.00001

import matplotlib.pyplot as plt
# plt.figure(figsize=(10,5))
# plt.hist(a, bins=1000, edgecolor='black', density=True)
# plt.show()

import seaborn as sns
plt.figure(figsize=(10,5))
# sns.kdeplot(a, fill=True)
plt.hist(a, bins=1000, edgecolor='black')
plt.show()
plt.savefig('plots/dense_mofo.pdf')
