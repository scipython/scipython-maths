import numpy as np
from matplotlib import rc
import matplotlib.pylab as plt

# Simulate a coin-tossing experiment in which, in each of ntrials trials
# a fair coin is tossed ntosses times and a record kept, on each toss, of
# the difference between the total number of heads and total number of tails
# seen. The maths behind this code is described in the scipython blog
# article at https://scipython.com/blog/the-arcsine-law/
# Christian Hill, March 2017.

rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

def coin_tosses(ntosses):
    return np.cumsum(np.random.choice([-1,1], size=ntosses))

ntrials = 10
ntosses = 1000

for i in range(ntrials):
    plt.plot(range(ntosses), coin_tosses(ntosses), c='r', alpha=0.4)
plt.axhline(c='k')
plt.xlabel('Toss number')
plt.ylabel(r'$n_\mathrm{heads}-n_\mathrm{tails}$')
plt.savefig('random_walk.png')
plt.show()
