
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} is {x}*{n//x}")
            break

for num in range(2, 10):
    if num % 2 == 0:
        print(f"Found an even number {num}")
        continue
    print(f"Found an odd number {num}")

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
        else:
            print(n, 'is a prime number')


print('hello')


def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 401 | 402 | 403 | 404:
            return "Not found"
        case 418:
            return "I am a teapot"
        case _:
            return "Something wrong with the internet"

print(http_error(404))
print(http_error(402))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")
        
for _ in range(10):
    print(10)


print('\n')
class Dog:
    def bark(self):
        print("Woof!")

d = Dog()

print(d.bark)
d.bark()

print('\n')


def greet():
    print("HellO!")

def run_twice(func):
    func()
    func()

run_twice(greet)


print(f'\n')


def fib(n):
    """Print a fibonacci sequence less than n"""
    a, b = 0, 1
    while a < n:
        print(a, end=" ")
        a, b = b, a+b
    print()

fib(10**2)

print("yo")

def fib2(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result 

f100 = fib2(100)
f100  
print(f100)


print(f'\n')


def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        reply = input(prompt)
        if reply in {'y', 'ye', 'yes'}:
            return True
        if reply in {'n', 'no', 'nope'}:
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)

# ask_ok(prompt="Hey there: ")


def f(a, L=[]):
    L.append(a)
    return L

print(f(1))
print(f(4))
print(f(1))


def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry we're all out of", kind)
    for arg in arguments:
        print(arg)
    print('-'*40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("limburger", "its very runny sir", "its really very veryr unny sir", shopkeeper="michael palin")
    



def foo(name, /, **kwds):
    return 'name' in kwds

print(foo(1, **{'name':2}))
print('\n')







