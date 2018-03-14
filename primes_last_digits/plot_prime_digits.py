import numpy as np
import matplotlib.pyplot as plt

# Create a set of bar charts summarizing the probabilities associated with
# the last digits of consecutive prime numbers. More details
# at https://scipython.com/blog/do-consecutive-primes-avoid-sharing-the-same-last-digit/
# Christian Hill, March 2016.

# Dictionary of consecutive digit counts for the first 10,000,000 primes
digit_count = {1: {1: 446808, 3: 756072, 9: 526953, 7: 769924},
               3: {1: 593196, 3: 422302, 9: 769915, 7: 714795},
               9: {1: 820369, 3: 640076, 9: 446032, 7: 593275},
               7: {1: 639384, 3: 681759, 9: 756852, 7: 422289}}
fig, ax = plt.subplots(nrows=2, ncols=2, facecolor='#dddddd')

xticks = [0,1,2,3]
last_digits = [1,3,7,9]
for i, d in enumerate(last_digits):
    ir, ic = i // 2, i % 2 
    this_ax = ax[ir,ic]
    this_ax.patch.set_alpha(1)
    count = np.array([digit_count[d][j] for j in last_digits])
    total = sum(count)
    prob = count / total * 100
    this_ax.bar(xticks, prob, align='center', color='maroon', ec='maroon',
                alpha=0.7)
    this_ax.set_title('Last digit of prime: {:d}'.format(d), fontsize=14)
    this_ax.set_xticklabels(['{:d}'.format(j) for j in last_digits])
    this_ax.set_xticks(xticks)
    this_ax.set_yticks([0,10,20,30,40])
    this_ax.set_ylim(0,35)
    this_ax.set_yticks([])
    for j, pr in enumerate(prob):
        this_ax.annotate('{:.1f}%'.format(pr), xy=(j, pr-2), ha='center',
                         va='top', color='w', fontsize=12)
    this_ax.set_xlabel('Next prime ends in')
    this_ax.set_frame_on(False)
    this_ax.tick_params(axis='x', length=0)
    this_ax.tick_params(axis='y', length=0)
fig.subplots_adjust(wspace=0.2, hspace=0.7, left=0, bottom=0.1, right=1,
                    top=0.95)
plt.savefig('prime_digits.png')
plt.show()


