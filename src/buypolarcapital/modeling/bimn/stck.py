stack = [3,4,5]
stack.append(6)
stack.append(7)
print(stack)
print(stack.pop())
print(stack.pop())
print(stack.pop())
print(stack)

from collections import deque 

queue = deque(["Eric", "John", "Michael"])
print(queue)
queue.append("Terry")
print(queue.append("Graham"))
queue.popleft()
queue.popleft()
print(queue)


squares = []
for x in range(10):
    squares.append(x**2)
print(squares)

sques = list(map(lambda x: x**2, range(10)))
print(sques)

sqrus = [x**2 for x in range(10)]
print(sqrus)

dongas = [(x,y) for x in [1,2,3] for y in [3,1,4] if x != y]
print(dongas)

vec = [-4, -2, 0, 2, 4]
vec2 = [x*2 for x in vec]
print(vec2)

# create a list of 2-tuples like (number, square)

df = [(x, x**2) for x in range(10000)]
print(df)


vec = [[1,2,3], [4,5,6], [7,8,9]]
df = [num for elem in vec for num in elem]
print(df)

from math import pi
df = [str(round(pi, i)) for i in range(10000)]
print(df)






