
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart, 
        self.i = imagpart

x = Complex(3.0, 4.5)
print(x.r, x.i)
print(f"{x.r}+{x.i}")

class Dog:

    kind = 'canine'

    def __init__(self, name):
        self.name = name

d = Dog(name='Fido')
print(d)
print(d.name)
print(d.kind)


class Cat:

    tricks = []

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Cat('Kate')
e = Cat('Mistoffeles')
d.add_trick('roll_over')
d.add_trick('jump')
d.add_trick('yabbadabbadoo')
print(d.tricks)


class Bag:
    def __init__(self):
        self.data=[]
    
    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)

gucci = Bag()
gucci.addtwice('makeup')
print(gucci)

# ---












