import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Plot the "Goldbach Comet" illustrating the number of ways
# the numbers 3–nmax can be written as the sum of two primes. Mathematical
# details are available on my blog article at
# https://scipython.com/blog/the-goldbach-comet/
# Christian Hill, April 2017.

rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 16})
rc('text', usetex=True)

nmax = 2000
# Odd prime numbers up to nmax.
odd_primes = np.array([n for n in range(3, nmax) if all(
                        (n % m) != 0 for m in range(2,int(np.sqrt(n))+1))])

def get_g(n):
    g = 0
    for p in odd_primes:
        if p > n//2:
            break
        if n-p in odd_primes:
            g += 1
    return g
    
imax = nmax//2 - 1
idx = np.arange(imax)
def get_n_from_index(i):
    return 2*(i+2)
n = get_n_from_index(np.arange(imax))

g = np.zeros(imax, dtype=int)
for i in idx:
    g[i] = get_g(n[i])


i_0 = idx[((n%6)==0)]
i_2 = idx[((n%6)==2)]
i_4 = idx[((n%6)==4)]

plt.scatter(n[i_0], g[i_0], marker='+', c='b', alpha=0.5,
            label=r'$n=0\;(\mathrm{mod}\;6)$')
plt.scatter(n[i_2], g[i_2], marker='+', c='g', alpha=0.5,
            label=r'$n=2\;(\mathrm{mod}\;6)$')
plt.scatter(n[i_4], g[i_4], marker='+', c='r', alpha=0.5,
            label=r'$n=4\;(\mathrm{mod}\;6)$')
plt.xlim(0, nmax)
plt.ylim(0, np.max(g[i_0]))
plt.xlabel(r'$n$')
plt.ylabel(r'$g(n)$')
plt.legend(loc='upper left', scatterpoints=1)
plt.savefig('goldbach_comet.png')
plt.show()


