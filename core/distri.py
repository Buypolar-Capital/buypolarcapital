import random
import math
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the folder exists
os.makedirs('plots', exist_ok=True)

a = []
i = 0
while i <= 1:
    j = random.random()
    j = ((j ** random.random() * 1 / random.random() ** 2 + i / math.pi) ** 2 + math.pi + random.random() ** 2)*(random.random()-random.random())
    a.append(j)
    i = i + 0.00001

# Plot histogram with log y-scale
plt.figure(figsize=(10, 5))
plt.hist(a, bins=500, edgecolor='black')
plt.yscale('log')  # apply log scale on y-axis
plt.title('Histogram (Log Scale)')
plt.xlabel('Value')
plt.ylabel('Frequency (log scale)')
plt.savefig('plots/histogram_log.pdf')
plt.show()

# Plot scatter of index vs value with log y-axis
plt.figure(figsize=(10, 5))
plt.scatter(range(len(a)), a, s=1, alpha=0.5)
plt.yscale('log')
plt.title('Scatter Plot (Log Scale)')
plt.xlabel('Index')
plt.ylabel('Value (log scale)')
plt.savefig('plots/scatter_log.pdf')
plt.show()

# Plot KDE on log-transformed values
log_a = [math.log(x) for x in a if x > 0]  # filter out non-positive
plt.figure(figsize=(10, 5))
sns.kdeplot(log_a, fill=True)
plt.title('KDE of log(values)')
plt.xlabel('log(Value)')
plt.ylabel('Density')
plt.savefig('plots/kde_log.pdf')
plt.show()
