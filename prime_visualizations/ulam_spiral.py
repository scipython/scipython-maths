import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Visualize prime numbers as an "Ulam spiral"
# The maths behind this code is described in the scipython blog
# article at https://scipython.com/blog/the-ulam-spiral/
# Christian Hill, October 2016.

def make_spiral(arr):
    nrows, ncols= arr.shape
    idx = np.arange(nrows*ncols).reshape(nrows,ncols)[::-1]
    spiral_idx = []
    while idx.size:
        spiral_idx.append(idx[0])
        # Remove the first row (the one we've just appended to spiral).
        idx = idx[1:]
        # Rotate the rest of the array anticlockwise
        idx = idx.T[::-1]
    # Make a flat array of indices spiralling into the array.
    spiral_idx = np.hstack(spiral_idx)
    # Index into a flattened version of our target array with spiral indices.
    spiral = np.empty_like(arr)
    spiral.flat[spiral_idx] = arr.flat[::-1]
    return spiral

# edge size of the square array.
w = 251
# Prime numbers up to and including w**2.
primes = np.array([n for n in range(2,w**2+1) if all(
                        (n % m) != 0 for m in range(2,int(np.sqrt(n))+1))])
# Create an array of boolean values: 1 for prime, 0 for composite
arr = np.zeros(w**2, dtype='u1')
arr[primes-1] = 1
# Spiral the values clockwise out from the centre
arr = make_spiral(arr.reshape((w,w)))

plt.matshow(arr, cmap=cm.binary)
plt.axis('off')
plt.savefig('ulam_spiral.png')
plt.show()
