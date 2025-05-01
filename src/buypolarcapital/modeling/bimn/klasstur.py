


class ClassName:
    pass
ClassName()

class MyClass:
    """A simple example class bby"""
    i = 12345

    def f(self):
        return 'hello there'

print(MyClass.i)
print(MyClass.f)
print(MyClass.f(10))

x = MyClass()
print(x.i)


def __init__(self):
    self.data = []


class Complex:
    def __init__(self, realpart, imagpart):
        self.r, self.i = realpart, imagpart

x = Complex(3.0, -4.5)
x.r, x.i 
print(x.r, x.i)
print(x.r)
print(f'{x.r}{x.i}i')

x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
    print(x.counter)
print(x.counter)
del x.counter


x = MyClass()
print(x.f())

