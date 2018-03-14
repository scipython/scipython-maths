import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Create a heatmap summarizing the probabilities associated with
# the last digits of consecutive prime numbers. More details
# at https://scipython.com/blog/do-consecutive-primes-avoid-sharing-the-same-last-digit/
# Christian Hill, March 2016.

# First 10,000,000 primes
digit_count = {1: {1: 446808, 3: 756072, 9: 526953, 7: 769924},
               3: {1: 593196, 3: 422302, 9: 769915, 7: 714795},
               9: {1: 820369, 3: 640076, 9: 446032, 7: 593275},
               7: {1: 639384, 3: 681759, 9: 756852, 7: 422289}}
last_digits = [1,3,7,9]

hmap = np.empty((4,4))
for i, d1 in enumerate(last_digits):
    total = sum(digit_count[d1].values())
    for j, d2 in enumerate(last_digits):
        hmap[i,j] = digit_count[d1][d2] / total * 100

fig = plt.figure()
ax = fig.add_axes([0.1,0.3,0.8,0.6])
im = ax.imshow(hmap, interpolation='nearest', cmap=plt.cm.YlOrRd, origin='lower')
tick_labels = [str(d) for d in last_digits]
ax.set_xticks(range(4))
ax.set_xticklabels(tick_labels)
ax.set_xlabel('Last digit of second prime')
ax.set_yticks(range(4))
ax.set_yticklabels(tick_labels)
ax.set_ylabel('Last digit of first prime')

cbar_axes = fig.add_axes([0.1,0.1,0.8,0.05])

cbar = plt.colorbar(im, orientation='horizontal', cax=cbar_axes)
cbar.ax.set_xlabel('Probability /%')

plt.savefig('prime_digits_hmap.png')
plt.show()
