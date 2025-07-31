

a = [1,2,3]
b = [4,5,6]
a[len(a):] = [5]
print(a)
a.insert(0,1)
a.insert(2,2)
print(a)
a.pop()
print(a.pop())
a.clear()
print(a)
print(b)
del b[:]
print(b)
c = [1,2,3,4,5,6,7,8,9,1,2,3,1,2,4,5,3,21,3,3,4,5,2]
print(c.count(2))

import yfinance as yf
import pandas as pd

aapl = yf.download('AAPL', start="2020-01-01", end="2024-01-01")
print(aapl)


print("\n")
df = pd.DataFrame(aapl)
print(df)

print(df['Close'])
print(df.Close.head(2))

print(df[df['Close']>=191])

import numpy as np

df['CloseLog'] = np.log(df['Close'])
print(df.head(3))



# print(df.groupby('Date').agg(avg_volume=('Volume', 'mean')).head(3))

# print(df[('Price', 'Volume')])


stack = [3,4,5]
stack.append(6)
stack.append(7)
print(stack)
print(stack.pop())
print(stack.pop())
print(stack.pop())
print(stack)
