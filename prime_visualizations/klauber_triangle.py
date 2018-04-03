import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Visualize prime numbers as a "Klauber triangle"
# The maths behind this code is described in the scipython blog
# article at https://scipython.com/blog/the-klauber-triangle/
# Christian Hill, November 2016.

n = 200
ncols = 2*n+1
nmax = n**2

# Prime numbers up to and including n**2.
primes = np.array([n for n in range(2,n**2+1) if all(
                        (n % m) != 0 for m in range(2,int(np.sqrt(n))+1))])
a = np.zeros(nmax)
a[primes-1]=1

arr = np.zeros((n, ncols))
for i in range(n):
    arr[i,(n-i):(n+i+1)] = a[i**2:i**2+2*i+1]

fig, ax = plt.subplots()
ax.matshow(arr, cmap=cm.binary)
ax.axis('off')
# Ensure the Axes are centred in the figure
ax.set_position([0.1,0.1,0.8,0.8])
plt.savefig('klauber_triangle.png')
plt.show()
