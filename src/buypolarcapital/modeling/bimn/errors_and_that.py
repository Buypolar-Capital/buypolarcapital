


# syntaxing it up
# while True: print('hello world!')

# while True:
#     try:
#         x = int(input('please enter a number: '))
#         break
#     except ValueError:
#         print('woopsies that wasnt a valid number')


class B(Exception):
    pass

class C(B):
    pass

class D(C):
    pass

for cls in [B,C,D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")


def this_fails():
    x = 1/0

try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error: ', err)

# raise NameError('HiThere')

print('yp')

# try:
#     raise NameError('HelloThere')
# except NameError:
#     print('an exception flew by')
#     raise

try:
    open('filessimo.txt')
except OSError:
    raise RuntimeError('unable to handle error')


modname.attribute = 42
print(modname.attribute)
print(modname)
print(attribute)





