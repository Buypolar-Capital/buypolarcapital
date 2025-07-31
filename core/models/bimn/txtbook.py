
print(10//3)
print(10%3)
print(5**2)

print(10)

for _ in range(5):
    print("hello")

for _ in ['apple', 'banana', 'orange']:
    print("Processing")

pairs = [(1,"one"), (2,"two"), (3,"three")]
for num, _ in pairs:
    print(num)

print('first line \nsecond line')
print(r'first line \nsecond line')
print(3*'un'+'ium')
print('py' 'thon')

word = 'python'
print(word[0])
print(word[1])
# print(word[-7])

s = 'supercalifragilisticexpialidocious'
print(len(s))

squares = [1, 4, 9, 16, 25]
print(squares)
print(squares[0])
print(squares[:1])
print(squares[:6])
print(squares+[40,46])

a, b = 0, 1
while a < 10:
    print(a)
    a, b = b, a+b

i = 256*256
print('the value of i is', i)
print(f'the value of i is {i}')

a, b = 0, 1
while a < 1000:
    print(a, end=', ')
    a, b = b, a+b

print('\n')


# x = int(input("Please enter an integer: "))
# if x < 0:
#     x = 0
#     print('negative changed to zero')
# elif x == 0:
#     print('zero')
# elif x == 1:
#     print('single')
# else:
#     print('none')

words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

users = {'Hans':'active', 'Eleonore':'inactive', '您好':'active'}
print(users)

for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

a = ['mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])

print(sum(range(4)))

# 4.4. break and continue Statements