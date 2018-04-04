import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Demonstrate that the distribution for the number of times "heads" leads
# "tails" in the sequential tossing of ntosses coins follows the "arcsine
# law". The maths behind this code is described in the scipython blog           
# article at https://scipython.com/blog/the-arcsine-law/
# Christian Hill, March 2017.

rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

# Number of coin tosses in each trial sequence.
ntosses = 1000
# Number of trials of ntosses to repeat.
ntrials = 10000

def coin_tosses(ntosses):
    """Return a running score for ntosses coin tosses.

    Each toss scores +1 for a head and -1 for a tail.

    """

    return np.cumsum(np.random.choice([-1,1], size=ntosses))

def n_times_ahead(ntosses):
    """Return the number of times "heads" leads in N coin tosses.

    Simulate ntosses tosses of a fair coin and return the number of times
    during this sequence that the cumulative number of "heads" results exceeds
    the number of "tails" results.

    """

    tosses = coin_tosses(ntosses)
    return sum(tosses>0)

# Number of tosses out of ntosses that "heads" leads over "tails" for each
# of ntrials trials.
n_ahead = np.array([n_times_ahead(ntosses) for i in range(ntrials)])

# Plot a histogram in nbins bins and the arcsine distribution.
nbins = 20
bins = np.linspace(0, ntosses, nbins)
hist, bin_edges = np.histogram(n_ahead, bins=bins, normed=True)
bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2

dpi = 72
plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)

# bar widths in units of the x-axis.
bar_width = ntosses/nbins * 0.5
plt.bar(bin_centres, hist, align='center', width=bar_width, facecolor='r',
        edgecolor=None, alpha=0.7)

# The arcsine distribution
x = np.linspace(0, 1, 100)
plt.plot(x*ntosses, 1/np.pi/np.sqrt(x*(1-x))/ntosses, color='g', lw=2)

plt.xlabel('Number of times ``heads" leads')
plt.savefig('arcsine.png', dpi=dpi)
plt.show()
