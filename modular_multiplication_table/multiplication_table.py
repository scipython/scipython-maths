import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Create a colour-coded multiplication table based on modular arithmetic.
# algorithm. The maths behind this code is described in the scipython blog
# article at
# https://scipython.com/blog/visulaizing-modular-multiplication-tables/
# Christian Hill, May 2016.


def multiplication_table(n, N=None, number_labels=True):
    """Create and plot an image of a multiplication table modulo n

    The table is of ij % n for i, j = 1, 2, ..., N-1. If not supplied,
    N defaults to n. If N is a mutiple of n, the pattern is repeated
    across the created image. The "rainbow" colormap is used, but zeros
    (corresponding to factors of n) are displayed in white.

    """

    if not N:
        N=n

    # A multiplication table (modulo n)
    arr = np.fromfunction(lambda i,j:(i+1)*(j+1) % n, (N-1,N-1))

    # Select a colormap, but we'll set 0 values to white
    cmap = matplotlib.cm.get_cmap('rainbow')
    cmap.set_under('w')

    fig, ax = plt.subplots()
    # Plot an image of the multiplication table in colours for values greater
    # than 1. Zero values get plotted in white thanks to set_under, above.
    ax.imshow(arr, interpolation='nearest', cmap=cmap, vmin=1)

    # Make sure the tick marks are correct (start at 1)
    tick_formatter = FuncFormatter(lambda v, pos: str(int(v+1)))
    ax.xaxis.set_major_formatter(tick_formatter)
    ax.yaxis.set_major_formatter(tick_formatter)

    # For small n, write the value in each box of the array image.
    if number_labels and N < 21:
        for i in range(N-1):
            for j in range(N-1):
                ax.annotate(s=str((i+1)*(j+1)%n), xy=(i,j), ha='center',
                            va='center')

# The user supplies n (and optionally N) as command line arguments
n = int(sys.argv[1])
try:
    N = int(sys.argv[2])
except IndexError:
    N = None

number_labels = False
multiplication_table(n, N, number_labels)
plt.savefig('modmult-{}-{}.png'.format(N if N else n, n))
plt.show()
